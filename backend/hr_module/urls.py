from django.urls import path
from . import views

urlpatterns = [
    # --- Employee / Crew API ---
    path('employees/', views.get_all_employees, name='get_all_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/delete/<str:emp_id>/', views.delete_employee, name='delete_employee'),
    path('employees/toggle/<str:emp_id>/', views.toggle_roster_status, name='toggle_roster_status'),
    path('employees/update/<str:emp_id>/', views.update_employee, name='update_employee'),

    # --- Roster Matrix API ---
    path('rosters/', views.roster_list, name='roster_list'),
    path('rosters/delete/<int:pk>/', views.delete_roster, name='delete_roster'),

    # --- Vessel Activity API ---
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/delete/<int:pk>/', views.delete_activity, name='delete_activity'),

    # --- Automated Payroll API ---
    path('payroll/', views.payroll_calculation, name='payroll_calculation'),

    # --- Tactical Dashboard Analytics API ---
    path('analytics/', views.dashboard_analytics, name='dashboard_analytics'),

    # --- Position Master Rates API ---
    path('positions/', views.position_list, name='position_list'),
    path('positions/delete/<int:pk>/', views.delete_position, name='delete_position'),

    # --- Certification Management API ---
    path('certifications/<str:emp_id>/', views.certification_list, name='certification_list'),
    path('certifications/add/<str:emp_id>/', views.add_certification, name='add_certification'),
    path('certifications/delete/<str:cert_id>/', views.delete_certification, name='delete_certification'),
]