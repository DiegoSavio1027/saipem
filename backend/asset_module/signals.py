from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WorkOrderMaterial

@receiver(post_save, sender=WorkOrderMaterial)
def reserve_spare_part_stock(sender, instance, created, **kwargs):
    """
    Auto-reserve spare part stock when a WorkOrderMaterial is added.
    """
    if created:
        spare_part = instance.spare_part
        spare_part.quantity_reserved += instance.quantity_used
        spare_part.save()

@receiver(post_delete, sender=WorkOrderMaterial)
def release_spare_part_stock(sender, instance, **kwargs):
    """
    Auto-release reserved spare part stock if a WorkOrderMaterial is deleted/removed from WO.
    """
    spare_part = instance.spare_part
    # Prevent negative reserved quantity just in case
    spare_part.quantity_reserved = max(0, spare_part.quantity_reserved - instance.quantity_used)
    spare_part.save()
