from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PermitToWork

@receiver(pre_save, sender=PermitToWork)
def ptw_status_change_handler(sender, instance, **kwargs):
    """
    Handle Spare Part reserved stock and physical stock deduction when PTW status changes.
    """
    if not instance.pk:
        return  # New instance, no status change yet

    try:
        old_instance = PermitToWork.objects.get(pk=instance.pk)
    except PermitToWork.DoesNotExist:
        return

    # Check if status changed
    if old_instance.status != instance.status:
        # If PTW is CLOSED, deduct physical stock and release reserved stock
        if instance.status == 'CLOSED' and old_instance.status != 'CLOSED':
            if instance.wo_id:
                materials = instance.wo_id.materials.all()
                for material in materials:
                    spare_part = material.spare_part
                    # Deduct physical stock
                    spare_part.quantity_on_hand = max(0, spare_part.quantity_on_hand - material.quantity_used)
                    # Release the reserved stock
                    spare_part.quantity_reserved = max(0, spare_part.quantity_reserved - material.quantity_used)
                    spare_part.save()

        # If PTW is REJECTED, just release the reserved stock, don't deduct physical stock
        elif instance.status == 'REJECTED' and old_instance.status != 'REJECTED':
            if instance.wo_id:
                materials = instance.wo_id.materials.all()
                for material in materials:
                    spare_part = material.spare_part
                    # Only release reserved stock, physical stock remains
                    spare_part.quantity_reserved = max(0, spare_part.quantity_reserved - material.quantity_used)
                    spare_part.save()
