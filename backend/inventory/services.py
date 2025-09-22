from django.db.models import Sum, F, Q
from inventory.models import StockLot, Reagent, Requisition, User, StockMovement
from django.db import transaction
from decimal import Decimal
import datetime
from django.utils import timezone

def get_lots_for_withdrawal(reagent_obj: Reagent, quantity_needed: float):
    """
    Applies FEFO (First-Expire, First-Out) logic to select stock lots for withdrawal.
    Returns a list of (StockLot, quantity_to_withdraw) tuples.
    """
    quantity_needed = Decimal(str(quantity_needed)) # Convert to Decimal

    # Get all available lots for the reagent, ordered by expiry date (FEFO)
    available_lots = StockLot.objects.filter(
        reagent=reagent_obj,
        current_quantity__gt=0
    ).order_by('expiry_date')

    selected_lots_info = []
    remaining_quantity = quantity_needed

    for lot in available_lots:
        if remaining_quantity <= 0:
            break

        if lot.current_quantity >= remaining_quantity:
            # This lot can cover the remaining quantity
            selected_lots_info.append((lot, remaining_quantity))
            remaining_quantity = Decimal(0)
        else:
            # This lot is fully depleted
            selected_lots_info.append((lot, lot.current_quantity))
            remaining_quantity -= lot.current_quantity

    if remaining_quantity > 0:
        # Not enough stock to cover the withdrawal
        raise ValueError(f"Not enough stock for {reagent_obj.name}. Needed {quantity_needed}, available {quantity_needed - remaining_quantity}.")

    return selected_lots_info

@transaction.atomic
def perform_withdrawal(reagent_obj: Reagent, quantity_needed: float, user):
    """
    Performs a withdrawal operation, applying FEFO logic and updating stock quantities.
    """
    selected_lots_info = get_lots_for_withdrawal(reagent_obj, quantity_needed)
    
    total_withdrawn = 0
    for lot, qty_to_withdraw in selected_lots_info:
        lot.current_quantity -= qty_to_withdraw
        lot.save()
        total_withdrawn += qty_to_withdraw
        # Here you would also create a StockMovement record
        StockMovement.objects.create(stock_lot=lot, user=user, quantity=qty_to_withdraw, move_type='Retirada')

    return total_withdrawn

@transaction.atomic
def approve_requisition(requisition_obj: Requisition, approver_user: User):
    """
    Approves a requisition, updates its status, and performs the stock withdrawal.
    """
    if requisition_obj.status != 'Pendente':
        raise ValueError("Requisition is not in 'Pendente' status.")

    # Perform withdrawal using FEFO logic
    perform_withdrawal(
        reagent_obj=requisition_obj.reagent,
        quantity_needed=requisition_obj.quantity,
        user=approver_user # The approver is the one performing the withdrawal
    )

    # Update requisition status
    requisition_obj.status = 'Aprovada'
    requisition_obj.approver = approver_user
    requisition_obj.approval_date = datetime.datetime.now()
    requisition_obj.save()

    return True

def get_consumption_by_user_report(start_date, end_date, user_id=None, reagent_id=None):
    """
    Generates a report on reagent consumption by user within a specified period.
    """
    movements = StockMovement.objects.filter(
        move_type='Retirada',
        timestamp__range=(start_date, end_date)
    )

    if user_id:
        movements = movements.filter(user_id=user_id)
    if reagent_id:
        movements = movements.filter(stock_lot__reagent_id=reagent_id)

    report_data = movements.values(
        'user__username', 'stock_lot__reagent__name'
    ).annotate(total_quantity=Sum('quantity')).order_by('user__username', 'stock_lot__reagent__name')

    return list(report_data)

def get_waste_loss_report(start_date, end_date, reagent_id=None):
    """
    Generates a report on reagent waste and loss within a specified period.
    """
    movements = StockMovement.objects.filter(
        timestamp__range=(start_date, end_date)
    ).filter(
        Q(move_type='Descarte') | (Q(move_type='Ajuste') & Q(quantity__lt=0))
    )

    if reagent_id:
        movements = movements.filter(stock_lot__reagent_id=reagent_id)

    report_data = movements.values(
        'stock_lot__reagent__name', 'move_type'
    ).annotate(total_quantity=Sum('quantity')).order_by('stock_lot__reagent__name', 'move_type')

    return list(report_data)

def get_stock_value_report(group_by=None):
    """
    Calculates the total value of all stock lots, optionally grouped by category or location.
    """
    if group_by not in [None, 'category', 'location']:
        raise ValueError("Invalid group_by parameter. Must be 'category', 'location', or None.")

    stock_value_query = StockLot.objects.filter(current_quantity__gt=0)

    if group_by == 'category':
        report_data = stock_value_query.values(
            'reagent__category__name'
        ).annotate(total_value=Sum(F('current_quantity') * F('purchase_price'))).order_by('reagent__category__name')
    elif group_by == 'location':
        report_data = stock_value_query.values(
            'location__name'
        ).annotate(total_value=Sum(F('current_quantity') * F('purchase_price'))).order_by('location__name')
    else:
        total_value = stock_value_query.aggregate(
            total_value=Sum(F('current_quantity') * F('purchase_price'))
        )['total_value'] or Decimal(0)
        return {'total_value': total_value}

    return list(report_data)

def get_expiry_report(days_until_expiry=None, expired=False):
    """
    Generates a report of reagents with upcoming or past expiry dates.
    """
    today = timezone.now().date()
    
    lots = StockLot.objects.filter(current_quantity__gt=0)

    if expired:
        lots = lots.filter(expiry_date__lt=today)
    elif days_until_expiry is not None:
        expiry_threshold_date = today + datetime.timedelta(days=days_until_expiry)
        lots = lots.filter(expiry_date__lte=expiry_threshold_date, expiry_date__gte=today)
    else:
        # If no parameters, return all lots with future expiry dates
        lots = lots.filter(expiry_date__gte=today)

    report_data = lots.values(
        'reagent__name', 'lot_number', 'expiry_date', 'current_quantity', 'location__name'
    ).order_by('expiry_date', 'reagent__name')

    return list(report_data)

def calculate_total_stock_value():
    """
    Calculates the total value of all stock lots based on their purchase price.
    """
    return StockLot.objects.filter(current_quantity__gt=0).aggregate(
        total=Sum(F('current_quantity') * F('purchase_price'))
    ).get('total') or Decimal(0)