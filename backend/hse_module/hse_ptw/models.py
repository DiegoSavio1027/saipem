from django.db import models

# ============================================================================
# EMPLOYEE MODEL (untuk linking dengan User)
# ============================================================================

class Employee(models.Model):
    """Employee data - linked to Django User"""
    ROSTER_STATUS_CHOICES = [
        ('ONBOARD', 'On Board'),
        ('OFFBOARD', 'Off Board'),
    ]

    emp_id = models.CharField(max_length=50, unique=True, primary_key=True)
    full_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    roster_status = models.CharField(max_length=50, choices=ROSTER_STATUS_CHOICES)
    email = models.EmailField(unique=True, null=True, blank=True)  # ← Add
    mcu_expiry = models.DateField(null=True, blank=True)           # ← Add
    mcu_status = models.CharField(max_length=50, default="PENDING") # ← Add
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emp_id} - {self.full_name}"


# ============================================================================
# PERMIT TO WORK MODEL (UPDATED STRUCTURE)
# ============================================================================

class PermitToWork(models.Model):
    """Permit to Work - Updated structure"""
    PERMIT_TYPE_CHOICES = [
        ('HOT_WORK', 'Hot Work Permit'),
        ('CONFINED_SPACE', 'Confined Space Entry Permit'),
        ('WORKING_AT_HEIGHT', 'Working at Height Permit'),
        ('ISOLATION', 'Isolation Certificate'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved (Active)'),
        ('WAITING_FOR_CLOSE', 'Waiting for Close'),
        ('CLOSED', 'Closed'),
        ('REJECTED', 'Rejected'),
    ]

    # Basic Information
    permit_id = models.CharField(max_length=20, unique=True, help_text="Format: HW-270526-0001")
    vessel = models.ForeignKey('asset_module.Vessel', on_delete=models.PROTECT, related_name='ptws')
    emp_id = models.CharField(max_length=50, verbose_name="Employee ID")
    wo_id = models.ForeignKey('asset_module.WorkOrder', on_delete=models.PROTECT, verbose_name="Work Order", related_name='ptws')
    deck_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Work Location")
    permit_type = models.CharField(max_length=50, choices=PERMIT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Approval
    approved_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Safety Officer")
    approved_at = models.DateTimeField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True, help_text="Digital signature base64")

    # Rejection
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)

    # Completion
    completion_notes = models.TextField(blank=True, null=True)

    # Closing
    closed_by = models.CharField(max_length=100, blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    closing_notes = models.TextField(blank=True, null=True)

    # Audit Trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.permit_id} | {self.get_permit_type_display()} - {self.status}"

    @staticmethod
    def get_permit_type_code(permit_type):
        """Map permit type to code"""
        type_codes = {
            'HOT_WORK': 'HW',
            'CONFINED_SPACE': 'CSE',
            'ISOLATION': 'IC',
            'WORKING_AT_HEIGHT': 'WAH',
        }
        return type_codes.get(permit_type, 'PTW')

    @classmethod
    def generate_next_permit_id(cls, permit_type):
        """Generate permit ID: {TYPE}-{DDMMYY}-{SEQUENCE}"""
        from datetime import datetime

        type_code = cls.get_permit_type_code(permit_type)
        today = datetime.now().strftime('%d%m%y')

        # Find last permit with same type and date
        last_ptw = cls.objects.filter(
            permit_type=permit_type,
            created_at__date=datetime.now().date()
        ).order_by('-id').first()

        if not last_ptw:
            sequence = 1
        else:
            try:
                # Extract sequence from last permit ID (format: TYPE-DDMMYY-SEQUENCE)
                parts = last_ptw.permit_id.split('-')
                if len(parts) >= 3:
                    sequence = int(parts[-1]) + 1
                else:
                    sequence = 1
            except (ValueError, IndexError):
                sequence = 1

        return f"{type_code}-{today}-{str(sequence).zfill(4)}"

    def save(self, *args, **kwargs):
        """Auto-generate permit_id if not provided"""
        if not self.permit_id:
            self.permit_id = self.generate_next_permit_id(self.permit_type)
        super().save(*args, **kwargs)
