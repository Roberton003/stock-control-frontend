import pytest
from rest_framework.test import APIClient
from inventory.models import Produto, Category, Supplier, StockLot, Location, MovimentacaoEstoque, User, Requisition
import datetime
from django.utils import timezone
from decimal import Decimal
import time

@pytest.fixture
def performance_test_data():
    """Create a large dataset for performance testing"""
    # Create categories
    categories = []
    for i in range(10):
        categories.append(Category.objects.create(name=f'Category {i}'))
    
    # Create suppliers
    suppliers = []
    for i in range(20):
        suppliers.append(Supplier.objects.create(name=f'Supplier {i}'))
    
    # Create locations
    locations = []
    for i in range(50):
        locations.append(Location.objects.create(name=f'Location {i}'))
    
    # Create produtos
    produtos = []
    for i in range(200):
        produtos.append(Produto.objects.create(
            nome=f'Produto {i}',
            sku=f'SKU-{i:03d}',
            category=categories[i % len(categories)],
            fornecedor=suppliers[i % len(suppliers)],
            quantidade=Decimal('100.00')
        ))
    
    # Create stock lots
    stock_lots = []
    for i in range(1000):
        stock_lots.append(StockLot.objects.create(
            produto=produtos[i % len(produtos)],
            lot_number=f'LOT-{i:04d}',
            location=locations[i % len(locations)],
            expiry_date=timezone.now().date() + datetime.timedelta(days=365),
            purchase_price=Decimal(f'{10 + (i % 100)}'),
            initial_quantity=Decimal('1000.00'),
            current_quantity=Decimal('1000.00')
        ))
    
    # Create users
    users = []
    for i in range(50):
        users.append(User.objects.create_user(
            username=f'user{i}',
            password='testpass',
            role='Analista' if i % 2 == 0 else 'Convidado'
        ))
    
    # Create some stock movements
    for i in range(5000):
        MovimentacaoEstoque.objects.create(
            produto=stock_lots[i % len(stock_lots)].produto,
            usuario=users[i % len(users)],
            quantidade=Decimal(f'{10 + (i % 100)}'),
            tipo='SAIDA' if i % 3 == 0 else 'ENTRADA',
        )
    
    # Create some requisitions
    for i in range(1000):
        Requisition.objects.create(
            requester=users[i % len(users)],
            produto=produtos[i % len(produtos)],
            quantity=Decimal(f'{50 + (i % 200)}'),
            status='Pendente' if i % 3 == 0 else 'Aprovada'
        )
    
    return {
        'categories': categories,
        'suppliers': suppliers,
        'locations': locations,
        'produtos': produtos,
        'stock_lots': stock_lots,
        'users': users
    }

@pytest.mark.django_db
def test_dashboard_performance(performance_test_data):
    """Test the performance of the dashboard summary endpoint"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    # Warm up the database
    client.get('/api/v1/dashboard/summary/')
    
    # Measure performance
    start_time = time.time()
    response = client.get('/api/v1/dashboard/summary/')
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 2.0  # Should respond in less than 2 seconds

@pytest.mark.django_db
def test_produtos_list_performance(performance_test_data):
    """Test the performance of the produtos list endpoint"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    # Warm up the database
    client.get('/api/v1/produtos/')
    
    # Measure performance
    start_time = time.time()
    response = client.get('/api/v1/produtos/')
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 1.0  # Should respond in less than 1 second

@pytest.mark.django_db
def test_stock_lots_list_performance(performance_test_data):
    """Test the performance of the stock lots list endpoint"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    # Warm up the database
    client.get('/api/v1/stock-lots/')
    
    # Measure performance
    start_time = time.time()
    response = client.get('/api/v1/stock-lots/')
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 1.5  # Should respond in less than 1.5 seconds

@pytest.mark.django_db
def test_requisitions_list_performance(performance_test_data):
    """Test the performance of the requisitions list endpoint"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    # Warm up the database
    client.get('/api/v1/requisitions/')
    
    # Measure performance
    start_time = time.time()
    response = client.get('/api/v1/requisitions/')
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 1.0  # Should respond in less than 1 second

@pytest.mark.django_db
def test_single_produto_retrieve_performance(performance_test_data):
    """Test the performance of retrieving a single produto"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    produto = performance_test_data['produtos'][0]
    
    # Warm up the database
    client.get(f'/api/v1/produtos/{produto.id}/')
    
    # Measure performance
    start_time = time.time()
    response = client.get(f'/api/v1/produtos/{produto.id}/')
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 0.5  # Should respond in less than 0.5 seconds

@pytest.mark.django_db
def test_single_stock_lot_retrieve_performance(performance_test_data):
    """Test the performance of retrieving a single stock lot"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    stock_lot = performance_test_data['stock_lots'][0]
    
    # Warm up the database
    client.get(f'/api/v1/stock-lots/{stock_lot.id}/')
    
    # Measure performance
    start_time = time.time()
    response = client.get(f'/api/v1/stock-lots/{stock_lot.id}/')
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 0.5  # Should respond in less than 0.5 seconds