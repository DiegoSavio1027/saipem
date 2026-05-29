from django.contrib import admin
from .models import Certification, Roster, VesselActivity, Position

class RosterAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'vessel')

class VesselActivityAdmin(admin.ModelAdmin):
    list_display = ('vessel', 'start_date', 'end_date', 'activity_name')

admin.site.register(Certification)
admin.site.register(Roster, RosterAdmin)
admin.site.register(VesselActivity, VesselActivityAdmin)
admin.site.register(Position)