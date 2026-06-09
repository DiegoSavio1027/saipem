from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Asset,
    MachineryEquipment,
    SparePart,
    WorkOrder,
    MaintenanceTask,
    InventoryItem
)
from .serializers import (
    AssetSerializer,
    MachineryEquipmentSerializer,
    SparePartSerializer,
    WorkOrderSerializer,
    MaintenanceTaskSerializer,
    InventoryItemSerializer
)


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
@api_view(['GET', 'POST'])
def sparepart_list(request):
    """Get all spare parts or create new spare part"""
    if request.method == 'GET':
        spareparts = SparePart.objects.all()
        serializer = SparePartSerializer(spareparts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SparePartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def sparepart_detail(request, pk):
    """Get, update, or delete specific spare part"""
    try:
        sparepart = SparePart.objects.get(pk=pk)
    except SparePart.DoesNotExist:
        return Response({"error": "Spare part not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SparePartSerializer(sparepart)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = SparePartSerializer(sparepart, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sparepart.delete()
        return Response({"message": "Spare part deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 5. WORK ORDER API
# ==========================================
@api_view(['GET', 'POST'])
def workorder_list(request):
    """Get all work orders or create new work order"""
    if request.method == 'GET':
        vessel_id = request.query_params.get('vessel_id')
        if vessel_id:
            workorders = WorkOrder.objects.filter(vessel_id=vessel_id)
        else:
            workorders = WorkOrder.objects.all()
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
        serializer = WorkOrderSerializer(workorder, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        workorder.delete()
        return Response({"message": "Work order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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
        items = InventoryItem.objects.all()
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
