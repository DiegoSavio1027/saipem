from django.contrib import admin
from .models import Employee, PermitToWork


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'full_name', 'job_role', 'roster_status', 'created_at']
    list_filter = ['roster_status', 'job_role']
    search_fields = ['emp_id', 'full_name', 'job_role']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(PermitToWork)
class PermitToWorkAdmin(admin.ModelAdmin):
    list_display = ['permit_id', 'emp_id', 'wo_id', 'permit_type', 'status', 'created_at']
    list_filter = ['status', 'permit_type', 'created_at']
    search_fields = ['permit_id', 'emp_id', 'wo_id']
    ordering = ['-created_at']
    readonly_fields = ['permit_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('permit_id', 'emp_id', 'wo_id', 'permit_type', 'status')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_at', 'signature'),
            'classes': ('collapse',)
        }),
        ('Rejection', {
            'fields': ('rejected_by', 'rejected_at', 'rejection_reason'),
            'classes': ('collapse',)
        }),
        ('Completion & Closing', {
            'fields': ('completion_notes', 'closed_by', 'closed_at', 'closing_notes'),
            'classes': ('collapse',)
        }),
        ('Audit Trail', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
