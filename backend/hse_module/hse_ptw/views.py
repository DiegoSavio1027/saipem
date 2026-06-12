from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import PermitToWork
from hr_module.models import Employee
from .serializers import PermitToWorkSerializer, EmployeeSerializer
from ..hse_analytics.services import update_analytics_realtime


def check_emergency_lockdown():
    """Check if system is in CONDITION RED (Emergency Lockdown)"""
    from ..hse_safety.models import SystemStatus
    try:
        system_status = SystemStatus.objects.get(id=1)
        return system_status.global_status == 'RED'
    except SystemStatus.DoesNotExist:
        return False


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    READ-ONLY ViewSet for Employee model
    HSE module can only READ employee data for PTW forms
    Only HR module has permission to create/update/delete employees
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'emp_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return all employees (except Admin and HR Staff), or filter by active vessel roster if vessel_id is provided"""
        queryset = Employee.objects.exclude(job_role__in=['Admin', 'HR Staff'])
        vessel_id = self.request.query_params.get('vessel_id')
        
        if vessel_id:
            from hr_module.models import Roster
            from django.utils import timezone
            
            today = timezone.now().date()
            # Find active rosters for the specified vessel on today's date
            active_rosters = Roster.objects.filter(
                vessel_id=vessel_id,
                start_date__lte=today,
                end_date__gte=today
            )
            # Filter employees by those who have active rosters
            emp_ids = active_rosters.values_list('employee_id', flat=True)
            queryset = queryset.filter(emp_id__in=emp_ids)
            
        return queryset


