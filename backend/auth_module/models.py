from django.db import models
from django.contrib.auth.models import User

# This module uses Django's built-in Groups for role management

class UserProfile(models.Model):
    """
    Extended user profile for HSE business data
    One-to-One relationship with Django User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Job Information
    job_role = models.CharField(max_length=100, default='Worker')

    # Roster Information
    roster_status = models.CharField(
        max_length=20,
        choices=[
            ('ONBOARD', 'On Board'),
            ('OFFBOARD', 'Off Board'),
        ],
        default='ONBOARD'
    )

    # Medical Information
    mcu_expiry = models.DateField(null=True, blank=True, verbose_name='MCU Expiry Date')
    mcu_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('FIT', 'Fit'),
            ('UNFIT', 'Unfit'),
            ('EXPIRED', 'Expired'),
        ],
        default='PENDING'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} - {self.job_role}"
