from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # ASSET ENDPOINTS
    # ==========================================
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<str:asset_id>/', views.asset_detail, name='asset_detail'),

    # ==========================================
    # TELEMETRY ENDPOINTS
    # ==========================================
    path('telemetry/history/', views.telemetry_history, name='telemetry_history'),

    # ==========================================
    # MACHINERY EQUIPMENT ENDPOINTS
    # ==========================================
    path('machinery/', views.machinery_list, name='machinery_list'),
    path('machinery/<int:pk>/', views.machinery_detail, name='machinery_detail'),


    # ==========================================
    # WORK ORDER ENDPOINTS
    # ==========================================
    path('workorders/', views.workorder_list, name='workorder_list'),
    path('workorders/<str:wo_id>/', views.workorder_detail, name='workorder_detail'),
    path('workorders/<str:wo_id>/add_material/', views.workorder_add_material, name='workorder_add_material'),
    path('workorders/<str:wo_id>/complete/', views.complete_work_order, name='complete_work_order'),

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
