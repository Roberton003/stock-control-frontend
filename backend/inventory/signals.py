import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Category, Supplier, Location, Reagent, StockLot, StockMovement, Attachment, Requisition, AuditLog
from .utils import CustomJsonEncoder # Import the custom encoder

User = get_user_model()

@receiver(post_save, sender=Category)
@receiver(post_save, sender=Supplier)
@receiver(post_save, sender=Location)
@receiver(post_save, sender=Reagent)
@receiver(post_save, sender=StockLot)
@receiver(post_save, sender=StockMovement)
@receiver(post_save, sender=Attachment)
@receiver(post_save, sender=Requisition)
@receiver(post_save, sender=User)
def log_model_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    
    # Sanitize instance data for JSON serialization
    instance_data = instance.__dict__.copy()
    if '_state' in instance_data:
        del instance_data['_state']
    
    details = {
        'model': sender.__name__,
        'id': instance.pk,
        'data': instance_data
    }
    user = None # Placeholder
    AuditLog.objects.create(user=user, action=f'{action}_{sender.__name__.upper()}', details=details)

@receiver(post_delete, sender=Category)
@receiver(post_delete, sender=Supplier)
@receiver(post_delete, sender=Location)
@receiver(post_delete, sender=Reagent)
@receiver(post_delete, sender=StockLot)
@receiver(post_delete, sender=StockMovement)
@receiver(post_delete, sender=Attachment)
@receiver(post_delete, sender=Requisition)
@receiver(post_delete, sender=User)
def log_model_delete(sender, instance, **kwargs):
    action = 'DELETE'
    
    # Sanitize instance data for JSON serialization
    instance_data = instance.__dict__.copy()
    if '_state' in instance_data:
        del instance_data['_state']

    details = {
        'model': sender.__name__,
        'id': instance.pk,
        'data': instance_data
    }
    user = None # Placeholder
    AuditLog.objects.create(user=user, action=f'{action}_{sender.__name__.upper()}', details=details)

# Additional signals for critical actions
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Requisition

@receiver(post_save, sender=Requisition)
def log_requisition_status_change(sender, instance, created, **kwargs):
    """
    Log when a requisition status changes.
    """
    if not created:  # Only for updates
        # Check if status has changed by comparing with database value
        try:
            old_instance = Requisition.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                details = {
                    'model': 'Requisition',
                    'id': instance.pk,
                    'old_status': old_instance.status,
                    'new_status': instance.status,
                    'reagent': instance.reagent.name if instance.reagent else None,
                    'requester': instance.requester.username if instance.requester else None,
                    'approver': instance.approver.username if instance.approver else None
                }
                user = None  # Placeholder for now
                AuditLog.objects.create(
                    user=user, 
                    action='UPDATE_REQUISITION_STATUS', 
                    details=details
                )
        except Requisition.DoesNotExist:
            pass  # Object was just created, no status change to log

@receiver(post_save, sender=StockMovement)
def log_stock_movement_details(sender, instance, created, **kwargs):
    """
    Log detailed information about stock movements.
    """
    if created:
        details = {
            'model': 'StockMovement',
            'id': instance.pk,
            'reagent': instance.stock_lot.reagent.name if instance.stock_lot and instance.stock_lot.reagent else None,
            'lot_number': instance.stock_lot.lot_number if instance.stock_lot else None,
            'quantity': float(instance.quantity) if instance.quantity else None,
            'move_type': instance.move_type,
            'user': instance.user.username if instance.user else None,
            'notes': instance.notes
        }
        user = None  # Placeholder for now
        AuditLog.objects.create(
            user=user, 
            action='CREATE_STOCK_MOVEMENT', 
            details=details
        )