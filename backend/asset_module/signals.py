from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WorkOrderMaterial

@receiver(post_save, sender=WorkOrderMaterial)
def deduct_spare_part_stock(sender, instance, created, **kwargs):
    """
    Auto-deduct spare part stock when a WorkOrderMaterial is added.
    """
    if created:
        spare_part = instance.spare_part
        spare_part.quantity_on_hand -= instance.quantity_used
        spare_part.save()

@receiver(post_delete, sender=WorkOrderMaterial)
def restock_spare_part_stock(sender, instance, **kwargs):
    """
    Auto-restock spare part stock if a WorkOrderMaterial is deleted/removed from WO.
    """
    spare_part = instance.spare_part
    spare_part.quantity_on_hand += instance.quantity_used
    spare_part.save()
