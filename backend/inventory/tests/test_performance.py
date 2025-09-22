import pytest
from rest_framework.test import APIClient
from inventory.models import Reagent, Category, Supplier, StockLot, Location, StockMovement, User, Requisition
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
    
    # Create reagents
    reagents = []
    for i in range(200):
        reagents.append(Reagent.objects.create(
            name=f'Reagent {i}',
            sku=f'SKU-{i:03d}',
            category=categories[i % len(categories)],
            supplier=suppliers[i % len(suppliers)],
            min_stock_level=Decimal('100.00')
        ))
    
    # Create stock lots
    stock_lots = []
    for i in range(1000):
        stock_lots.append(StockLot.objects.create(
            reagent=reagents[i % len(reagents)],
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
        StockMovement.objects.create(
            stock_lot=stock_lots[i % len(stock_lots)],
            user=users[i % len(users)],
            quantity=Decimal(f'{10 + (i % 100)}'),
            move_type='Retirada' if i % 3 == 0 else 'Entrada',
            notes=f'Test movement {i}'
        )
    
    # Create some requisitions
    for i in range(1000):
        Requisition.objects.create(
            requester=users[i % len(users)],
            reagent=reagents[i % len(reagents)],
            quantity=Decimal(f'{50 + (i % 200)}'),
            status='Pendente' if i % 3 == 0 else 'Aprovada'
        )
    
    return {
        'categories': categories,
        'suppliers': suppliers,
        'locations': locations,
        'reagents': reagents,
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
def test_reagents_list_performance(performance_test_data):
    """Test the performance of the reagents list endpoint"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    # Warm up the database
    client.get('/api/v1/reagents/')
    
    # Measure performance
    start_time = time.time()
    response = client.get('/api/v1/reagents/')
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
def test_single_reagent_retrieve_performance(performance_test_data):
    """Test the performance of retrieving a single reagent"""
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    
    reagent = performance_test_data['reagents'][0]
    
    # Warm up the database
    client.get(f'/api/v1/reagents/{reagent.id}/')
    
    # Measure performance
    start_time = time.time()
    response = client.get(f'/api/v1/reagents/{reagent.id}/')
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