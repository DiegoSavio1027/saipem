import datetime
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Roster, VesselActivity, Position, Certification
from .models import Employee
from asset_module.models import Vessel
from .serializers import (
    EmployeeSerializer,
    RosterSerializer,
    VesselActivitySerializer,
    PositionSerializer,
    CertificationSerializer
)

# ==========================================
# 1. POSITION RATE DATABASE API
# ==========================================

@api_view(['GET', 'POST'])
def position_list(request):
    if request.method == 'GET':
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_position(request, pk):
    try:
        position = Position.objects.get(pk=pk)
        position.delete()
        return Response({"message": "Position rate template deleted"}, status=status.HTTP_200_OK)
    except Position.DoesNotExist:
        return Response({"error": "Position template not found"}, status=status.HTTP_404_NOT_FOUND)


# ==========================================
# 2. EMPLOYEE & CREW API (WITH EDIT / UPDATE ENDPOINT!)
# ==========================================

@api_view(['GET'])
def get_all_employees(request):
    employees = Employee.objects.exclude(job_role__in=['Admin', 'HR Staff'])
    
    vessel_id = request.query_params.get('vessel_id')
    if vessel_id:
        employees = employees.filter(rosters__vessel_id=vessel_id).distinct()
        
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_employee(request):
    is_admin = request.user and request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    )
    role = request.data.get('job_role')
    if role in ['Admin', 'HR Staff'] and not is_admin:
        return Response(
            {"error": "Only Administrators are authorized to assign Admin or HR Staff roles."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# BARU: Endpoint Khusus Edit / Update Crew via Web Frontend (PATCH)
@api_view(['PUT', 'PATCH'])
def update_employee(request, emp_id):
    try:
        employee = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return Response({"error": "Crew not found"}, status=status.HTTP_404_NOT_FOUND)

    is_admin = request.user and request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    )
    role = request.data.get('job_role')
    if role and role != employee.job_role and role in ['Admin', 'HR Staff'] and not is_admin:
        return Response(
            {"error": "Only Administrators are authorized to assign Admin or HR Staff roles."},
            status=status.HTTP_403_FORBIDDEN
        )

    # partial=True memperbolehkan update sebagian kolom saja
    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_employee(request, emp_id):
    try:
        employee = Employee.objects.get(emp_id=emp_id)
        employee.delete()
        return Response({"message": "Crew deleted successfully"}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({"error": "Crew not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def toggle_roster_status(request, emp_id):
    try:
        employee = Employee.objects.get(emp_id=emp_id)
        if employee.roster_status == 'ONBOARD':
            employee.roster_status = 'AVAILABLE'
        else:
            employee.roster_status = 'ONBOARD'
        employee.save()
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({"error": "Crew not found"}, status=status.HTTP_404_NOT_FOUND)


# ==========================================
# 3. ROSTER SCHEDULING API
# ==========================================

@api_view(['GET', 'POST'])
def roster_list(request):
    if request.method == 'GET':
        rosters = Roster.objects.all()
        serializer = RosterSerializer(rosters, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RosterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_roster(request, pk):
    try:
        roster = Roster.objects.get(pk=pk)
        roster.delete()
        return Response({"message": "Roster assignment deleted"}, status=status.HTTP_200_OK)
    except Roster.DoesNotExist:
        return Response({"error": "Roster not found"}, status=status.HTTP_404_NOT_FOUND)


# ==========================================
# ==========================================
# 5. VESSEL OPERATIONAL ACTIVITY API
# ==========================================

@api_view(['GET', 'POST'])
def activity_list(request):
    if request.method == 'GET':
        asset_id = request.query_params.get('asset')
        if asset_id:
            activities = VesselActivity.objects.filter(asset_id=asset_id)
        else:
            activities = VesselActivity.objects.all()
        serializer = VesselActivitySerializer(activities, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VesselActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_activity(request, pk):
    try:
        activity = VesselActivity.objects.get(pk=pk)
        activity.delete()
        return Response({"message": "Activity log deleted"}, status=status.HTTP_200_OK)
    except VesselActivity.DoesNotExist:
        return Response({"error": "Activity log not found"}, status=status.HTTP_404_NOT_FOUND)


# ==========================================
# 6. AUTOMATED OFFSHORE PAYROLL API
# ==========================================

@api_view(['GET'])
def payroll_calculation(request):
    today = datetime.date.today()
    month = int(request.query_params.get('month', today.month))
    year = int(request.query_params.get('year', today.year))

    start_of_month = datetime.date(year, month, 1)
    if month == 12:
        end_of_month = datetime.date(year, 12, 31)
    else:
        end_of_month = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    payroll_data = []
    # Exclude non-offshore roles from payroll
    employees = Employee.objects.exclude(job_role__in=['Admin', 'HR Staff', 'System Administrator'])

    for emp in employees:
        emp_rosters = Roster.objects.filter(
            employee=emp,
            start_date__lte=end_of_month,
            end_date__gte=start_of_month
        )

        total_onboard_days = 0
        for roster in emp_rosters:
            overlap_start = max(roster.start_date, start_of_month)
            overlap_end = min(roster.end_date, end_of_month)
            days = (overlap_end - overlap_start).days + 1
            total_onboard_days += days

        pos = Position.objects.filter(title=emp.job_role).first()
        daily_rate = pos.daily_rate if pos else 500000
        allowance_rate = pos.allowance_rate if pos else 300000

        base_pay = total_onboard_days * daily_rate
        allowance_pay = total_onboard_days * allowance_rate
        total_earnings = base_pay + allowance_pay

        payroll_data.append({
            "emp_id": emp.emp_id,
            "full_name": emp.full_name,
            "job_role": emp.job_role,
            "daily_rate": daily_rate,
            "allowance_rate": allowance_rate,
            "total_days": total_onboard_days,
            "base_pay": base_pay,
            "allowance_pay": allowance_pay,
            "total_earnings": total_earnings
        })

    return Response(payroll_data)


# ==========================================
# 7. TACTICAL DASHBOARD ANALYTICS API
# ==========================================

@api_view(['GET'])
def dashboard_analytics(request):
    today = datetime.date.today()
    thirty_days_later = today + datetime.timedelta(days=30)
    
    total_crew = Employee.objects.exclude(job_role__in=['Admin', 'HR Staff']).count()
    onboard_crew = Employee.objects.exclude(job_role__in=['Admin', 'HR Staff']).filter(roster_status='ONBOARD').count()
    
    mcu_alerts = Employee.objects.exclude(job_role__in=['Admin', 'HR Staff']).filter(
        Q(mcu_status='EXPIRED') | 
        Q(mcu_status='UNFIT') |
        Q(mcu_expiry__lt=today) |
        Q(mcu_expiry__range=(today, thirty_days_later))
    ).distinct().count()
    
    total_vessels = Vessel.objects.count()
    active_vessels = Roster.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).values_list('vessel', flat=True).distinct().count()
    
    vessel_active_rate = 0
    if total_vessels > 0:
        vessel_active_rate = round((active_vessels / total_vessels) * 100)
        
    month = today.month
    year = today.year
    start_of_month = datetime.date(year, month, 1)
    if month == 12:
        end_of_month = datetime.date(year, 12, 31)
    else:
        end_of_month = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        
    rosters_current_month = Roster.objects.filter(
        start_date__lte=end_of_month,
        end_date__gte=start_of_month
    )
    
    estimated_budget = 0
    for roster in rosters_current_month:
        overlap_start = max(roster.start_date, start_of_month)
        overlap_end = min(roster.end_date, end_of_month)
        days = (overlap_end - overlap_start).days + 1
        
        emp = roster.employee
        
        pos = Position.objects.filter(title=emp.job_role).first()
        d_rate = pos.daily_rate if pos else 500000
        a_rate = pos.allowance_rate if pos else 300000
        
        estimated_budget += days * (d_rate + a_rate)

    return Response({
        "total_crew": total_crew,
        "onboard_crew": onboard_crew,
        "mcu_alerts": mcu_alerts,
        "total_vessels": total_vessels,
        "active_vessels": active_vessels,
        "estimated_budget": estimated_budget
    })


# ==========================================
# 8. CERTIFICATION MANAGEMENT API
# ==========================================

@api_view(['GET'])
def certification_list(request, emp_id):
    certs = Certification.objects.filter(employee_id=emp_id)
    serializer = CertificationSerializer(certs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_certification(request, emp_id):
    data = request.data.copy()
    data['employee'] = emp_id
    serializer = CertificationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_certification(request, cert_id):
    try:
        cert = Certification.objects.get(cert_id=cert_id)
        cert.delete()
        return Response({"message": "Certification deleted"}, status=status.HTTP_200_OK)
    except Certification.DoesNotExist:
        return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)