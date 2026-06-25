from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ..hse_pob.models import WorkLocation

class Incident(models.Model):
    """
    Model to record all incidents/safety reports
    Path 1: Bottom-Up from field
    """

    SEVERITY_CHOICES = [
        ('SAFETY_OBSERVATION', 'Safety Observation'),
        ('NEAR_MISS', 'Near Miss'),
        ('FIRST_AID', 'First Aid / Minor Injury'),
        ('LTI', 'LTI / Major Injury'),
    ]

    STATUS_CHOICES = [
        ('PENDING_VERIFICATION', 'Pending Verification'),
        ('OPEN', 'Open'),
        ('INVESTIGATING', 'Investigating'),
        ('CLOSED', 'Closed'),
        ('REJECTED', 'Rejected'),
    ]

    # Basic Info
    id = models.AutoField(primary_key=True)
    incident_id = models.CharField(max_length=50, unique=True, null=True, blank=True, editable=False, help_text="Auto-generated incident ID based on severity")
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        help_text="Incident severity level - KEY for metrics update"
    )
    location = models.ForeignKey(
        WorkLocation,
        on_delete=models.PROTECT,
        related_name='incidents',
        help_text="Work location where incident occurred"
    )
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.PROTECT, null=True, blank=True, related_name='incidents')
    description = models.TextField(help_text="Detailed incident description")
    proof_image = models.ImageField(
        upload_to='incident_proofs/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Incident proof image"
    )

    # People Involved
    employee_name = models.CharField(max_length=100, blank=True, null=True)
    reported_by = models.CharField(max_length=50)  # EMP ID

    # Timestamps
    incident_date = models.DateTimeField(help_text="When incident occurred")
    reported_date = models.DateTimeField(auto_now_add=True, help_text="When reported")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN'
    )

    # Audit
    investigation_notes = models.TextField(blank=True, null=True)
    closed_by = models.CharField(max_length=50, blank=True, null=True)
    closed_date = models.DateTimeField(blank=True, null=True)

    # Verification (for worker-reported incidents)
    verified_by = models.CharField(max_length=50, blank=True, null=True, help_text="EMP ID of verifier")
    verified_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason if rejected")

    class Meta:
        db_table = 'hse_incidents'
        ordering = ['-incident_date']
        indexes = [
            models.Index(fields=['severity', '-incident_date']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_severity_display()} - {self.location.deck_name} ({self.incident_date.strftime('%Y-%m-%d')})"

    def save(self, *args, **kwargs):
        if not self.incident_id:
            severity_prefix = self.severity
            count = Incident.objects.filter(severity=self.severity).count() + 1
            self.incident_id = f"{severity_prefix}-{count:03d}"
        super().save(*args, **kwargs)

    def get_impact_on_metrics(self):
        """
        Return impact of incident on metrics
        Used for automatic dashboard update
        """
        if self.severity == 'SAFETY_OBSERVATION':
            return {
                'days_without_lti': 'NO_CHANGE',
                'near_misses': 'NO_CHANGE',
                'global_status': 'NO_CHANGE',
                'description': 'Safety observation logged'
            }
        elif self.severity == 'NEAR_MISS':
            return {
                'days_without_lti': 'NO_CHANGE',
                'near_misses': 'INCREMENT',
                'global_status': 'NO_CHANGE',
                'description': 'Near miss recorded, Days Without LTI continues'
            }
        elif self.severity == 'FIRST_AID':
            return {
                'days_without_lti': 'NO_CHANGE',
                'near_misses': 'NO_CHANGE',
                'global_status': 'YELLOW',
                'description': 'Minor injury reported, status to YELLOW'
            }
        elif self.severity == 'LTI':
            return {
                'days_without_lti': 'RESET_TO_ZERO',
                'near_misses': 'NO_CHANGE',
                'global_status': 'RED',
                'description': 'MAJOR INJURY! Days Without LTI reset to 0, Status to RED, EMERGENCY MODE'
            }


class StatusOverride(models.Model):
    """
    Model to record manual status override
    Path 2: Top-Down from Command Center
    Audit trail for compliance
    """

    STATUS_CHOICES = [
        ('GREEN', 'Condition Green - All Safe'),
        ('YELLOW', 'Condition Yellow - Warning'),
        ('RED', 'Condition Red - Emergency'),
    ]

    id = models.AutoField(primary_key=True)
    previous_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    override_reason = models.TextField(help_text="Reason for manual override")
    changed_by = models.CharField(max_length=50, help_text="EMP ID of Safety Officer")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hse_status_overrides'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.previous_status} → {self.new_status} by {self.changed_by}"


class SystemStatus(models.Model):
    """
    Model to store current HSE system state
    Single record that is always updated
    """

    STATUS_CHOICES = [
        ('GREEN', 'Condition Green'),
        ('YELLOW', 'Condition Yellow'),
        ('RED', 'Condition Red'),
    ]

    id = models.AutoField(primary_key=True)

    # Current Metrics
    global_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='GREEN'
    )
    days_without_lti = models.IntegerField(default=0)
    last_lti_date = models.DateField(blank=True, null=True)
    near_misses_count = models.IntegerField(default=0)
    active_permits = models.IntegerField(default=0)

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    last_incident_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'hse_system_status'

    def __str__(self):
        return f"System Status: {self.global_status} | Days Without LTI: {self.days_without_lti}"

    @classmethod
    def get_or_create_singleton(cls):
        """Get or create single instance"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj, created

    def calculate_days_without_lti(self):
        """Hitung days without LTI dari last_lti_date"""
        if self.last_lti_date:
            days = (timezone.now().date() - self.last_lti_date).days
            self.days_without_lti = days
            return days
        return self.days_without_lti

    def update_global_status(self):
        """
        Auto-calculate global status berdasarkan metrics
        Logic untuk determine GREEN/YELLOW/RED
        """
        # RED: Jika ada LTI baru (days < 1) atau status di-override ke RED
        if self.days_without_lti == 0:
            self.global_status = 'RED'
            return

        # YELLOW: Jika days < 30 atau near misses tinggi
        if self.days_without_lti < 30 or self.near_misses_count > 5:
            self.global_status = 'YELLOW'
            return

        # GREEN: Semua aman
        self.global_status = 'GREEN'
