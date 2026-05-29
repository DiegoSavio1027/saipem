from django.db import models
from django.utils import timezone
from datetime import timedelta


class IncidentTrend(models.Model):
    """
    Aggregated incident statistics by time period
    Used for trend analysis and charts
    """
    PERIOD_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]

    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_start = models.DateField(help_text="Start date of the period")
    period_end = models.DateField(help_text="End date of the period")
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.PROTECT, null=True, blank=True, related_name='incident_trends')

    # Incident counts by severity
    safety_observation_count = models.IntegerField(default=0)
    near_miss_count = models.IntegerField(default=0)
    first_aid_count = models.IntegerField(default=0)
    lti_count = models.IntegerField(default=0)
    total_incidents = models.IntegerField(default=0)

    # Metrics
    days_without_lti = models.IntegerField(default=0)
    average_response_time = models.FloatField(null=True, blank=True, help_text="Average time to close incidents (hours)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hse_incident_trends'
        ordering = ['-period_start']
        unique_together = ['period_type', 'period_start', 'vessel']
        indexes = [
            models.Index(fields=['period_type', '-period_start']),
        ]

    def __str__(self):
        return f"{self.period_type} - {self.period_start} to {self.period_end}"


class SafetyMetrics(models.Model):
    """
    Historical safety performance metrics
    Calculated periodically for reporting
    """
    date = models.DateField(help_text="Date of metrics snapshot")
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.PROTECT, null=True, blank=True, related_name='safety_metrics')

    # Headcount metrics
    total_pob = models.IntegerField(default=0, help_text="Total persons on board")

    # PTW metrics
    total_ptw_issued = models.IntegerField(default=0)
    total_ptw_completed = models.IntegerField(default=0)
    total_ptw_rejected = models.IntegerField(default=0)
    average_ptw_duration = models.FloatField(null=True, blank=True, help_text="Average PTW duration (hours)")

    # Safety metrics
    days_without_lti = models.IntegerField(default=0)
    near_misses_count = models.IntegerField(default=0)
    total_incidents = models.IntegerField(default=0)

    # Calculated safety rates
    ltifr = models.FloatField(null=True, blank=True, help_text="Lost Time Injury Frequency Rate")
    trifr = models.FloatField(null=True, blank=True, help_text="Total Recordable Injury Frequency Rate")

    # System status
    global_status = models.CharField(max_length=10, default='GREEN')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hse_safety_metrics'
        ordering = ['-date']
        unique_together = ['date', 'vessel']
        indexes = [
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f"Safety Metrics - {self.date}"

    def calculate_ltifr(self, hours_worked=None):
        """
        Calculate LTIFR (Lost Time Injury Frequency Rate)
        LTIFR = (Number of LTIs × 1,000,000) / Total hours worked
        """
        if not hours_worked:
            # Assume 12-hour shifts, 7 days a week
            hours_worked = self.total_pob * 12 * 7

        if hours_worked > 0:
            from ..hse_safety.models import Incident
            lti_count = Incident.objects.filter(
                severity='LTI',
                incident_date__date=self.date
            ).count()
            self.ltifr = (lti_count * 1000000) / hours_worked
        return self.ltifr


class ComplianceReport(models.Model):
    """
    ISO 45001 compliance tracking and audit reports
    """
    REPORT_TYPE_CHOICES = [
        ('DAILY', 'Daily Compliance Check'),
        ('WEEKLY', 'Weekly Audit'),
        ('MONTHLY', 'Monthly Review'),
        ('QUARTERLY', 'Quarterly Assessment'),
        ('ANNUAL', 'Annual Audit'),
    ]

    STATUS_CHOICES = [
        ('COMPLIANT', 'Fully Compliant'),
        ('PARTIAL', 'Partially Compliant'),
        ('NON_COMPLIANT', 'Non-Compliant'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    report_date = models.DateField(default=timezone.now)
    period_start = models.DateField()
    period_end = models.DateField()
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.PROTECT, null=True, blank=True, related_name='compliance_reports')

    # Compliance status
    overall_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLIANT')
    compliance_score = models.FloatField(help_text="Compliance percentage (0-100)")

    # Audit findings
    total_checks = models.IntegerField(default=0)
    passed_checks = models.IntegerField(default=0)
    failed_checks = models.IntegerField(default=0)

    # Details
    findings = models.TextField(blank=True, help_text="Audit findings and observations")
    recommendations = models.TextField(blank=True, help_text="Recommendations for improvement")

    # Auditor info
    auditor_name = models.CharField(max_length=100)
    auditor_emp_id = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hse_compliance_reports'
        ordering = ['-report_date']
        indexes = [
            models.Index(fields=['report_type', '-report_date']),
        ]

    def __str__(self):
        return f"{self.report_type} - {self.report_date} ({self.overall_status})"

    def calculate_compliance_score(self):
        """Calculate compliance percentage"""
        if self.total_checks > 0:
            self.compliance_score = (self.passed_checks / self.total_checks) * 100
        else:
            self.compliance_score = 0
        return self.compliance_score


class LocationStatistics(models.Model):
    """
    Statistics by work location for hotspot analysis
    """
    location_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.PROTECT, null=True, blank=True, related_name='location_statistics')

    # Activity metrics
    total_check_ins = models.IntegerField(default=0)
    total_check_outs = models.IntegerField(default=0)
    average_occupancy = models.FloatField(default=0, help_text="Average personnel count")
    peak_occupancy = models.IntegerField(default=0)

    # Safety metrics
    total_incidents = models.IntegerField(default=0)
    total_ptw_issued = models.IntegerField(default=0)

    # Risk level
    risk_score = models.FloatField(default=0, help_text="Calculated risk score (0-100)")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hse_location_statistics'
        ordering = ['-date', 'location_name']
        unique_together = ['location_name', 'date', 'vessel']
        indexes = [
            models.Index(fields=['location_name', '-date']),
        ]

    def __str__(self):
        return f"{self.location_name} - {self.date}"

    def calculate_risk_score(self):
        """
        Calculate risk score based on incidents and activity
        Higher incidents + higher occupancy = higher risk
        """
        incident_weight = 40
        occupancy_weight = 30
        ptw_weight = 30

        # Normalize values (assuming max values)
        incident_score = min((self.total_incidents / 10) * incident_weight, incident_weight)
        occupancy_score = min((self.average_occupancy / 50) * occupancy_weight, occupancy_weight)
        ptw_score = min((self.total_ptw_issued / 20) * ptw_weight, ptw_weight)

        self.risk_score = incident_score + occupancy_score + ptw_score
        return self.risk_score
