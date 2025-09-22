import pytest
from rest_framework.test import APIClient
from inventory.models import Reagent, Category, Supplier, StockLot, Location, StockMovement, User
import datetime
from django.utils import timezone
from freezegun import freeze_time
from decimal import Decimal

@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass', role='Analista')
    client.force_authenticate(user=user)
    return client, user

@pytest.fixture
def report_test_data():
    """Create test data for report testing"""
    category = Category.objects.create(name='TestCategory')
    supplier = Supplier.objects.create(name='TestSupplier')
    location = Location.objects.create(name='TestLocation')
    reagent = Reagent.objects.create(
        name='TestReagent', 
        sku='TR-001', 
        category=category, 
        supplier=supplier, 
        min_stock_level=10
    )
    return category, supplier, location, reagent

@pytest.mark.django_db
def test_consumption_by_user_report(authenticated_client, report_test_data):
    """Test the consumption by user report endpoint"""
    client, user = authenticated_client
    category, supplier, location, reagent = report_test_data
    
    # Create stock lots and movements for the report
    stock_lot1 = StockLot.objects.create(
        reagent=reagent, lot_number='LOT-C-001', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=30),
        purchase_price=10, initial_quantity=100, current_quantity=100
    )
    stock_lot2 = StockLot.objects.create(
        reagent=reagent, lot_number='LOT-C-002', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=60),
        purchase_price=10, initial_quantity=100, current_quantity=100
    )

    with freeze_time("2025-01-15"):
        StockMovement.objects.create(
            stock_lot=stock_lot1, user=user, quantity=20, move_type='Retirada'
        )
    with freeze_time("2025-02-10"):
        StockMovement.objects.create(
            stock_lot=stock_lot2, user=user, quantity=30, move_type='Retirada'
        )

    start_date = "2025-01-01"
    end_date = "2025-02-28"
    response = client.get(f'/api/v1/reports/consumption-by-user/?start_date={start_date}&end_date={end_date}')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['user__username'] == user.username
    assert response.data[0]['stock_lot__reagent__name'] == reagent.name
    assert float(response.data[0]['total_quantity']) == 50.0

@pytest.mark.django_db
def test_waste_loss_report(authenticated_client, report_test_data):
    """Test the waste/loss report endpoint"""
    client, user = authenticated_client
    category, supplier, location, reagent = report_test_data

    stock_lot = StockLot.objects.create(
        reagent=reagent, lot_number='LOT-WL-001', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=30),
        purchase_price=10, initial_quantity=100, current_quantity=100
    )

    with freeze_time("2025-01-20"):
        StockMovement.objects.create(
            stock_lot=stock_lot, user=user, quantity=15, move_type='Descarte'
        )
    with freeze_time("2025-02-15"):
        StockMovement.objects.create(
            stock_lot=stock_lot, user=user, quantity=-10, move_type='Ajuste'  # Negative adjustment
        )

    start_date = "2025-01-01"
    end_date = "2025-02-28"
    response = client.get(f'/api/v1/reports/waste-loss/?start_date={start_date}&end_date={end_date}')

    assert response.status_code == 200
    assert len(response.data) == 2
    
    # Find the adjustment record
    adjustment_record = next((item for item in response.data if item['move_type'] == 'Ajuste'), None)
    assert adjustment_record is not None
    assert float(adjustment_record['total_quantity']) == -10.0
    
    # Find the discard record
    discard_record = next((item for item in response.data if item['move_type'] == 'Descarte'), None)
    assert discard_record is not None
    assert float(discard_record['total_quantity']) == 15.0

@pytest.mark.django_db
def test_stock_value_report(authenticated_client, report_test_data):
    """Test the stock value report endpoint"""
    client, user = authenticated_client
    category, supplier, location, reagent = report_test_data

    StockLot.objects.create(
        reagent=reagent, lot_number='LOT-SV-001', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=30),
        purchase_price=100, initial_quantity=10, current_quantity=10
    )
    StockLot.objects.create(
        reagent=reagent, lot_number='LOT-SV-002', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=60),
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
    assert response_cat.data[0]['reagent__category__name'] == category.name
    assert float(response_cat.data[0]['total_value']) == 1250.0

    # Test grouped by location
    response_loc = client.get('/api/v1/reports/stock-value/?group_by=location')
    assert response_loc.status_code == 200
    assert len(response_loc.data) == 1
    assert response_loc.data[0]['location__name'] == location.name
    assert float(response_loc.data[0]['total_value']) == 1250.0

    # Test invalid group_by parameter
    response_invalid = client.get('/api/v1/reports/stock-value/?group_by=invalid')
    assert response_invalid.status_code == 400

@pytest.mark.django_db
def test_expiry_report(authenticated_client, report_test_data):
    """Test the expiry report endpoint"""
    client, user = authenticated_client
    category, supplier, location, reagent = report_test_data

    # Lot expiring soon
    StockLot.objects.create(
        reagent=reagent, lot_number='LOT-EXP-001', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=5),  # Expires in 5 days
        purchase_price=10, initial_quantity=100, current_quantity=100
    )
    # Lot expiring later
    StockLot.objects.create(
        reagent=reagent, lot_number='LOT-EXP-002', location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=60),  # Expires in 60 days
        purchase_price=10, initial_quantity=100, current_quantity=100
    )
    # Expired lot
    StockLot.objects.create(
        reagent=reagent, lot_number='LOT-EXP-003', location=location,
        expiry_date=timezone.now().date() - datetime.timedelta(days=5),  # Expired 5 days ago
        purchase_price=10, initial_quantity=100, current_quantity=100
    )

    # Test upcoming expiry (default 30 days)
    response_upcoming = client.get('/api/v1/reports/expiry/')
    assert response_upcoming.status_code == 200
    assert len(response_upcoming.data) >= 2  # Should include LOT-EXP-001 and LOT-EXP-002

    # Test specific days until expiry
    response_specific = client.get('/api/v1/reports/expiry/?days_until_expiry=10')
    assert response_specific.status_code == 200
    assert len(response_specific.data) >= 1
    # Check if LOT-EXP-001 is in the response (expires in 5 days)
    lot_numbers = [item['lot_number'] for item in response_specific.data]
    assert 'LOT-EXP-001' in lot_numbers

    # Test expired lots
    response_expired = client.get('/api/v1/reports/expiry/?expired=true')
    assert response_expired.status_code == 200
    assert len(response_expired.data) >= 1
    # Check if LOT-EXP-003 is in the response (expired)
    expired_lot_numbers = [item['lot_number'] for item in response_expired.data]
    assert 'LOT-EXP-003' in expired_lot_numbers

@pytest.mark.django_db
def test_expiry_report_invalid_parameters(authenticated_client, report_test_data):
    """Test the expiry report with invalid parameters"""
    client, user = authenticated_client
    category, supplier, location, reagent = report_test_data

    # Test invalid days_until_expiry parameter
    response_invalid = client.get('/api/v1/reports/expiry/?days_until_expiry=invalid')
    assert response_invalid.status_code == 400