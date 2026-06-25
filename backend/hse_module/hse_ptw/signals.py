from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PermitToWork

@receiver(pre_save, sender=PermitToWork)
def ptw_status_change_handler(sender, instance, **kwargs):
    """
    Status change side effects handled in views instead of signals to prevent double-deduction.
    """
    pass
