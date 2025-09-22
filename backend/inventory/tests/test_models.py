import pytest
from django.test import TestCase
from django.db import IntegrityError
from inventory.models import (
    User, Category, Supplier, Location, Reagent, 
    StockLot, StockMovement, Attachment, AuditLog, 
    Requisition, Alert, Notification
)
import datetime
from decimal import Decimal


@pytest.mark.django_db
class TestUserModel:
    """Testes para o modelo User"""
    
    def test_create_user(self):
        """Testa a criação de um usuário"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='Analista'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'Analista'
        assert user.is_active is True
        assert user.check_password('testpass123') is True

    def test_create_superuser(self):
        """Testa a criação de um superusuário"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        assert admin.username == 'admin'
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.role == 'Convidado'  # Default role


@pytest.mark.django_db
class TestCategoryModel:
    """Testes para o modelo Category"""
    
    def test_create_category(self):
        """Testa a criação de uma categoria"""
        category = Category.objects.create(
            name='Ácidos',
            description='Ácidos químicos diversos'
        )
        
        assert category.name == 'Ácidos'
        assert category.description == 'Ácidos químicos diversos'
        assert str(category) == 'Ácidos'

    def test_category_unique_name(self):
        """Testa que nomes de categorias são únicos"""
        Category.objects.create(name='Bases')
        
        with pytest.raises(IntegrityError):
            Category.objects.create(name='Bases')


@pytest.mark.django_db
class TestSupplierModel:
    """Testes para o modelo Supplier"""
    
    def test_create_supplier(self):
        """Testa a criação de um fornecedor"""
        supplier = Supplier.objects.create(
            name='Fornecedor Químico Ltda',
            contact_person='João Silva',
            email='joao@fornecedor.com',
            phone='(11) 99999-9999'
        )
        
        assert supplier.name == 'Fornecedor Químico Ltda'
        assert supplier.contact_person == 'João Silva'
        assert supplier.email == 'joao@fornecedor.com'
        assert supplier.phone == '(11) 99999-9999'
        assert str(supplier) == 'Fornecedor Químico Ltda'


@pytest.mark.django_db
class TestLocationModel:
    """Testes para o modelo Location"""
    
    def test_create_location(self):
        """Testa a criação de uma localização"""
        location = Location.objects.create(
            name='Laboratório A',
            description='Laboratório de análises químicas'
        )
        
        assert location.name == 'Laboratório A'
        assert location.description == 'Laboratório de análises químicas'
        assert str(location) == 'Laboratório A'

    def test_location_unique_name(self):
        """Testa que nomes de localizações são únicos"""
        Location.objects.create(name='Estoque Principal')
        
        with pytest.raises(IntegrityError):
            Location.objects.create(name='Estoque Principal')


