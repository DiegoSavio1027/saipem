from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Incident, StatusOverride, SystemStatus
from .serializers import (
    IncidentSerializer,
    StatusOverrideSerializer,
    StatusOverrideDetailedSerializer,
    SystemStatusSerializer,
    IncidentReportSerializer,
    StatusOverrideRequestSerializer
)
from ..hse_analytics.services import update_analytics_realtime


class IncidentViewSet(viewsets.ModelViewSet):
    """
    API ViewSet untuk Incident
    Jalur 1: Bottom-Up dari lapangan
    """

    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter incidents berdasarkan query params"""
        queryset = Incident.objects.all()

        # Filter by vessel
        vessel_id = self.request.query_params.get('vessel')
        if vessel_id:
            queryset = queryset.filter(vessel_id=vessel_id)

        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)

        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location=location)

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(incident_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(incident_date__lte=end_date)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create incident report
        Otomatis update system metrics berdasarkan severity
        """
        serializer = IncidentReportSerializer(
            data=request.data,
            context={'user_id': request.user.username}
        )
        serializer.is_valid(raise_exception=True)
        incident = serializer.save()

        # Return incident dengan system status yang sudah updated
        system_status, _ = SystemStatus.get_or_create_singleton()
        response_data = {
            'incident': IncidentSerializer(incident).data,
            'system_status': SystemStatusSerializer(system_status).data,
            'impact': incident.get_impact_on_metrics()
        }

        # Broadcast incident created event
        from ..hse_pob.models import WorkLocation
        location_name = incident.location.name if incident.location else "Unknown"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "incidents_updates",
            {
                "type": "incident_created",
                "message": {
                    "event": "INCIDENT_CREATED",
                    "incident_id": incident.incident_id,
                    "severity": incident.severity,
                    "status": incident.status,
                    "location": location_name,
                    "description": incident.description,
                    "reported_by": incident.reported_by,
                    "employee_name": incident.employee_name,
                    "incident_date": incident.incident_date.isoformat(),
                    "timestamp": incident.created_at.isoformat(),
                    "notify_role": "Safety Officer"
                }
            }
        )

        # Broadcast system status if changed
        if incident.severity in ['FIRST_AID', 'LTI']:
            async_to_sync(channel_layer.group_send)(
                "incidents_updates",
                {
                    "type": "system_status_changed",
                    "message": {
                        "event": "SYSTEM_STATUS_CHANGED",
                        "global_status": system_status.global_status,
                        "days_without_lti": system_status.days_without_lti,
                        "near_misses_count": system_status.near_misses_count,
                        "timestamp": timezone.now().isoformat(),
                        "trigger": f"Incident {incident.incident_id} created",
                        "notify_all": True
                    }
                }
            )

        # Update analytics in real-time
        update_analytics_realtime()

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get incident statistics"""
        total_incidents = Incident.objects.count()
        lti_count = Incident.objects.filter(severity='LTI').count()
        near_miss_count = Incident.objects.filter(severity='NEAR_MISS').count()
        first_aid_count = Incident.objects.filter(severity='FIRST_AID').count()
        safety_obs_count = Incident.objects.filter(severity='SAFETY_OBSERVATION').count()

        # Last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        incidents_30d = Incident.objects.filter(incident_date__gte=thirty_days_ago).count()

        return Response({
            'total_incidents': total_incidents,
            'by_severity': {
                'lti': lti_count,
                'near_miss': near_miss_count,
                'first_aid': first_aid_count,
                'safety_observation': safety_obs_count
            },
            'incidents_last_30_days': incidents_30d
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent incidents (last 10)"""
        recent_incidents = Incident.objects.all()[:10]
        serializer = IncidentSerializer(recent_incidents, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update incident with WebSocket broadcast"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_status = instance.status

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Broadcast incident status changed if status changed
        if old_status != instance.status:
            from ..hse_pob.models import WorkLocation
            location_name = instance.location.name if instance.location else "Unknown"

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "incidents_updates",
                {
                    "type": "incident_status_changed",
                    "message": {
                        "event": "INCIDENT_STATUS_CHANGED",
                        "incident_id": instance.incident_id,
                        "severity": instance.severity,
                        "old_status": old_status,
                        "new_status": instance.status,
                        "location": location_name,
                        "reported_by": instance.reported_by,
                        "employee_name": instance.employee_name,
                        "timestamp": timezone.now().isoformat(),
                        "notify_role": "Safety Officer"
                    }
                }
            )

            # Update analytics in real-time when status changes
            update_analytics_realtime()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Partial update incident with WebSocket broadcast"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify or reject worker-reported incident
        Only for Admin/Safety Officer
        """
        incident = self.get_object()

        if incident.status != 'PENDING_VERIFICATION':
            return Response(
                {'error': 'Only pending incidents can be verified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        action = request.data.get('action')  # 'verify' or 'reject'
        rejection_reason = request.data.get('rejection_reason', '')

        if action == 'reject':
            if not rejection_reason or not rejection_reason.strip():
                return Response(
                    {'error': 'Rejection reason is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            incident.status = 'REJECTED'
            incident.rejection_reason = rejection_reason
            incident.verified_by = request.user.username
            incident.verified_at = timezone.now()
            incident.save()

            # Broadcast rejection
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "incidents_updates",
                {
                    "type": "incident_verified",
                    "message": {
                        "event": "INCIDENT_REJECTED",
                        "incident_id": incident.incident_id,
                        "severity": incident.severity,
                        "verified_by": incident.verified_by,
                        "timestamp": timezone.now().isoformat()
                    }
                }
            )

            return Response({
                'message': 'Incident rejected',
                'incident': IncidentSerializer(incident).data
            })

        elif action == 'verify':
            incident.status = 'OPEN'
            incident.verified_by = request.user.username
            incident.verified_at = timezone.now()
            incident.save()

            # Now apply metrics updates
            system_status, _ = SystemStatus.get_or_create_singleton()
            impact = incident.get_impact_on_metrics()

            if impact['days_without_lti'] == 'RESET_TO_ZERO':
                system_status.days_without_lti = 0
                system_status.last_lti_date = incident.incident_date.date()

            if impact['near_misses'] == 'INCREMENT':
                system_status.near_misses_count += 1

            if impact['global_status'] != 'NO_CHANGE':
                system_status.global_status = impact['global_status']

            system_status.last_incident_date = incident.incident_date
            system_status.save()

            # Broadcast verification and system status change
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "incidents_updates",
                {
                    "type": "incident_verified",
                    "message": {
                        "event": "INCIDENT_VERIFIED",
                        "incident_id": incident.incident_id,
                        "severity": incident.severity,
                        "verified_by": incident.verified_by,
                        "timestamp": timezone.now().isoformat()
                    }
                }
            )

            # Broadcast system status if changed
            if incident.severity in ['FIRST_AID', 'LTI']:
                async_to_sync(channel_layer.group_send)(
                    "incidents_updates",
                    {
                        "type": "system_status_changed",
                        "message": {
                            "event": "SYSTEM_STATUS_CHANGED",
                            "global_status": system_status.global_status,
                            "days_without_lti": system_status.days_without_lti,
                            "near_misses_count": system_status.near_misses_count,
                            "timestamp": timezone.now().isoformat(),
                            "trigger": f"Incident {incident.incident_id} verified",
                            "notify_all": True
                        }
                    }
                )

            # Update analytics in real-time
            update_analytics_realtime()

            return Response({
                'message': 'Incident verified and metrics updated',
                'incident': IncidentSerializer(incident).data,
                'system_status': SystemStatusSerializer(system_status).data
            })

        else:
            return Response(
                {'error': 'Invalid action. Use "verify" or "reject"'},
                status=status.HTTP_400_BAD_REQUEST
            )


class SystemStatusViewSet(viewsets.ViewSet):
    """
    API ViewSet untuk System Status
    Endpoint untuk dashboard metrics
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current system status"""
        from ..hse_ptw.models import PermitToWork

        system_status, _ = SystemStatus.get_or_create_singleton()
        system_status.calculate_days_without_lti()

        # Calculate active permits (APPROVED or IN_PROGRESS)
        active_permits_count = PermitToWork.objects.filter(
            status__in=['APPROVED', 'IN_PROGRESS']
        ).count()
        system_status.active_permits = active_permits_count

        serializer = SystemStatusSerializer(system_status)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def override(self, request):
        """
        Manual override status
        Jalur 2: Top-Down dari Command Center
        """
        serializer = StatusOverrideRequestSerializer(
            data=request.data,
            context={'user_id': request.user.username}
        )
        serializer.is_valid(raise_exception=True)
        override = serializer.save()

        system_status, _ = SystemStatus.get_or_create_singleton()

        response_data = {
            'override': StatusOverrideDetailedSerializer(override).data,
            'system_status': SystemStatusSerializer(system_status).data,
            'message': f'Status changed to {system_status.global_status}'
        }

        # Trigger actions based on status
        if system_status.global_status == 'RED':
            response_data['actions'] = [
                'ALARM_ACTIVATED',
                'PTW_APPROVALS_FROZEN',
                'EVACUATION_PROTOCOLS_READY'
            ]

        # Broadcast system status changed event
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "incidents_updates",
            {
                "type": "system_status_changed",
                "message": {
                    "event": "SYSTEM_STATUS_CHANGED",
                    "global_status": system_status.global_status,
                    "days_without_lti": system_status.days_without_lti,
                    "near_misses_count": system_status.near_misses_count,
                    "timestamp": timezone.now().isoformat(),
                    "trigger": "Manual override by Command Center",
                    "override_reason": override.override_reason,
                    "notify_all": True
                }
            }
        )

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get status override history (audit trail) with filtering and pagination

        Query params:
        - start_date: Filter by created_at >= start_date (ISO format)
        - end_date: Filter by created_at <= end_date (ISO format)
        - changed_by: Filter by employee ID
        - limit: Number of records to return (default: 20, max: 100)
        - offset: Number of records to skip (default: 0)
        """
        queryset = StatusOverride.objects.all()

        # Filter by date range
        start_date = request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        end_date = request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Filter by changed_by (employee ID)
        changed_by = request.query_params.get('changed_by')
        if changed_by:
            queryset = queryset.filter(changed_by=changed_by)

        # Get total count before pagination
        total_count = queryset.count()

        # Pagination
        try:
            limit = int(request.query_params.get('limit', 20))
            limit = min(limit, 100)  # Max 100 records per request
        except ValueError:
            limit = 20

        try:
            offset = int(request.query_params.get('offset', 0))
            offset = max(offset, 0)  # Ensure non-negative
        except ValueError:
            offset = 0

        # Apply pagination
        queryset = queryset[offset:offset + limit]

        serializer = StatusOverrideDetailedSerializer(queryset, many=True)

        return Response({
            'count': total_count,
            'limit': limit,
            'offset': offset,
            'results': serializer.data
        })
