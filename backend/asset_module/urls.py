from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # ASSET ENDPOINTS
    # ==========================================
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<str:asset_id>/', views.asset_detail, name='asset_detail'),

    # ==========================================
    # MACHINERY EQUIPMENT ENDPOINTS
    # ==========================================
    path('machinery/', views.machinery_list, name='machinery_list'),
    path('machinery/<int:pk>/', views.machinery_detail, name='machinery_detail'),

    # ==========================================
    # SPARE PART ENDPOINTS
    # ==========================================
    path('spareparts/', views.sparepart_list, name='sparepart_list'),
    path('spareparts/<int:pk>/', views.sparepart_detail, name='sparepart_detail'),

    # ==========================================
    # WORK ORDER ENDPOINTS
    # ==========================================
    path('workorders/', views.workorder_list, name='workorder_list'),
    path('workorders/<str:wo_id>/', views.workorder_detail, name='workorder_detail'),
    path('workorders/<str:wo_id>/add_material/', views.workorder_add_material, name='workorder_add_material'),

    # ==========================================
    # MAINTENANCE TASK ENDPOINTS
    # ==========================================
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<str:task_id>/', views.maintenance_detail, name='maintenance_detail'),

    # ==========================================
    # INVENTORY ITEM ENDPOINTS
    # ==========================================
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<str:item_code>/', views.inventory_detail, name='inventory_detail'),
]
