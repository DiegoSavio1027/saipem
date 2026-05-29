from django.db import models

# ==========================================
# POSITION MODEL (Master Posisi & Rate Gaji)
# ==========================================
class Position(models.Model):
    """Job positions with salary rates"""
    title = models.CharField(max_length=100, unique=True)  # ex: Welder, Crane Operator, HSE Officer
    discipline = models.CharField(max_length=100, default="Marine")  # ex: Marine, Drilling, Safety
    daily_rate = models.IntegerField(default=500000)  # Gaji pokok harian
    allowance_rate = models.IntegerField(default=300000)  # Tunjangan harian

    def __str__(self):
        return f"{self.title} ({self.discipline})"


# ==========================================
# CERTIFICATION MODEL
# ==========================================
class Certification(models.Model):
    """Employee certifications with expiry tracking"""
    cert_id = models.CharField(max_length=50, primary_key=True)
    cert_type = models.CharField(max_length=100)
    employee = models.ForeignKey('hse_ptw.Employee', on_delete=models.CASCADE, related_name='certifications')
    expiry_date = models.DateField()

    def __str__(self):
        return self.cert_id


# ==========================================
# ROSTER MODEL
# ==========================================
class Roster(models.Model):
    """Employee roster schedule"""
    employee = models.ForeignKey('hse_ptw.Employee', on_delete=models.CASCADE, related_name='rosters')
    start_date = models.DateField()
    end_date = models.DateField()
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.CASCADE, related_name='rosters', null=True, blank=True)
    location = models.CharField(max_length=100, default="Offshore Rig A")

    def __str__(self):
        return f"{self.employee.full_name} on {self.vessel.vessel_name if self.vessel else self.location}"


# ==========================================
# VESSEL ACTIVITY MODEL
# ==========================================
class VesselActivity(models.Model):
    """Vessel activity schedule"""
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    activity_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vessel.vessel_name} - {self.start_date} to {self.end_date}: {self.activity_name}"
