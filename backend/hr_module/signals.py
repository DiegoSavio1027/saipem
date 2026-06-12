import threading
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Employee

# Thread-local storage to prevent infinite loops during synchronization
_local = threading.local()

@receiver(post_save, sender=Employee)
def sync_employee_to_user(sender, instance, created, **kwargs):
    if getattr(_local, 'sync_in_progress', False):
        return

    _local.sync_in_progress = True
    try:
        # Split full_name into first_name and last_name
        names = instance.full_name.split(' ', 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        # Get or create User
        user, user_created = User.objects.get_or_create(
            username=instance.emp_id,
            defaults={
                'email': instance.email or '',
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True
            }
        )

        if user_created:
            # Set a default or provided password
            raw_password = getattr(instance, '_password', 'saipem123')
            user.set_password(raw_password)
            user.save()
        else:
            # Update existing User details
            user.email = instance.email or ''
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        # Map job_role to Group
        job_role_clean = instance.job_role.strip()
        role_mapping = {
            'System Administrator': 'Admin',
            'Admin': 'Admin',
            'HR Staff': 'HR Staff',
            'HR Manager': 'HR Staff',
            'Chief Engineer': 'Chief Engineer',
            'Engineering Chief': 'Chief Engineer',
            'Supervisor Engineer': 'Chief Engineer',
            'Engineering Supervisor': 'Chief Engineer',
            'Safety Officer': 'Safety Officer',
            'HSE Officer': 'Safety Officer',
            'Worker': 'Worker',
            'Field Worker': 'Worker',
            'Lead Welder': 'Worker',
            'Logistics Manager': 'HR Staff',
            'Deck Foreman': 'Worker',
            'Rig Manager': 'Chief Engineer',
            'Scaffolder': 'Worker'
        }
        mapped_role = role_mapping.get(job_role_clean, 'Worker')

        # Sync user groups
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=mapped_role)
        user.groups.add(group)

        # Superuser and staff flags for Admin
        if mapped_role == 'Admin':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        user.save()
    except Exception as e:
        print(f"Error syncing Employee to User: {e}")
    finally:
        _local.sync_in_progress = False


@receiver(post_save, sender=User)
def sync_user_to_employee(sender, instance, created, **kwargs):
    if getattr(_local, 'sync_in_progress', False):
        return

    _local.sync_in_progress = True
    try:
        # Determine job role from superuser status or groups
        role = 'Worker'
        if instance.is_superuser:
            role = 'Admin'
        elif instance.groups.exists():
            role = instance.groups.first().name

        full_name = f"{instance.first_name} {instance.last_name}".strip()
        if not full_name:
            full_name = instance.username

        # Get or create Employee
        employee, emp_created = Employee.objects.get_or_create(
            emp_id=instance.username,
            defaults={
                'full_name': full_name,
                'job_role': role,
                'email': instance.email or None,
                'roster_status': 'AVAILABLE',
                'mcu_status': 'FIT' if role == 'Admin' else 'PENDING'
            }
        )

        if not emp_created:
            # Update existing Employee
            updated = False
            if employee.full_name != full_name:
                employee.full_name = full_name
                updated = True
            if employee.job_role != role:
                employee.job_role = role
                updated = True
            if employee.email != (instance.email or None):
                employee.email = instance.email or None
                updated = True
            if updated:
                employee.save()
    except Exception as e:
        print(f"Error syncing User to Employee: {e}")
    finally:
        _local.sync_in_progress = False


@receiver(post_delete, sender=Employee)
def delete_linked_user(sender, instance, **kwargs):
    if getattr(_local, 'sync_in_progress', False):
        return

    _local.sync_in_progress = True
    try:
        User.objects.filter(username=instance.emp_id).delete()
    except Exception as e:
        print(f"Error deleting linked User: {e}")
    finally:
        _local.sync_in_progress = False


@receiver(post_delete, sender=User)
def delete_linked_employee(sender, instance, **kwargs):
    if getattr(_local, 'sync_in_progress', False):
        return

    _local.sync_in_progress = True
    try:
        Employee.objects.filter(emp_id=instance.username).delete()
    except Exception as e:
        print(f"Error deleting linked Employee: {e}")
    finally:
        _local.sync_in_progress = False
