from django.db import models

class WorkLocation(models.Model):
    """Represents a deck/location that can be assigned to vessels"""
    deck_name = models.CharField(max_length=100, unique=True, verbose_name="Deck Name")
    risk_level = models.CharField(max_length=20, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM')

    class Meta:
        ordering = ['deck_name']
        verbose_name = "Deck Location"
        verbose_name_plural = "Deck Locations"

    def __str__(self):
        return self.deck_name

class POBLog(models.Model):
    ACTION_CHOICES = [
        ('IN', 'Check In'),
        ('OUT', 'Check Out'),
    ]

    emp_id = models.CharField(max_length=50, verbose_name="Employee ID")
    deck_location = models.ForeignKey('WorkLocation', on_delete=models.PROTECT, verbose_name="Deck Location")
    action = models.CharField(max_length=3, choices=ACTION_CHOICES, verbose_name="Action")
    # ptw field will be added in a later migration to avoid circular dependency
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "POB Log"
        verbose_name_plural = "POB Logs"

    def __str__(self):
        return f"{self.emp_id} - {self.deck_location} ({self.action})"

