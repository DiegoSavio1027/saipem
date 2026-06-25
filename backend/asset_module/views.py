from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import (
    Asset,
    MachineryEquipment,
    WorkOrder,
    MaintenanceTask,
    InventoryItem
)
from .serializers import (
    AssetSerializer,
    MachineryEquipmentSerializer,
    WorkOrderSerializer,
    MaintenanceTaskSerializer,
    InventoryItemSerializer
)
from .models import TelemetryLog


# ==========================================
# 1. ASSET API
# ==========================================
@api_view(['GET', 'POST'])
def asset_list(request):
    """Get all assets or create new asset"""
    if request.method == 'GET':
        vessel_id = request.query_params.get('vessel_id')
        if vessel_id:
            assets = Asset.objects.filter(vessel_id=vessel_id)
        else:
            assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def asset_detail(request, asset_id):
    """Get, update, or delete a specific asset"""
    try:
        asset = Asset.objects.get(asset_id=asset_id)
    except Asset.DoesNotExist:
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = AssetSerializer(asset, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        asset.delete()
        return Response({"message": "Asset deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 2. TELEMETRY API
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def telemetry_history(request):
    """Fetch historical telemetry logs for an asset or machinery"""
    asset_id = request.query_params.get('asset_id')
    machinery_id = request.query_params.get('machinery_id')
    limit = int(request.query_params.get('limit', 50))
    
    logs = TelemetryLog.objects.all()
    if asset_id:
        logs = logs.filter(asset_id=asset_id)
    elif machinery_id:
        logs = logs.filter(machinery_id=machinery_id)
    else:
        return Response({"error": "Provide asset_id or machinery_id"}, status=status.HTTP_400_BAD_REQUEST)
        
    logs = logs[:limit]
    
    data = []
    for log in reversed(logs): # return chronological order for charts
        data.append({
            'timestamp': log.timestamp.isoformat(),
            'vibration': float(log.vibration),
            'temperature': float(log.temperature)
        })
        
    return Response(data)



# ==========================================
# 3. MACHINERY EQUIPMENT API
# ==========================================
@api_view(['GET', 'POST'])
def machinery_list(request):
    """Get all machinery equipment or create new equipment"""
    if request.method == 'GET':
        vessel_id = request.query_params.get('vessel_id')
        if vessel_id:
            machinery = MachineryEquipment.objects.filter(vessel_id=vessel_id)
        else:
            machinery = MachineryEquipment.objects.all()
        serializer = MachineryEquipmentSerializer(machinery, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MachineryEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def machinery_detail(request, pk):
    """Get, update, or delete specific machinery equipment"""
    try:
        machinery = MachineryEquipment.objects.get(pk=pk)
    except MachineryEquipment.DoesNotExist:
        return Response({"error": "Machinery equipment not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MachineryEquipmentSerializer(machinery)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = MachineryEquipmentSerializer(machinery, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        machinery.delete()
        return Response({"message": "Machinery equipment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 4. SPARE PART API
# ==========================================



# ==========================================
# 5. WORK ORDER API
# ==========================================
@api_view(['GET', 'POST'])
def workorder_list(request):
    """Get all work orders or create new work order"""
    if request.method == 'GET':
        vessel_id = request.query_params.get('vessel_id')
        assigned_to = request.query_params.get('assigned_to')
        
        workorders = WorkOrder.objects.all()
        
        if vessel_id:
            workorders = workorders.filter(vessel_id=vessel_id)
        if assigned_to:
            workorders = workorders.filter(assigned_to_id=assigned_to)
        serializer = WorkOrderSerializer(workorders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def workorder_detail(request, wo_id):
    """Get, update, or delete specific work order"""
    try:
        workorder = WorkOrder.objects.get(wo_id=wo_id)
    except WorkOrder.DoesNotExist:
        return Response({"error": "Work order not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WorkOrderSerializer(workorder)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        
        # Check if status is changing
        old_status = workorder.status
        new_status = request.data.get('status', old_status)
        
        serializer = WorkOrderSerializer(workorder, data=request.data, partial=partial)
        if serializer.is_valid():
            # If changing to COMPLETED, deduct stock
            if old_status != 'COMPLETED' and new_status == 'COMPLETED':
                for material in workorder.materials.all():
                    inv_item = material.inventory_item
                    inv_item.current_stock -= material.quantity_used
                    inv_item.quantity_reserved -= material.quantity_used
                    # Ensure stock doesn't go below 0 just in case
                    if inv_item.current_stock < 0:
                        inv_item.current_stock = 0
                    if inv_item.quantity_reserved < 0:
                        inv_item.quantity_reserved = 0
                    inv_item.save()
            
            # If changing to CANCELLED, free reserved stock
            elif old_status != 'CANCELLED' and new_status == 'CANCELLED':
                for material in workorder.materials.all():
                    inv_item = material.inventory_item
                    inv_item.quantity_reserved -= material.quantity_used
                    if inv_item.quantity_reserved < 0:
                        inv_item.quantity_reserved = 0
                    inv_item.save()
                    
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        workorder.delete()
        return Response({"message": "Work order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def workorder_add_material(request, wo_id):
    """Add spare part material to a work order"""
    try:
        workorder = WorkOrder.objects.get(wo_id=wo_id)
    except WorkOrder.DoesNotExist:
        return Response({"error": "Work order not found"}, status=status.HTTP_404_NOT_FOUND)
        
    inventory_item_id = request.data.get('spare_part_id') # keeping variable name from frontend for compatibility
    quantity = int(request.data.get('quantity_used', 1))
    
    try:
        inventory_item = InventoryItem.objects.get(pk=inventory_item_id)
    except InventoryItem.DoesNotExist:
        return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)
        
    if inventory_item.available_stock < quantity:
        return Response({"error": f"Insufficient stock. Only {inventory_item.available_stock} available."}, status=status.HTTP_400_BAD_REQUEST)
        
    from .models import WorkOrderMaterial
    material = WorkOrderMaterial.objects.create(
        work_order=workorder,
        inventory_item=inventory_item,
        quantity_used=quantity
    )
    
    # Reserve the stock immediately
    inventory_item.quantity_reserved += quantity
    inventory_item.save()
    
    serializer = WorkOrderSerializer(workorder)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==========================================
# 6. MAINTENANCE TASK API
# ==========================================
@api_view(['GET', 'POST'])
def maintenance_list(request):
    """Get all maintenance tasks or create new task"""
    if request.method == 'GET':
        tasks = MaintenanceTask.objects.all()
        serializer = MaintenanceTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MaintenanceTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def maintenance_detail(request, task_id):
    """Get, update, or delete specific maintenance task"""
    try:
        task = MaintenanceTask.objects.get(task_id=task_id)
    except MaintenanceTask.DoesNotExist:
        return Response({"error": "Maintenance task not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MaintenanceTaskSerializer(task)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = MaintenanceTaskSerializer(task, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({"message": "Maintenance task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 7. INVENTORY ITEM API
# ==========================================
@api_view(['GET', 'POST'])
def inventory_list(request):
    """Get all inventory items or create new item"""
    if request.method == 'GET':
        vessel_id = request.query_params.get('vessel_id')
        items = InventoryItem.objects.all()
        if vessel_id:
            items = items.filter(asset_location__vessel_id=vessel_id)
        serializer = InventoryItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def inventory_detail(request, item_code):
    """Get, update, or delete specific inventory item"""
    try:
        item = InventoryItem.objects.get(item_code=item_code)
    except InventoryItem.DoesNotExist:
        return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InventoryItemSerializer(item)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = InventoryItemSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response({"message": "Inventory item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
