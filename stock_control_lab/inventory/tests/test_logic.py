import pytest
from inventory.models import Produto, Category, Supplier, StockLot, Location, User, Requisition, AuditLog, MovimentacaoEstoque
from inventory.services import get_lots_for_withdrawal, approve_requisition, perform_withdrawal, calculate_total_stock_value
import datetime
from decimal import Decimal
from django.db.models import Sum, F # Added

@pytest.mark.django_db
def test_fefo_withdrawal_logic():
    """
    Tests that the FEFO (First-Expire, First-Out) logic correctly prioritizes
    lots with the earliest expiry dates for withdrawal.
    """
    # Create prerequisites
    category = Category.objects.create(name='Ácidos')
    supplier = Supplier.objects.create(name='Fornecedor Geral')
    location = Location.objects.create(name='Armário Principal')
    produto = Produto.objects.create(
        nome='Ácido Nítrico',
        sku='HNO3-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )

    # Create multiple lots with different expiry dates
    lot_a = StockLot.objects.create(
        produto=produto,
        lot_number='HNO3-LoteA',
        location=location,
        expiry_date=datetime.date(2025, 1, 1), # Expires first
        purchase_price=Decimal('10.00'),
        initial_quantity=Decimal('100.00'),
        current_quantity=Decimal('100.00')
    )
    lot_b = StockLot.objects.create(
        produto=produto,
        lot_number='HNO3-LoteB',
        location=location,
        expiry_date=datetime.date(2025, 6, 1), # Expires second
        purchase_price=Decimal('10.00'),
        initial_quantity=Decimal('100.00'),
        current_quantity=Decimal('100.00')
    )
    lot_c = StockLot.objects.create(
        produto=produto,
        lot_number='HNO3-LoteC',
        location=location,
        expiry_date=datetime.date(2026, 1, 1), # Expires last
        purchase_price=Decimal('10.00'),
        initial_quantity=Decimal('100.00'),
        current_quantity=Decimal('100.00')
    )

    # Test 1: Withdraw a small quantity from lot_a
    selected_lots_info_1 = get_lots_for_withdrawal(produto, Decimal('50.00'))
    assert len(selected_lots_info_1) == 1
    assert selected_lots_info_1[0][0].id == lot_a.id
    assert selected_lots_info_1[0][1] == Decimal('50.00')

    # Test 2: Withdraw a quantity that depletes lot_a and partially lot_b
    selected_lots_info_2 = get_lots_for_withdrawal(produto, Decimal('150.00'))
    assert len(selected_lots_info_2) == 2
    assert selected_lots_info_2[0][0].id == lot_a.id
    assert selected_lots_info_2[0][1] == Decimal('100.00') # All of lot_a
    assert selected_lots_info_2[1][0].id == lot_b.id
    assert selected_lots_info_2[1][1] == Decimal('50.00') # Remaining from lot_b

    # Test 3: Withdraw a quantity larger than available stock
    with pytest.raises(ValueError, match="Not enough stock"): # Expect ValueError
        get_lots_for_withdrawal(produto, Decimal('500.00')) # Total available is 300

@pytest.mark.django_db
def test_get_lots_for_withdrawal_no_stock():
    """Tests FEFO logic when no stock is available."""
    category = Category.objects.create(name='Bases')
    supplier = Supplier.objects.create(name='Fornecedor Vazio')
    produto = Produto.objects.create(nome='Hidróxido de Amônio', sku='NH4OH-001', category=category, fornecedor=supplier, quantidade=100)
    
    with pytest.raises(ValueError, match="Not enough stock"):
        get_lots_for_withdrawal(produto, Decimal('1.00'))

@pytest.mark.django_db
def test_requisition_approval_flow():
    """
    Tests the requisition and approval workflow.
    """
    # Create prerequisites
    requester = User.objects.create_user(username='requester', password='pass123', role='Convidado')
    approver = User.objects.create_user(username='approver', password='pass123', role='Analista')
    category = Category.objects.create(name='Gases')
    supplier = Supplier.objects.create(name='Gás Ltda.')
    location = Location.objects.create(name='Cilindros')
    produto = Produto.objects.create(
        nome='Nitrogênio',
        sku='N2-001',
        category=category,
        fornecedor=supplier,
        quantidade=10.00
    )
    stock_lot = StockLot.objects.create(
        produto=produto,
        lot_number='N2-LoteX',
        location=location,
        expiry_date=datetime.date(2027, 1, 1),
        purchase_price=Decimal('100.00'),
        initial_quantity=Decimal('50.00'),
        current_quantity=Decimal('50.00')
    )

    # Create a requisition
    requisition = Requisition.objects.create(
        requester=requester,
        produto=produto,
        quantity=Decimal('10.00'),
        status='Pendente'
    )

    approved = approve_requisition(requisition, approver)

    # Assertions
    assert approved is True
    requisition.refresh_from_db()
    assert requisition.status == 'Aprovada'
    assert requisition.approver == approver
    # Check if stock was updated (this will be part of the approval logic)
    stock_lot.refresh_from_db()
    assert stock_lot.current_quantity == Decimal('40.00')

@pytest.mark.django_db
def test_approve_requisition_invalid_status():
    """Tests that approving a non-pending requisition raises an error."""
    requester = User.objects.create_user(username='requester2', password='pass123')
    approver = User.objects.create_user(username='approver2', password='pass123')
    produto = Produto.objects.create(nome='Produto Aprovado', sku='PA-001', category=Category.objects.create(name='Cat A'), fornecedor=Supplier.objects.create(name='Sup A'), quantidade=1)
    requisition = Requisition.objects.create(requester=requester, produto=produto, quantity=1, status='Aprovada')

    with pytest.raises(ValueError, match="Requisition is not in 'Pendente' status."):
        approve_requisition(requisition, approver)

@pytest.mark.django_db
def test_audit_log_creation():
    """
    Tests that creating a model instance automatically creates an AuditLog entry.
    """
    # Create a Category instance
    category = Category.objects.create(name='Test Category', description='For testing audit log')

    # Assert that an AuditLog entry was created
    assert AuditLog.objects.filter(action='CREATE_CATEGORY', details__model='Category', details__id=category.id).exists()

    # Test update
    category.name = 'Updated Category'
    category.save()
    assert AuditLog.objects.filter(action='UPDATE_CATEGORY', details__model='Category', details__id=category.id).exists()

    # Test delete
    category_id = category.id
    category.delete()
    assert AuditLog.objects.filter(action='DELETE_CATEGORY', details__model='Category', details__id=category_id).exists()

@pytest.mark.django_db
def test_perform_withdrawal_updates_stock():
    """
    Tests that perform_withdrawal correctly updates stock quantities and creates MovimentacaoEstoque records.
    """
    # Create prerequisites
    requester = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    produto = Produto.objects.create(
        nome='Test Produto',
        sku='TP-001',
        category=category,
        fornecedor=supplier,
        quantidade=10.00
    )
    lot1 = StockLot.objects.create(
        produto=produto,
        lot_number='LOT-001',
        location=location,
        expiry_date=datetime.date(2025, 1, 1),
        purchase_price=Decimal('10.00'),
        initial_quantity=Decimal('100.00'),
        current_quantity=Decimal('100.00')
    )
    lot2 = StockLot.objects.create(
        produto=produto,
        lot_number='LOT-002',
        location=location,
        expiry_date=datetime.date(2025, 12, 31),
        purchase_price=Decimal('10.00'),
        initial_quantity=Decimal('100.00'),
        current_quantity=Decimal('100.00')
    )

    # Perform withdrawal
    initial_lot1_qty = lot1.current_quantity
    initial_lot2_qty = lot2.current_quantity
    withdrawal_qty = Decimal('120.00')

    perform_withdrawal(produto, withdrawal_qty, requester)

    # Assertions
    lot1.refresh_from_db()
    lot2.refresh_from_db()

    assert lot1.current_quantity == Decimal('0.00') # lot1 should be depleted
    assert lot2.current_quantity == Decimal('80.00') # 20 from lot2

    # Check MovimentacaoEstoque records
    movements = MovimentacaoEstoque.objects.filter(usuario=requester, tipo='SAIDA').order_by('data')
    assert movements.count() == 2
    assert movements[0].produto == produto
    assert movements[0].quantidade == Decimal('100.00')
    assert movements[1].produto == produto
    assert movements[1].quantidade == Decimal('20.00')

@pytest.mark.django_db
def test_total_stock_value_calculation():
    """
    Tests the calculation of total stock value using the service function.
    """
    # Create prerequisites
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    produto1 = Produto.objects.create(
        nome='Produto 1',
        sku='P1-001',
        category=category,
        fornecedor=supplier,
        quantidade=10.00
    )
    produto2 = Produto.objects.create(
        nome='Produto 2',
        sku='P2-001',
        category=category,
        fornecedor=supplier,
        quantidade=10.00
    )

    StockLot.objects.create(
        produto=produto1,
        lot_number='P1-LOT1',
        location=location,
        expiry_date=datetime.date(2025, 1, 1),
        purchase_price=Decimal('10.00'),
        initial_quantity=Decimal('100.00'),
        current_quantity=Decimal('50.00')
    )
    StockLot.objects.create(
        produto=produto1,
        lot_number='P1-LOT2',
        location=location,
        expiry_date=datetime.date(2025, 12, 31),
        purchase_price=Decimal('12.00'),
        initial_quantity=Decimal('200.00'),
        current_quantity=Decimal('150.00')
    )
    StockLot.objects.create(
        produto=produto2,
        lot_number='P2-LOT1',
        location=location,
        expiry_date=datetime.date(2025, 6, 1),
        purchase_price=Decimal('5.00'),
        initial_quantity=Decimal('50.00'),
        current_quantity=Decimal('25.00')
    )

    # Calculate expected total value: (50*10) + (150*12) + (25*5) = 500 + 1800 + 125 = 2425
    expected_total_value = Decimal('2425.00')

    # Call the service function
    total_value = calculate_total_stock_value()

    assert total_value == expected_total_value
