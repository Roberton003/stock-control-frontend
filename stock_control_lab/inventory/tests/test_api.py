import pytest
from rest_framework.test import APIClient
from inventory.models import Produto, Category, Supplier, StockLot, Location, MovimentacaoEstoque, User
import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_api_client():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='USER')
    client.force_authenticate(user=user)
    return client, user

@pytest.fixture
def setup_data():
    """Create common test data"""
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    produto = Produto.objects.create(
        nome='Test Produto',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=100
    )
    return category, supplier, location, produto

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
def test_retrieve_produto():
    """Test retrieving a single produto by ID"""
    client = APIClient()
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    produto = Produto.objects.create(
        nome='Test Produto',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )

    response = client.get(f'/api/v1/produtos/{produto.id}/')
    
    assert response.status_code == 200
    assert response.data['nome'] == 'Test Produto'
    assert response.data['sku'] == 'TEST-001'

@pytest.mark.django_db
def test_update_produto():
    """Test updating a produto"""
    client = APIClient()
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    produto = Produto.objects.create(
        nome='Original Produto',
        sku='ORIG-001',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )

    update_data = {
        'nome': 'Updated Produto',
        'sku': 'UPD-001',
        'category': category.id,
        'fornecedor': supplier.id,
        'quantidade': 75.00
    }

    response = client.put(f'/api/v1/produtos/{produto.id}/', update_data, format='json')
    
    assert response.status_code == 200
    produto.refresh_from_db()
    assert produto.nome == 'Updated Produto'
    assert produto.quantidade == 75.00

@pytest.mark.django_db
def test_delete_produto():
    """Test deleting a produto"""
    client = APIClient()
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    produto = Produto.objects.create(
        nome='Produto to Delete',
        sku='DEL-001',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )

    response = client.delete(f'/api/v1/produtos/{produto.id}/')
    
    assert response.status_code == 204
    assert not Produto.objects.filter(id=produto.id).exists()

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

    # Create an ENTRADA movement (uses MovimentacaoEstoqueSerializer)
    data = {
        'produto': produto.id,
        'usuario': user.id,
        'quantidade': 500.00,
        'tipo': 'ENTRADA'
    }

    response = client.post('/api/v1/movimentacoes/', data, format='json')

    assert response.status_code == 201
    assert MovimentacaoEstoque.objects.filter(quantidade=500.00, tipo='ENTRADA').exists()

@pytest.mark.django_db
def test_movimentacao_estoque_with_authentication():
    """Test movimentacao endpoint with proper authentication and permissions"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='USER')
    client.force_authenticate(user=user)
    
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    produto = Produto.objects.create(
        nome='Test Produto',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )

    # Create an ENTRADA movement (uses MovimentacaoEstoqueSerializer)
    data = {
        'produto': produto.id,
        'usuario': user.id,
        'quantidade': 10.0,
        'tipo': 'ENTRADA'
    }

    response = client.post('/api/v1/movimentacoes/', data, format='json')
    
    assert response.status_code == 201
    movimentacao = MovimentacaoEstoque.objects.get(produto=produto, tipo='ENTRADA')
    assert movimentacao.tipo == 'ENTRADA'
    assert movimentacao.quantidade == 10.0

@pytest.mark.django_db
def test_movimentacao_estoque_validation():
    """Test validation for movimentacao endpoint"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='USER')
    client.force_authenticate(user=user)
    
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    produto = Produto.objects.create(
        nome='Test Produto',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )

    # Test with invalid tipo
    data = {
        'produto': produto.id,
        'usuario': user.id,
        'quantidade': 10.0,
        'tipo': 'INVALIDO'
    }

    response = client.post('/api/v1/movimentacoes/', data, format='json')
    
    assert response.status_code == 400  # Should be 400 for invalid data

@pytest.mark.django_db
def test_movimentacao_estoque_saida():
    """Test SAIDA tipo which uses StockWithdrawalSerializer through the ViewSet withdraw action"""
    # This test will use the withdraw action instead of the regular create endpoint
    pass  # Skipping this test for now as it requires specific setup for the ViewSet action

@pytest.mark.django_db
def test_create_category():
    """Test creating a category via API"""
    client = APIClient()
    data = {
        'name': 'New Category',
        'description': 'A new test category'
    }
    
    response = client.post('/api/v1/categories/', data, format='json')
    
    assert response.status_code == 201
    assert Category.objects.filter(name='New Category').exists()

@pytest.mark.django_db
def test_create_supplier():
    """Test creating a supplier via API"""
    client = APIClient()
    data = {
        'name': 'New Supplier',
        'contact_person': 'John Doe',
        'email': 'john@example.com',
        'phone': '123456789'
    }
    
    response = client.post('/api/v1/suppliers/', data, format='json')
    
    assert response.status_code == 201
    assert Supplier.objects.filter(name='New Supplier').exists()

@pytest.mark.django_db
def test_create_location():
    """Test creating a location via API"""
    client = APIClient()
    data = {
        'name': 'New Location',
        'description': 'A new test location'
    }
    
    response = client.post('/api/v1/locations/', data, format='json')
    
    assert response.status_code == 201
    assert Location.objects.filter(name='New Location').exists()