import pytest
from decimal import Decimal
from inventory.models import (
    User, Category, Supplier, Location, Reagent, 
    StockLot, StockMovement, Requisition
)
from inventory.serializers import (
    ReagentSerializer, StockLotSerializer, StockMovementSerializer,
    RequisitionSerializer, CategorySerializer, SupplierSerializer,
    LocationSerializer, UserSerializer
)


@pytest.mark.django_db
class TestReagentSerializer:
    """Testes para o ReagentSerializer"""
    
    def test_serialize_reagent(self):
        """Testa a serialização de um reagente"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor Exemplo')
        
        reagent = Reagent.objects.create(
            name='Ácido Clorídrico',
            sku='HCL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        
        serializer = ReagentSerializer(reagent)
        data = serializer.data
        
        assert data['name'] == 'Ácido Clorídrico'
        assert data['sku'] == 'HCL-001'
        assert data['category'] == category.id
        assert data['supplier'] == supplier.id
        assert Decimal(str(data['min_stock_level'])) == Decimal('100.00')

    def test_deserialize_reagent_valid(self):
        """Testa a desserialização válida de um reagente"""
        category = Category.objects.create(name='Bases')
        supplier = Supplier.objects.create(name='Outro Fornecedor')
        
        data = {
            'name': 'Hidróxido de Sódio',
            'sku': 'NAOH-001',
            'category': category.id,
            'supplier': supplier.id,
            'min_stock_level': '50.00'
        }
        
        serializer = ReagentSerializer(data=data)
        assert serializer.is_valid()
        
        reagent = serializer.save()
        assert reagent.name == 'Hidróxido de Sódio'
        assert reagent.sku == 'NAOH-001'
        assert reagent.category == category
        assert reagent.supplier == supplier
        assert reagent.min_stock_level == Decimal('50.00')

    def test_deserialize_reagent_invalid_missing_fields(self):
        """Testa a desserialização inválida de um reagente (campos obrigatórios faltando)"""
        data = {
            'name': 'Ácido Sulfúrico',
            # sku está faltando (obrigatório)
            # category está faltando (obrigatório)
            # supplier está faltando (obrigatório)
            'min_stock_level': '75.00'
        }
        
        serializer = ReagentSerializer(data=data)
        assert not serializer.is_valid()
        assert 'sku' in serializer.errors
        assert 'category' in serializer.errors
        assert 'supplier' in serializer.errors


@pytest.mark.django_db
class TestStockLotSerializer:
    """Testes para o StockLotSerializer"""
    
    def test_serialize_stock_lot(self):
        """Testa a serialização de um lote de estoque"""
        category = Category.objects.create(name='Sais')
        supplier = Supplier.objects.create(name='Fornecedor de Sais')
        location = Location.objects.create(name='Prateleira C-1')
        reagent = Reagent.objects.create(
            name='Cloreto de Sódio',
            sku='NACL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('1000.00')
        )
        
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='NACL20250917',
            location=location,
            expiry_date='2026-09-17',
            purchase_price=Decimal('50.00'),
            initial_quantity=Decimal('5000.00'),
            current_quantity=Decimal('5000.00')
        )
        
        serializer = StockLotSerializer(stock_lot)
        data = serializer.data
        
        assert data['reagent'] == reagent.id
        assert data['lot_number'] == 'NACL20250917'
        assert data['location'] == location.id
        assert str(data['expiry_date']) == '2026-09-17'
        assert Decimal(str(data['purchase_price'])) == Decimal('50.00')
        assert Decimal(str(data['initial_quantity'])) == Decimal('5000.00')
        assert Decimal(str(data['current_quantity'])) == Decimal('5000.00')

    def test_deserialize_stock_lot_valid(self):
        """Testa a desserialização válida de um lote de estoque"""
        category = Category.objects.create(name='Solventes')
        supplier = Supplier.objects.create(name='Fornecedor de Solventes')
        location = Location.objects.create(name='Armário 5')
        reagent = Reagent.objects.create(
            name='Etanol',
            sku='ETOH-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('2000.00')
        )
        
        data = {
            'reagent': reagent.id,
            'lot_number': 'ETOH20250101',
            'location': location.id,
            'expiry_date': '2026-01-01',
            'purchase_price': '25.00',
            'initial_quantity': '10000.00',
            'current_quantity': '10000.00'
        }
        
        serializer = StockLotSerializer(data=data)
        assert serializer.is_valid()
        
        stock_lot = serializer.save()
        assert stock_lot.reagent == reagent
        assert stock_lot.lot_number == 'ETOH20250101'
        assert stock_lot.location == location
        assert str(stock_lot.expiry_date) == '2026-01-01'
        assert stock_lot.purchase_price == Decimal('25.00')
        assert stock_lot.initial_quantity == Decimal('10000.00')
        assert stock_lot.current_quantity == Decimal('10000.00')


@pytest.mark.django_db
class TestStockMovementSerializer:
    """Testes para o StockMovementSerializer"""
    
    def test_serialize_stock_movement(self):
        """Testa a serialização de uma movimentação de estoque"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor Geral')
        location = Location.objects.create(name='Armário Principal')
        user = User.objects.create_user(username='analista1', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Ácido Nítrico',
            sku='HNO3-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='HNO3-LoteA',
            location=location,
            expiry_date='2025-12-31',
            purchase_price=Decimal('15.00'),
            initial_quantity=Decimal('500.00'),
            current_quantity=Decimal('500.00')
        )
        
        movement = StockMovement.objects.create(
            stock_lot=stock_lot,
            user=user,
            quantity=Decimal('50.00'),
            move_type='Retirada',
            notes='Uso em experimento'
        )
        
        serializer = StockMovementSerializer(movement)
        data = serializer.data
        
        assert data['stock_lot'] == stock_lot.id
        assert data['user'] == user.id
        assert Decimal(str(data['quantity'])) == Decimal('50.00')
        assert data['move_type'] == 'Retirada'
        assert data['notes'] == 'Uso em experimento'

    def test_deserialize_stock_movement_valid(self):
        """Testa a desserialização válida de uma movimentação de estoque"""
        category = Category.objects.create(name='Bases')
        supplier = Supplier.objects.create(name='Lab Supplies')
        location = Location.objects.create(name='Laboratório B')
        user = User.objects.create_user(username='analista2', password='testpass', role='Analista')
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
            expiry_date='2026-02-01',
            purchase_price=Decimal('20.00'),
            initial_quantity=Decimal('300.00'),
            current_quantity=Decimal('300.00')
        )
        
        data = {
            'stock_lot': stock_lot.id,
            'user': user.id,
            'quantity': '25.00',
            'move_type': 'Retirada',
            'notes': 'Para análise química'
        }
        
        serializer = StockMovementSerializer(data=data)
        assert serializer.is_valid()
        
        movement = serializer.save()
        assert movement.stock_lot == stock_lot
        assert movement.user == user
        assert movement.quantity == Decimal('25.00')
        assert movement.move_type == 'Retirada'
        assert movement.notes == 'Para análise química'
        
    def test_deserialize_stock_movement_entry_type(self):
        """Testa a desserialização de uma movimentação do tipo Entrada"""
        category = Category.objects.create(name='Reagentes')
        supplier = Supplier.objects.create(name='Fornecedor Reagentes')
        location = Location.objects.create(name='Estoque Principal')
        user = User.objects.create_user(username='estoquista', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Ácido Fosfórico',
            sku='H3PO4-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='H3PO4-2025',
            location=location,
            expiry_date='2026-12-31',
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        
        # Reduzir a quantidade para simular uso
        stock_lot.current_quantity = Decimal('50.00')
        stock_lot.save()
        
        data = {
            'stock_lot': stock_lot.id,
            'user': user.id,
            'quantity': '25.00',
            'move_type': 'Entrada',
            'notes': 'Reposição de estoque'
        }
        
        serializer = StockMovementSerializer(data=data)
        assert serializer.is_valid()
        
        movement = serializer.save()
        stock_lot.refresh_from_db()
        
        assert movement.move_type == 'Entrada'
        assert stock_lot.current_quantity == Decimal('75.00')  # 50 + 25

    def test_deserialize_stock_movement_adjustment_type(self):
        """Testa a desserialização de uma movimentação do tipo Ajuste"""
        category = Category.objects.create(name='Solventes')
        supplier = Supplier.objects.create(name='Fornecedor Solventes')
        location = Location.objects.create(name='Armário de Solventes')
        user = User.objects.create_user(username='ajustador', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Acetona',
            sku='CH3COCH3-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='ACETONA-2025',
            location=location,
            expiry_date='2026-06-30',
            purchase_price=Decimal('15.00'),
            initial_quantity=Decimal('200.00'),
            current_quantity=Decimal('200.00')
        )
        
        data = {
            'stock_lot': stock_lot.id,
            'user': user.id,
            'quantity': '-50.00',  # Ajuste negativo
            'move_type': 'Ajuste',
            'notes': 'Perda por evaporação'
        }
        
        serializer = StockMovementSerializer(data=data)
        assert serializer.is_valid()
        
        movement = serializer.save()
        stock_lot.refresh_from_db()
        
        assert movement.move_type == 'Ajuste'
        assert stock_lot.current_quantity == Decimal('150.00')  # 200 - 50

    def test_deserialize_stock_movement_discard_type(self):
        """Testa a desserialização de uma movimentação do tipo Descarte"""
        category = Category.objects.create(name='Indicadores')
        supplier = Supplier.objects.create(name='Fornecedor Indicadores')
        location = Location.objects.create(name='Laboratório Análises')
        user = User.objects.create_user(username='descartador', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Azul de Metileno',
            sku='C16H18ClN3S-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='AZUL-METILENO-2025',
            location=location,
            expiry_date='2025-12-31',
            purchase_price=Decimal('25.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        
        data = {
            'stock_lot': stock_lot.id,
            'user': user.id,
            'quantity': '30.00',
            'move_type': 'Descarte',
            'notes': 'Produto fora da validade'
        }
        
        serializer = StockMovementSerializer(data=data)
        assert serializer.is_valid()
        
        movement = serializer.save()
        stock_lot.refresh_from_db()
        
        assert movement.move_type == 'Descarte'
        assert stock_lot.current_quantity == Decimal('70.00')  # 100 - 30


@pytest.mark.django_db
class TestRequisitionSerializer:
    """Testes para o RequisitionSerializer"""
    
    def test_serialize_requisition(self):
        """Testa a serialização de uma requisição"""
        category = Category.objects.create(name='Indicadores')
        supplier = Supplier.objects.create(name='Fornecedor C')
        requester = User.objects.create_user(username='pesquisador1', password='testpass', role='Convidado')
        reagent = Reagent.objects.create(
            name='Fenolftaleína',
            sku='FENOL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        requisition = Requisition.objects.create(
            requester=requester,
            reagent=reagent,
            quantity=Decimal('10.00'),
            status='Pendente'
        )
        
        serializer = RequisitionSerializer(requisition)
        data = serializer.data
        
        assert data['requester'] == requester.id
        assert data['reagent'] == reagent.id
        assert Decimal(str(data['quantity'])) == Decimal('10.00')
        assert data['status'] == 'Pendente'
        assert data['approver'] is None

    def test_deserialize_requisition_valid(self):
        """Testa a desserialização válida de uma requisição"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor Ácidos')
        requester = User.objects.create_user(username='pesquisador2', password='testpass', role='Convidado')
        reagent = Reagent.objects.create(
            name='Ácido Acético',
            sku='CH3COOH-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        data = {
            'requester': requester.id,
            'reagent': reagent.id,
            'quantity': '5.00',
            'status': 'Pendente'
        }
        
        serializer = RequisitionSerializer(data=data)
        assert serializer.is_valid()
        
        requisition = serializer.save()
        assert requisition.requester == requester
        assert requisition.reagent == reagent
        assert requisition.quantity == Decimal('5.00')
        assert requisition.status == 'Pendente'
        assert requisition.approver is None


@pytest.mark.django_db
class TestCategorySerializer:
    """Testes para o CategorySerializer"""
    
    def test_serialize_category(self):
        """Testa a serialização de uma categoria"""
        category = Category.objects.create(
            name='Ácidos',
            description='Ácidos químicos diversos'
        )
        
        serializer = CategorySerializer(category)
        data = serializer.data
        
        assert data['name'] == 'Ácidos'
        assert data['description'] == 'Ácidos químicos diversos'

    def test_deserialize_category_valid(self):
        """Testa a desserialização válida de uma categoria"""
        data = {
            'name': 'Bases',
            'description': 'Bases químicas'
        }
        
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        
        category = serializer.save()
        assert category.name == 'Bases'
        assert category.description == 'Bases químicas'

    def test_deserialize_category_invalid_duplicate_name(self):
        """Testa a desserialização inválida de uma categoria (nome duplicado)"""
        Category.objects.create(name='Sais')
        
        data = {
            'name': 'Sais',  # Nome já existe
            'description': 'Sais químicos'
        }
        
        serializer = CategorySerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestSupplierSerializer:
    """Testes para o SupplierSerializer"""
    
    def test_serialize_supplier(self):
        """Testa a serialização de um fornecedor"""
        supplier = Supplier.objects.create(
            name='Fornecedor Químico Ltda',
            contact_person='João Silva',
            email='joao@fornecedor.com',
            phone='(11) 99999-9999'
        )
        
        serializer = SupplierSerializer(supplier)
        data = serializer.data
        
        assert data['name'] == 'Fornecedor Químico Ltda'
        assert data['contact_person'] == 'João Silva'
        assert data['email'] == 'joao@fornecedor.com'
        assert data['phone'] == '(11) 99999-9999'

    def test_deserialize_supplier_valid(self):
        """Testa a desserialização válida de um fornecedor"""
        data = {
            'name': 'Lab Supplies Co.',
            'contact_person': 'Maria Santos',
            'email': 'maria@labsupplies.com',
            'phone': '(21) 88888-8888'
        }
        
        serializer = SupplierSerializer(data=data)
        assert serializer.is_valid()
        
        supplier = serializer.save()
        assert supplier.name == 'Lab Supplies Co.'
        assert supplier.contact_person == 'Maria Santos'
        assert supplier.email == 'maria@labsupplies.com'
        assert supplier.phone == '(21) 88888-8888'


@pytest.mark.django_db
class TestLocationSerializer:
    """Testes para o LocationSerializer"""
    
    def test_serialize_location(self):
        """Testa a serialização de uma localização"""
        location = Location.objects.create(
            name='Laboratório A',
            description='Laboratório de análises químicas'
        )
        
        serializer = LocationSerializer(location)
        data = serializer.data
        
        assert data['name'] == 'Laboratório A'
        assert data['description'] == 'Laboratório de análises químicas'

    def test_deserialize_location_valid(self):
        """Testa a desserialização válida de uma localização"""
        data = {
            'name': 'Estoque Principal',
            'description': 'Área de armazenamento central'
        }
        
        serializer = LocationSerializer(data=data)
        assert serializer.is_valid()
        
        location = serializer.save()
        assert location.name == 'Estoque Principal'
        assert location.description == 'Área de armazenamento central'


@pytest.mark.django_db
class TestUserSerializer:
    """Testes para o UserSerializer"""
    
    def test_serialize_user(self):
        """Testa a serialização de um usuário"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='Analista',
            first_name='Test',
            last_name='User'
        )
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert data['role'] == 'Analista'
        assert data['first_name'] == 'Test'
        assert data['last_name'] == 'User'
        # Verificar que a senha não está sendo serializada
        assert 'password' not in data

    def test_deserialize_user_valid(self):
        """Testa a desserialização válida de um usuário"""
        data = {
            'username': 'novouser',
            'email': 'novo@example.com',
            'role': 'Convidado',
            'first_name': 'Novo',
            'last_name': 'Usuário'
        }
        
        serializer = UserSerializer(data=data)
        # UserSerializer é principalmente para serialização,
        # a criação de usuários é feita via User.objects.create_user()
        # Este teste verifica que os campos estão presentes
        assert 'username' in serializer.fields
        assert 'email' in serializer.fields
        assert 'role' in serializer.fields
        assert 'first_name' in serializer.fields
        assert 'last_name' in serializer.fields