@pytest.mark.django_db
class TestReagentModel:
    """Testes para o modelo Reagent"""
    
    def test_create_reagent(self):
        """Testa a criação de um reagente"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor Químico')
        
        reagent = Reagent.objects.create(
            name='Ácido Clorídrico',
            sku='HCL-001',
            category=category,
            supplier=supplier,
            storage_conditions='Armazenar em local seco',
            min_stock_level=Decimal('50.00')
        )
        
        assert reagent.name == 'Ácido Clorídrico'
        assert reagent.sku == 'HCL-001'
        assert reagent.category == category
        assert reagent.supplier == supplier
        assert reagent.storage_conditions == 'Armazenar em local seco'
        assert reagent.min_stock_level == Decimal('50.00')
        assert str(reagent) == 'Ácido Clorídrico'

    def test_reagent_unique_sku(self):
        """Testa que SKUs de reagentes são únicos"""
        category = Category.objects.create(name='Bases')
        supplier = Supplier.objects.create(name='Lab Supplies')
        
        Reagent.objects.create(
            name='Hidróxido de Sódio',
            sku='NAOH-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        
        with pytest.raises(IntegrityError):
            Reagent.objects.create(
                name='Outro Hidróxido de Sódio',
                sku='NAOH-001',
                category=category,
                supplier=supplier,
                min_stock_level=Decimal('50.00')
            )


@pytest.mark.django_db
class TestStockLotModel:
    """Testes para o modelo StockLot"""
    
    def test_create_stock_lot(self):
        """Testa a criação de um lote de estoque"""
        category = Category.objects.create(name='Sais')
        supplier = Supplier.objects.create(name='Química Ltda')
        location = Location.objects.create(name='Prateleira 1')
        reagent = Reagent.objects.create(
            name='Cloreto de Sódio',
            sku='NACL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('200.00')
        )
        
        lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='NACL20250101',
            location=location,
            expiry_date=datetime.date(2026, 1, 1),
            purchase_price=Decimal('25.00'),
            initial_quantity=Decimal('1000.00'),
            current_quantity=Decimal('1000.00')
        )
        
        assert lot.reagent == reagent
        assert lot.lot_number == 'NACL20250101'
        assert lot.location == location
        assert lot.expiry_date == datetime.date(2026, 1, 1)
        assert lot.purchase_price == Decimal('25.00')
        assert lot.initial_quantity == Decimal('1000.00')
        assert lot.current_quantity == Decimal('1000.00')
        assert str(lot) == 'Cloreto de Sódio - Lote: NACL20250101'

    def test_stock_lot_unique_together(self):
        """Testa a restrição única de reagente + número do lote"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor A')
        location = Location.objects.create(name='Armário 1')
        reagent = Reagent.objects.create(
            name='Ácido Sulfúrico',
            sku='H2SO4-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('150.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='H2SO4-LOT1',
            location=location,
            expiry_date=datetime.date(2026, 6, 1),
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('500.00'),
            current_quantity=Decimal('500.00')
        )
        
        # Tentar criar outro lote com o mesmo reagente e número do lote
        with pytest.raises(IntegrityError):
            StockLot.objects.create(
                reagent=reagent,
                lot_number='H2SO4-LOT1',
                location=location,
                expiry_date=datetime.date(2026, 12, 1),
                purchase_price=Decimal('30.00'),
                initial_quantity=Decimal('300.00'),
                current_quantity=Decimal('300.00')
            )


@pytest.mark.django_db
class TestStockMovementModel:
    """Testes para o modelo StockMovement"""
    
    def test_create_stock_movement(self):
        """Testa a criação de uma movimentação de estoque"""
        category = Category.objects.create(name='Bases')
        supplier = Supplier.objects.create(name='Fornecedor B')
        location = Location.objects.create(name='Laboratório B')
        user = User.objects.create_user(
            username='analista1',
            password='testpass123',
            role='Analista'
        )
        reagent = Reagent.objects.create(
            name='Hidróxido de Potássio',
            sku='KOH-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('75.00')
        )
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='KOH20250201',
            location=location,
            expiry_date=datetime.date(2026, 2, 1),
            purchase_price=Decimal('20.00'),
            initial_quantity=Decimal('500.00'),
            current_quantity=Decimal('500.00')
        )
        
        movement = StockMovement.objects.create(
            stock_lot=stock_lot,
            user=user,
            quantity=Decimal('50.00'),
            move_type='Retirada',
            notes='Para experimento X'
        )
        
        assert movement.stock_lot == stock_lot
        assert movement.user == user
        assert movement.quantity == Decimal('50.00')
        assert movement.move_type == 'Retirada'
        assert movement.notes == 'Para experimento X'
        assert str(movement) == 'Retirada de 50.00 no Hidróxido de Potássio - Lote: KOH20250201'


@pytest.mark.django_db
class TestRequisitionModel:
    """Testes para o modelo Requisition"""
    
    def test_create_requisition(self):
        """Testa a criação de uma requisição"""
        category = Category.objects.create(name='Indicadores')
        supplier = Supplier.objects.create(name='Fornecedor C')
        user_requester = User.objects.create_user(
            username='pesquisador1',
            password='testpass123',
            role='Convidado'
        )
        user_approver = User.objects.create_user(
            username='supervisor1',
            password='testpass123',
            role='Analista'
        )
        reagent = Reagent.objects.create(
            name='Fenolftaleína',
            sku='FENOL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        requisition = Requisition.objects.create(
            requester=user_requester,
            reagent=reagent,
            quantity=Decimal('10.00'),
            status='Pendente'
        )
        
        assert requisition.requester == user_requester
        assert requisition.reagent == reagent
        assert requisition.quantity == Decimal('10.00')
        assert requisition.status == 'Pendente'
        assert requisition.approver is None
        assert str(requisition) == 'Requisição de Fenolftaleína por pesquisador1'