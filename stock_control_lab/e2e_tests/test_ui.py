import pytest
from rest_framework.test import APIClient
from inventory.models import Produto, Category, Supplier, StockLot, Location, MovimentacaoEstoque, User
import datetime
from decimal import Decimal
from decimal import Decimal
from decimal import Decimal
from decimal import Decimal
from decimal import Decimal
from decimal import Decimal
from django.utils import timezone
from freezegun import freeze_time
from datetime import timedelta

@pytest.mark.django_db
def test_create_produto():
    """ 
    Tests that a new produto can be created via the API.
    """
    client = APIClient()

    # Create prerequisites
    category = Category.objects.create(name='Ácidos')
    supplier = Supplier.objects.create(name='Fornecedor Exemplo')

    data = {
        'nome': 'Ácido Clorídrico',
        'sku': 'HCL-001',
        'category': category.id,
        'fornecedor': supplier.id,
        'quantidade': 100.00
    }

    response = client.post('/api/v1/produtos/', data, format='json')

    assert response.status_code == 201
    assert Produto.objects.filter(sku='HCL-001').exists()

@pytest.mark.django_db
def test_list_produtos():
    """
    Tests that the API can list produtos.
    """
    client = APIClient()
    category = Category.objects.create(name='Bases')
    supplier = Supplier.objects.create(name='Outro Fornecedor')
    Produto.objects.create(
        nome='Hidróxido de Sódio',
        sku='NAOH-001',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )

    response = client.get('/api/v1/produtos/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['sku'] == 'NAOH-001'

@pytest.mark.django_db
def test_create_stock_lot():
    """
    Tests that a new stock lot can be added via the API.
    """
    client = APIClient()

    # Create prerequisites
    category = Category.objects.create(name='Sais')
    supplier = Supplier.objects.create(name='Fornecedor de Sais')
    location = Location.objects.create(name='Prateleira C-1')
    produto = Produto.objects.create(
        nome='Cloreto de Sódio',
        sku='NACL-001',
        category=category,
        fornecedor=supplier,
        quantidade=1000.00
    )

    data = {
        'produto': produto.id,
        'lot_number': 'NACL20250917',
        'location': location.id,
        'expiry_date': (datetime.date.today() + datetime.timedelta(days=365)).isoformat(),
        'purchase_price': 50.00,
        'initial_quantity': 5000.00,
        'current_quantity': 5000.00
    }

    response = client.post('/api/v1/stock-lots/', data, format='json')

    assert response.status_code == 201
    assert StockLot.objects.filter(lot_number='NACL20250917').exists()

@pytest.mark.django_db
def test_create_movimentacao_estoque():
    """
    Tests that a new stock movement can be recorded via the API.
    """
    client = APIClient()

    # Create prerequisites
    category = Category.objects.create(name='Solventes')
    supplier = Supplier.objects.create(name='Fornecedor de Solventes')
    location = Location.objects.create(name='Armário 5')
    produto = Produto.objects.create(
        nome='Etanol',
        sku='ETOH-001',
        category=category,
        fornecedor=supplier,
        quantidade=2000.00
    )
    stock_lot = StockLot.objects.create(
        produto=produto,
        lot_number='ETOH20250101',
        location=location,
        expiry_date=datetime.date(2026, 1, 1),
        purchase_price=25.00,
        initial_quantity=10000.00,
        current_quantity=10000.00
    )
    user = User.objects.create_user(username='analista1', password='testpass', role='Analista')
    client.force_authenticate(user=user) # Authenticate the client

    data = {
        'produto_id': produto.id,
        'quantidade': 500.00,
        'tipo': 'SAIDA'
    }

    response = client.post('/api/v1/movimentacoes/', data, format='json')

    assert response.status_code == 201
    # The stock_lot is determined by FEFO logic in the serializer, so we can't assert on a specific stock_lot directly here.
    # Instead, we assert that a movement was created for the correct quantity and type.
    assert MovimentacaoEstoque.objects.filter(quantidade=500.00, tipo='SAIDA').exists()
    # We should also check if the stock_lot's current_quantity was updated, but that's part of the FEFO logic test.

@pytest.fixture
def authenticated_client_and_data():
    client = APIClient()
    user = User.objects.create_user(username='reportuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)

    category = Category.objects.create(name='ReportCategory')
    supplier = Supplier.objects.create(name='ReportSupplier')
    location = Location.objects.create(name='ReportLocation')
    produto = Produto.objects.create(
        nome='ReportProduto', sku='RR-001', category=category, fornecedor=supplier, quantidade=10
    )
    return client, user, produto, category, supplier, location

@pytest.mark.django_db
def test_consumption_by_user_report(authenticated_client_and_data):
    client, user, produto, _, _, location = authenticated_client_and_data
    
    # Create stock lots and movements for the report
    stock_lot1 = StockLot.objects.create(
        produto=produto, lot_number='LOT-C-001', location=location,
        expiry_date=timezone.now().date() + timedelta(days=30),
        purchase_price=10, initial_quantity=100, current_quantity=100
    )
    stock_lot2 = StockLot.objects.create(
        produto=produto, lot_number='LOT-C-002', location=location,
        expiry_date=timezone.now().date() + timedelta(days=60),
        purchase_price=10, initial_quantity=100, current_quantity=100
    )

    with freeze_time("2025-01-15"):
        MovimentacaoEstoque.objects.create(
            produto=produto, usuario=user, quantidade=20, tipo='SAIDA'
        )
    with freeze_time("2025-02-10"):
        MovimentacaoEstoque.objects.create(
            produto=produto, usuario=user, quantidade=30, tipo='SAIDA'
        )
    with freeze_time("2025-03-01"): # Outside report range
        MovimentacaoEstoque.objects.create(
            produto=produto, usuario=user, quantidade=10, tipo='SAIDA'
        )

    start_date = "2025-01-01"
    end_date = "2025-02-28"
    response = client.get(f'/api/v1/reports/consumption-by-user/?start_date={start_date}&end_date={end_date}')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['usuario__username'] == user.username
    assert response.data[0]['produto__nome'] == produto.nome
    assert response.data[0]['total_quantity'] == Decimal('50.00')
@pytest.mark.django_db
def test_waste_loss_report(authenticated_client_and_data):
    client, user, produto, _, _, location = authenticated_client_and_data

    stock_lot = StockLot.objects.create(
        produto=produto, lot_number='LOT-WL-001', location=location,
        expiry_date=timezone.now().date() + timedelta(days=30),
        purchase_price=10, initial_quantity=100, current_quantity=100
    )

    with freeze_time("2025-01-20"):
        MovimentacaoEstoque.objects.create(
            produto=produto, usuario=user, quantidade=15, tipo='Descarte'
        )
    with freeze_time("2025-02-15"):
        MovimentacaoEstoque.objects.create(
            produto=produto, usuario=user, quantidade=-10, tipo='Ajuste' # Negative adjustment
        )
    with freeze_time("2025-03-05"): # Outside report range
        MovimentacaoEstoque.objects.create(
            produto=produto, usuario=user, quantidade=5, tipo='Descarte'
        )

    start_date = "2025-01-01"
    end_date = "2025-02-28"
    response = client.get(f'/api/v1/reports/waste-loss/?start_date={start_date}&end_date={end_date}')

    assert response.status_code == 200
    assert len(response.data) == 2
    # Find the adjustment record
    adjustment_record = next((item for item in response.data if item['tipo'] == 'Ajuste'), None)
    assert adjustment_record is not None
    assert float(adjustment_record['total_quantity']) == -10.0
    
    # Find the discard record
    discard_record = next((item for item in response.data if item['tipo'] == 'Descarte'), None)
    assert discard_record is not None
    assert float(discard_record['total_quantity']) == 15.0
@pytest.mark.django_db
def test_stock_value_report(authenticated_client_and_data):
    client, _, produto, category, _, location = authenticated_client_and_data

    StockLot.objects.create(
        produto=produto, lot_number='LOT-SV-001', location=location,
        expiry_date=timezone.now().date() + timedelta(days=30),
        purchase_price=100, initial_quantity=10, current_quantity=10
    )
    StockLot.objects.create(
        produto=produto, lot_number='LOT-SV-002', location=location,
        expiry_date=timezone.now().date() + timedelta(days=60),
        purchase_price=50, initial_quantity=5, current_quantity=5
    )

    # Test total value
    response = client.get('/api/v1/reports/stock-value/')
    assert response.status_code == 200
    assert float(response.data['total_value']) == 1250.0  # 10*100 + 5*50
    # Test grouped by category
    response_cat = client.get('/api/v1/reports/stock-value/?group_by=category')
    assert response_cat.status_code == 200
    assert len(response_cat.data) == 1
    assert response_cat.data[0]['produto_category_nome'] == category.name
    assert Decimal(response_cat.data[0]['total_value']) == Decimal('1250.00')

    # Test grouped by location
    response_loc = client.get('/api/v1/reports/stock-value/?group_by=location')
    assert response_loc.status_code == 200
    assert len(response_loc.data) == 1
    assert response_loc.data[0]['location_nome'] == location.name
    assert Decimal(response_loc.data[0]['total_value']) == Decimal('1250.00')

@pytest.mark.django_db
def test_expiry_report(authenticated_client_and_data):
    client, _, produto, _, _, location = authenticated_client_and_data

    # Lot expiring soon
    StockLot.objects.create(
        produto=produto, lot_number='LOT-EXP-001', location=location,
        expiry_date=timezone.now().date() + timedelta(days=5), # Expires in 5 days
        purchase_price=10, initial_quantity=100, current_quantity=100
    )
    # Lot expiring later
    StockLot.objects.create(
        produto=produto, lot_number='LOT-EXP-002', location=location,
        expiry_date=timezone.now().date() + timedelta(days=60), # Expires in 60 days
        purchase_price=10, initial_quantity=100, current_quantity=100
    )
    # Expired lot
    StockLot.objects.create(
        produto=produto, lot_number='LOT-EXP-003', location=location,
        expiry_date=timezone.now().date() - timedelta(days=5), # Expired 5 days ago
        purchase_price=10, initial_quantity=100, current_quantity=100
    )

    # Test upcoming expiry (default 30 days)
    response_upcoming = client.get('/api/v1/reports/expiry/')
    assert response_upcoming.status_code == 200
    assert len(response_upcoming.data) == 2 # LOT-EXP-001 and LOT-EXP-002 (if today is before 60 days)
    assert response_upcoming.data[0]['lot_number'] == 'LOT-EXP-001'

    # Test specific days until expiry
    response_specific = client.get('/api/v1/reports/expiry/?days_until_expiry=10')
    assert response_specific.status_code == 200
    assert len(response_specific.data) == 1
    assert response_specific.data[0]['lot_number'] == 'LOT-EXP-001'

    # Test expired lots
    response_expired = client.get('/api/v1/reports/expiry/?expired=true')
    assert response_expired.status_code == 200
    assert len(response_expired.data) == 1
    assert response_expired.data[0]['lot_number'] == 'LOT-EXP-003'
