from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils import timezone
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import WorkLocation, POBLog
from .serializers import WorkLocationSerializer, POBLogSerializer, VesselWithDecksSerializer
from asset_module.models import Vessel

# Fungsi untuk mengecek apakah user adalah Safety Officer
def is_safety_officer(user):
    return user.groups.filter(name='Safety Officer').exists()

# View Endpoint Root API
def pob_dashboard(request):
    return JsonResponse({
        "status": "Online",
        "message": "SAIPEM HSE API is running. Please access the Vue.js frontend on port 5173."
    })

# View Rahasia (HANYA Safety Officer atau Admin yang boleh memicu ini)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_trigger(request):
    # Tolak jika bukan Safety Officer dan bukan Superuser
    if not (is_safety_officer(request.user) or request.user.is_superuser):
        return JsonResponse({"error": "AKSES DITOLAK: Hanya Safety Officer atau Admin yang dapat mengubah status POB."}, status=403)

    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from ..hse_safety.models import SystemStatus

    # Get parameters from query string
    target_status = request.GET.get('status', 'RED')  # Default to RED
    target_location = request.GET.get('location', 'ALL')  # Default to ALL
    target_vessel = request.GET.get('vessel', 'ALL')  # Default to ALL

    # 1. Set Global Status (RED or YELLOW)
    system_status = SystemStatus.objects.get_or_create(id=1)[0]
    system_status.global_status = target_status
    system_status.save()

    # 2. Get active PTW (IN_PROGRESS) - filter by location and vessel if specified
    from ..hse_ptw.models import PermitToWork
    active_ptws = PermitToWork.objects.filter(status='IN_PROGRESS')

    # Filter by location if not ALL
    if target_location != 'ALL':
        active_ptws = active_ptws.filter(deck_location=target_location)

    # Filter by vessel if not ALL
    if target_vessel != 'ALL':
        active_ptws = active_ptws.filter(vessel__asset_id=target_vessel)

    # 3. Broadcast emergency alert via WebSocket
    channel_layer = get_channel_layer()

    # Send emergency status change
    async_to_sync(channel_layer.group_send)(
        "pob_dashboard",
        {
            "type": "send_emergency_alert",
            "message": {
                "event": "MUSTER_DRILL_ACTIVATED",
                "global_status": target_status,
                "target_location": target_location,
                "target_vessel": target_vessel,
                "timestamp": timezone.now().isoformat(),
                "active_ptws_count": active_ptws.count(),
                "active_ptws": [
                    {
                        "permit_id": ptw.permit_id,
                        "emp_id": ptw.emp_id if isinstance(ptw.emp_id, str) else ptw.emp_id.emp_id,
                        "employee_name": ptw.emp_id.full_name if hasattr(ptw.emp_id, 'full_name') else str(ptw.emp_id),
                        "location": ptw.deck_location,
                        "status": ptw.status
                    }
                    for ptw in active_ptws
                ]
            }
        }
    )

    condition_text = f"CONDITION {target_status}"
    location_text = f"Location: {target_location}" if target_location != 'ALL' else "All Locations"
    vessel_text = f"Vessel: {target_vessel}" if target_vessel != 'ALL' else "All Vessels"

    return JsonResponse({
        "message": f"MUSTER DRILL ACTIVATED - {condition_text}",
        "global_status": target_status,
        "target_location": target_location,
        "target_vessel": target_vessel,
        "ptw_lockdown": True,
        "active_workers_in_danger": active_ptws.count(),
        "timestamp": timezone.now().isoformat()
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_offshore_vessels(request):
    """List all vessels with their assigned decks (GET: all users, POST: admin only)"""
    if request.method == 'GET':
        vessels = Vessel.objects.all()
        serializer = VesselWithDecksSerializer(vessels, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Admin check for POST
        if not (request.user.groups.filter(name='Admin').exists() or request.user.is_staff):
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)

        # Create new vessel
        vessel_data = {
            'vessel_name': request.data.get('name'),
            'vessel_type': request.data.get('type', 'Vessel'),
            'operational_status': 'OPERATIONAL'
        }

        vessel = Vessel.objects.create(**vessel_data)
        serializer = VesselWithDecksSerializer(vessel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_offshore_vessel_detail(request, vessel_id):
    """Get, update or delete a vessel (GET: all users, PUT/DELETE: admin only)"""
    vessel = get_object_or_404(Vessel, id=vessel_id)

    if request.method == 'GET':
        serializer = VesselWithDecksSerializer(vessel)
        return Response(serializer.data)

    # Admin check for PUT and DELETE
    if not (request.user.groups.filter(name='Admin').exists() or request.user.is_staff):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        vessel.vessel_name = request.data.get('name', vessel.vessel_name)
        vessel.vessel_type = request.data.get('type', vessel.vessel_type)
        vessel.save()
        serializer = VesselWithDecksSerializer(vessel)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        vessel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_offshore_locations(request):
    """Manage deck locations independently (GET: all users, POST: admin only)"""
    if request.method == 'GET':
        # Get all decks (independent, not filtered by vessel)
        locations = WorkLocation.objects.all().order_by('deck_name')
        serializer = WorkLocationSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Admin check for POST
        if not (request.user.groups.filter(name='Admin').exists() or request.user.is_staff):
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkLocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_offshore_location_detail(request, pk):
    """Get, update or delete a deck location (GET: all users, PUT/DELETE: admin only)"""
    location = get_object_or_404(WorkLocation, pk=pk)

    if request.method == 'GET':
        serializer = WorkLocationSerializer(location)
        return Response(serializer.data)

    # Admin check for PUT and DELETE
    if not (request.user.groups.filter(name='Admin').exists() or request.user.is_staff):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = WorkLocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_assign_decks_to_vessel(request, vessel_id):
    """Assign or unassign decks to/from a vessel (admin only)"""
    if not (request.user.groups.filter(name='Admin').exists() or request.user.is_staff):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)

    vessel = get_object_or_404(Vessel, id=vessel_id)

    if request.method == 'POST':
        # Assign decks to vessel using the many-to-many relationship
        deck_ids = request.data.get('deck_ids', [])
        if not deck_ids:
            return Response({'error': 'deck_ids required'}, status=status.HTTP_400_BAD_REQUEST)

        decks = WorkLocation.objects.filter(id__in=deck_ids)
        vessel.assigned_decks.add(*decks)

        serializer = VesselWithDecksSerializer(vessel)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        # Unassign all decks from vessel
        vessel.assigned_decks.clear()
        serializer = VesselWithDecksSerializer(vessel)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_unassign_deck_from_vessel(request, vessel_id, deck_id):
    """Unassign a specific deck from a vessel (admin only)"""
    if not (request.user.groups.filter(name='Admin').exists() or request.user.is_staff):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)

    vessel = get_object_or_404(Vessel, id=vessel_id)
    deck = get_object_or_404(WorkLocation, id=deck_id)

    vessel.assigned_decks.remove(deck)
    serializer = VesselWithDecksSerializer(vessel)
    return Response(serializer.data)
    if request.method == 'GET':
        # Filter by vessel if provided
        vessel_id = request.query_params.get('vessel_id')
        if vessel_id:
            locations = WorkLocation.objects.filter(vessel_id=vessel_id).order_by('deck_name')
        else:
            locations = WorkLocation.objects.all().order_by('deck_name')
        serializer = WorkLocationSerializer(locations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WorkLocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_location_detail(request, pk):
    location = get_object_or_404(WorkLocation, pk=pk)
    
    if request.method == 'PUT':
        serializer = WorkLocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_pob_log(request):
    if request.method == 'GET':
        # Get recent POB logs (last 10)
        logs = POBLog.objects.all()

        # Filter by vessel if provided
        vessel_id = request.query_params.get('vessel')
        if vessel_id:
            logs = logs.filter(vessel_id=vessel_id)

        logs = logs.order_by('-timestamp')[:10]
        serializer = POBLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = POBLogSerializer(data=request.data)
        if serializer.is_valid():
            pob_log = serializer.save()

            # Broadcast via WebSocket
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pob_dashboard",
                {
                    "type": "send_location_update",
                    "message": {
                        "action": pob_log.action,
                        "employee_name": serializer.data.get('employee_name', pob_log.emp_id),
                        "location": pob_log.deck_location,
                        "timestamp": pob_log.timestamp.isoformat()
                    }
                }
            )

            return Response({"message": "POB log recorded successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def api_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})

def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_role = "Admin" if user.is_superuser else (
                user.groups.first().name if user.groups.exists() else "No Role"
            )
            return JsonResponse({"message": "Login successful", "username": user.username, "role": user_role})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@ensure_csrf_cookie
def api_me(request):
    if request.user.is_authenticated:
        user_role = "Admin" if request.user.is_superuser else (
            request.user.groups.first().name if request.user.groups.exists() else "No Role"
        )

        # Try to get emp_id from Employee model, fallback to username
        emp_id = request.user.username  # Default to username
        try:
            from ..hse_ptw.models import Employee
            # Check if employee exists with this username as emp_id
            employee = Employee.objects.filter(emp_id=request.user.username).first()
            if employee:
                emp_id = employee.emp_id
        except Exception:
            pass

        return JsonResponse({
            "username": request.user.username,
            "role": user_role,
            "emp_id": emp_id
        })
    return JsonResponse({"error": "Not authenticated"}, status=401)