class PermitToWorkViewSet(viewsets.ModelViewSet):
    """ViewSet for PermitToWork model with custom actions"""
    queryset = PermitToWork.objects.all()
    serializer_class = PermitToWorkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter PTWs based on user role and vessel"""
        user = self.request.user
        queryset = PermitToWork.objects.all()

        # Vessel filtering
        vessel_id = self.request.query_params.get('vessel')
        if vessel_id:
            queryset = queryset.filter(vessel_id=vessel_id)

        # Role-based filtering
        if user.is_superuser:
            return queryset

        # Check user's group/role
        if user.groups.filter(name__in=['Admin', 'Safety Officer']).exists():
            return queryset

        # Workers see only their own PTWs
        return queryset.filter(emp_id=user.username)

    def perform_create(self, serializer):
        """Save PTW with emp_id from request data - blocked during emergency"""
        if check_emergency_lockdown():
            raise ValueError("PTW operations are locked during CONDITION RED (Emergency)")
        ptw = serializer.save()

        # Get employee name
        try:
            employee = Employee.objects.get(emp_id=ptw.emp_id)
            employee_name = employee.full_name
        except Employee.DoesNotExist:
            employee_name = ptw.emp_id

        # Broadcast PTW created event
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "ptw_updates",
            {
                "type": "ptw_created",
                "message": {
                    "event": "PTW_CREATED",
                    "permit_id": ptw.permit_id,
                    "emp_id": ptw.emp_id,
                    "employee_name": employee_name,
                    "permit_type": ptw.permit_type,
                    "status": ptw.status,
                    "deck_location": ptw.deck_location,
                    "timestamp": ptw.created_at.isoformat(),
                    "affected_user": ptw.emp_id,
                    "notify_role": "Safety Officer"
                }
            }
        )

        # Update analytics in real-time
        update_analytics_realtime()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a PTW - blocked during emergency"""
        if check_emergency_lockdown():
            return Response(
                {"error": "PTW approvals are locked during CONDITION RED (Emergency)"},
                status=status.HTTP_403_FORBIDDEN
            )

        ptw = self.get_object()

        if ptw.status != 'PENDING':
            return Response(
                {"error": "Only PENDING PTWs can be approved"},
                status=status.HTTP_400_BAD_REQUEST
            )

        signature = request.data.get('signature')
        if not signature:
            return Response(
                {"error": "Signature is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get approver's full name from Employee model
        try:
            approver = Employee.objects.get(emp_id=request.user.username)
            approver_name = approver.full_name
        except Employee.DoesNotExist:
            approver_name = request.user.username

        ptw.status = 'APPROVED'
        ptw.approved_by = approver_name
        ptw.approved_at = timezone.now()
        ptw.signature = signature
        ptw.save()

        # Broadcast PTW approved event
        try:
            employee = Employee.objects.get(emp_id=ptw.emp_id)
            employee_name = employee.full_name
        except Employee.DoesNotExist:
            employee_name = ptw.emp_id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "ptw_updates",
            {
                "type": "ptw_status_changed",
                "message": {
                    "event": "PTW_APPROVED",
                    "permit_id": ptw.permit_id,
                    "emp_id": ptw.emp_id,
                    "employee_name": employee_name,
                    "permit_type": ptw.permit_type,
                    "status": ptw.status,
                    "approved_by": approver_name,
                    "approved_at": ptw.approved_at.isoformat(),
                    "timestamp": timezone.now().isoformat(),
                    "affected_user": ptw.emp_id,
                    "notify_role": "Worker"
                }
            }
        )

        return Response(
            {"message": f"PTW {ptw.permit_id} approved successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def start_work(self, request, pk=None):
        """Start work on a PTW - changes status to IN_PROGRESS and auto check-in"""
        ptw = self.get_object()

        if ptw.status != 'APPROVED':
            return Response(
                {"error": "Only APPROVED PTWs can be started"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ptw.status = 'IN_PROGRESS'
        ptw.save()

        # Phase 5 Integration: Update WorkOrder Status
        if ptw.wo_id:
            ptw.wo_id.status = 'IN_PROGRESS'
            ptw.wo_id.save()

        # Auto CHECK-IN: Create POB log when PTW starts
        from ..hse_pob.models import POBLog
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        if not ptw.deck_location:
            return Response(
                {"error": "Cannot start work without a valid deck location."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create POB Log for Applicant
        pob_log = POBLog.objects.create(
            emp_id=ptw.emp_id,
            deck_location=ptw.deck_location,
            action='IN',
            ptw=ptw
        )

        # Create POB Log for all Assigned Personnel (Crew)
        crew_members = ptw.assigned_personnel.all()
        for crew in crew_members:
            POBLog.objects.create(
                emp_id=crew.emp_id,
                deck_location=ptw.deck_location,
                action='IN',
                ptw=ptw
            )

        try:
            employee = Employee.objects.get(emp_id=ptw.emp_id)
            employee_name = employee.full_name
        except Employee.DoesNotExist:
            employee_name = ptw.emp_id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "pob_dashboard",
            {
                "type": "send_location_update",
                "message": {
                    "action": pob_log.action,
                    "employee_name": employee_name,
                    "location": pob_log.deck_location.deck_name,
                    "timestamp": pob_log.timestamp.isoformat()
                }
            }
        )

        return Response(
            {"message": f"PTW {ptw.permit_id} started successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a PTW"""
        ptw = self.get_object()

        if ptw.status != 'PENDING':
            return Response(
                {"error": "Only PENDING PTWs can be rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rejection_reason = request.data.get('rejection_reason')
        if not rejection_reason:
            return Response(
                {"error": "Rejection reason is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get rejector's full name from Employee model
        try:
            rejector = Employee.objects.get(emp_id=request.user.username)
            rejector_name = rejector.full_name
        except Employee.DoesNotExist:
            rejector_name = request.user.username

        ptw.status = 'REJECTED'
        ptw.rejected_by = rejector_name
        ptw.rejected_at = timezone.now()
        ptw.rejection_reason = rejection_reason
        ptw.save()

        # Broadcast PTW rejected event
        try:
            employee = Employee.objects.get(emp_id=ptw.emp_id)
            employee_name = employee.full_name
        except Employee.DoesNotExist:
            employee_name = ptw.emp_id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "ptw_updates",
            {
                "type": "ptw_status_changed",
                "message": {
                    "event": "PTW_REJECTED",
                    "permit_id": ptw.permit_id,
                    "emp_id": ptw.emp_id,
                    "employee_name": employee_name,
                    "permit_type": ptw.permit_type,
                    "status": ptw.status,
                    "rejected_by": rejector_name,
                    "rejected_at": ptw.rejected_at.isoformat(),
                    "rejection_reason": rejection_reason,
                    "timestamp": timezone.now().isoformat(),
                    "affected_user": ptw.emp_id,
                    "notify_role": "Worker"
                }
            }
        )

        return Response(
            {"message": f"PTW {ptw.permit_id} rejected successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def mark_done(self, request, pk=None):
        """Mark PTW as job done"""
        ptw = self.get_object()

        if ptw.status != 'IN_PROGRESS':
            return Response(
                {"error": "Only IN_PROGRESS PTWs can be marked as done"},
                status=status.HTTP_400_BAD_REQUEST
            )

        completion_notes = request.data.get('completion_notes', '')
        ptw.status = 'WAITING_FOR_CLOSE'
        ptw.completion_notes = completion_notes
        ptw.save()

        # Auto CHECK-OUT: Create POB log when PTW marked as done
        from ..hse_pob.models import POBLog
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        if ptw.deck_location:
            # Create POB log for Applicant
            pob_log = POBLog.objects.create(
                emp_id=ptw.emp_id,
                deck_location=ptw.deck_location,
                action='OUT',
                ptw=ptw
            )
            
            # Create POB log for all Assigned Personnel
            crew_members = ptw.assigned_personnel.all()
            for crew in crew_members:
                POBLog.objects.create(
                    emp_id=crew.emp_id,
                    deck_location=ptw.deck_location,
                    action='OUT',
                    ptw=ptw
                )

            location_name = pob_log.deck_location.deck_name
            timestamp_iso = pob_log.timestamp.isoformat()
        else:
            location_name = "Unknown Location"
            timestamp_iso = timezone.now().isoformat()

        # Get employee name
        try:
            employee = Employee.objects.get(emp_id=ptw.emp_id)
            employee_name = employee.full_name
        except Employee.DoesNotExist:
            employee_name = ptw.emp_id

        # Broadcast via WebSocket (POB)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "pob_dashboard",
            {
                "type": "send_location_update",
                "message": {
                    "action": 'OUT',
                    "employee_name": employee_name,
                    "location": location_name,
                    "timestamp": timestamp_iso
                }
            }
        )

        # Broadcast PTW marked done event
        async_to_sync(channel_layer.group_send)(
            "ptw_updates",
            {
                "type": "ptw_status_changed",
                "message": {
                    "event": "PTW_MARKED_DONE",
                    "permit_id": ptw.permit_id,
                    "emp_id": ptw.emp_id,
                    "employee_name": employee_name,
                    "permit_type": ptw.permit_type,
                    "status": ptw.status,
                    "completion_notes": completion_notes,
                    "timestamp": timezone.now().isoformat(),
                    "affected_user": ptw.emp_id,
                    "notify_role": "Safety Officer"
                }
            }
        )

        return Response(
            {"message": f"PTW {ptw.permit_id} marked as job done"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def confirm_close(self, request, pk=None):
        """Confirm close of PTW"""
        ptw = self.get_object()

        if ptw.status != 'WAITING_FOR_CLOSE':
            return Response(
                {"error": "PTW is not waiting for close"},
                status=status.HTTP_400_BAD_REQUEST
            )

        closing_notes = request.data.get('closing_notes', '')

        # Get closer's full name from Employee model
        try:
            closer = Employee.objects.get(emp_id=request.user.username)
            closer_name = closer.full_name
        except Employee.DoesNotExist:
            closer_name = request.user.username

        ptw.status = 'CLOSED'
        ptw.closed_by = closer_name
        ptw.closed_at = timezone.now()
        ptw.closing_notes = closing_notes
        ptw.save()

        # Phase 5 Integration: Update WorkOrder Status
        if ptw.wo_id:
            ptw.wo_id.status = 'COMPLETED'
            ptw.wo_id.completion_date = timezone.now().date()
            ptw.wo_id.save()

        # Broadcast PTW closed event
        try:
            employee = Employee.objects.get(emp_id=ptw.emp_id)
            employee_name = employee.full_name
        except Employee.DoesNotExist:
            employee_name = ptw.emp_id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "ptw_updates",
            {
                "type": "ptw_status_changed",
                "message": {
                    "event": "PTW_CLOSED",
                    "permit_id": ptw.permit_id,
                    "emp_id": ptw.emp_id,
                    "employee_name": employee_name,
                    "permit_type": ptw.permit_type,
                    "status": ptw.status,
                    "closed_by": closer_name,
                    "closed_at": ptw.closed_at.isoformat(),
                    "closing_notes": closing_notes,
                    "timestamp": timezone.now().isoformat(),
                    "affected_user": ptw.emp_id,
                    "notify_role": "Worker"
                }
            }
        )

        return Response(
            {"message": f"PTW {ptw.permit_id} closed successfully"},
            status=status.HTTP_200_OK
        )
