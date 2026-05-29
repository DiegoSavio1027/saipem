from django.contrib import admin
from .models import Incident, StatusOverride, SystemStatus


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'severity',
        'location',
        'employee_name',
        'reported_by',
        'incident_date',
        'status',
        'created_at'
    ]
    list_filter = ['severity', 'location', 'status', 'incident_date']
    search_fields = ['description', 'employee_name', 'reported_by']
    date_hierarchy = 'incident_date'
    ordering = ['-incident_date']

    fieldsets = (
        ('Incident Information', {
            'fields': ('severity', 'location', 'description', 'incident_date')
        }),
        ('People Involved', {
            'fields': ('employee_name', 'reported_by')
        }),
        ('Status', {
            'fields': ('status', 'investigation_notes', 'closed_by', 'closed_date')
        }),
        ('Timestamps', {
            'fields': ('reported_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['reported_date', 'created_at', 'updated_at']


@admin.register(StatusOverride)
class StatusOverrideAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'previous_status',
        'new_status',
        'changed_by',
        'created_at'
    ]
    list_filter = ['previous_status', 'new_status', 'created_at']
    search_fields = ['override_reason', 'changed_by']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    readonly_fields = ['created_at']


@admin.register(SystemStatus)
class SystemStatusAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'global_status',
        'days_without_lti',
        'last_lti_date',
        'near_misses_count',
        'active_permits',
        'updated_at'
    ]

    fieldsets = (
        ('Current Status', {
            'fields': ('global_status',)
        }),
        ('Metrics', {
            'fields': (
                'days_without_lti',
                'last_lti_date',
                'near_misses_count',
                'active_permits'
            )
        }),
        ('Timestamps', {
            'fields': ('updated_at', 'last_incident_date')
        }),
    )

    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Only allow one SystemStatus instance
        return not SystemStatus.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SystemStatus
        return False
