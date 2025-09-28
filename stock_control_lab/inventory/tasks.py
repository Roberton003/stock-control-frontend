from celery import shared_task
from django.db.models import Sum
from datetime import date, timedelta
from .models import Alert, Notification, StockLot

@shared_task
def check_alerts():
    active_alerts = Alert.objects.filter(is_active=True)

    for alert in active_alerts:
        if alert.alert_type == 'low_stock':
            # Calculate the total current quantity for the reagent across all its stock lots
            total_quantity = StockLot.objects.filter(reagent=alert.reagent).aggregate(total=Sum('current_quantity'))['total'] or 0

            if total_quantity < alert.threshold_value:
                message = f"Alerta de estoque baixo para {alert.reagent.name}. Quantidade atual: {total_quantity}, Limite: {alert.threshold_value}."
                
                # Create notification for all users linked to the alert
                for user in alert.users_to_notify.all():
                    # Avoid creating duplicate notifications
                    Notification.objects.get_or_create(
                        user=user, 
                        alert=alert, 
                        message=message, 
                        is_read=False
                    )
        
        elif alert.alert_type == 'expiry_date':
            # Calculate the date threshold
            threshold_days = int(alert.threshold_value)
            expiry_limit_date = date.today() + timedelta(days=threshold_days)

            # Find stock lots expiring within the threshold
            expiring_lots = StockLot.objects.filter(
                reagent=alert.reagent,
                expiry_date__lte=expiry_limit_date,
                current_quantity__gt=0  # Only consider lots that are still in stock
            )

            if expiring_lots.exists():
                for lot in expiring_lots:
                    message = f"Alerta de validade para {alert.reagent.name} (Lote: {lot.lot_number}). Vence em: {lot.expiry_date.strftime('%d/%m/%Y')}."
                    
                    for user in alert.users_to_notify.all():
                        Notification.objects.get_or_create(
                            user=user,
                            alert=alert,
                            message=message,
                            is_read=False
                        )