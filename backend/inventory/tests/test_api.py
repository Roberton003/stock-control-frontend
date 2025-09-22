import pytest
from rest_framework.test import APIClient
from inventory.models import Reagent, Category, Supplier, StockLot, Location, StockMovement, User
import datetime

@pytest.mark.django_db
def test_create_reagent():
    """ 
    Tests that a new reagent can be created via the API.
    """
    client = APIClient()

    # Create prerequisites
    category = Category.objects.create(name='Ácidos')
    supplier = Supplier.objects.create(name='Fornecedor Exemplo')

    data = {
        'name': 'Ácido Clorídrico',
        'sku': 'HCL-001',
        'category': category.id,
        'supplier': supplier.id,
        'min_stock_level': 100.00
    }

    response = client.post('/api/v1/reagents/', data, format='json')

    assert response.status_code == 201
    assert Reagent.objects.filter(sku='HCL-001').exists()

@pytest.mark.django_db
def test_list_reagents():
    """
    Tests that the API can list reagents.
    """
    client = APIClient()
    category = Category.objects.create(name='Bases')
    supplier = Supplier.objects.create(name='Outro Fornecedor')
    Reagent.objects.create(
        name='Hidróxido de Sódio',
        sku='NAOH-001',
        category=category,
        supplier=supplier,
        min_stock_level=50.00
    )

    response = client.get('/api/v1/reagents/')

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
    reagent = Reagent.objects.create(
        name='Cloreto de Sódio',
        sku='NACL-001',
        category=category,
        supplier=supplier,
        min_stock_level=1000.00
    )

    data = {
        'reagent': reagent.id,
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
def test_create_stock_movement():
    """
    Tests that a new stock movement can be recorded via the API.
    """
    client = APIClient()

    # Create prerequisites
    category = Category.objects.create(name='Solventes')
    supplier = Supplier.objects.create(name='Fornecedor de Solventes')
    location = Location.objects.create(name='Armário 5')
    reagent = Reagent.objects.create(
        name='Etanol',
        sku='ETOH-001',
        category=category,
        supplier=supplier,
        min_stock_level=2000.00
    )
    stock_lot = StockLot.objects.create(
        reagent=reagent,
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
        'reagent': reagent.id, # Changed from stock_lot
        'user': user.id,
        'quantity': 500.00,
        'move_type': 'Retirada',
        'notes': 'Uso em cromatografia'
    }

    response = client.post('/api/v1/stock-movements/', data, format='json')

    assert response.status_code == 201
    # The stock_lot is determined by FEFO logic in the serializer, so we can't assert on a specific stock_lot directly here.
    # Instead, we assert that a movement was created for the correct quantity and type.
    assert StockMovement.objects.filter(quantity=500.00, move_type='Retirada').exists()
    # We should also check if the stock_lot's current_quantity was updated, but that's part of the FEFO logic test.