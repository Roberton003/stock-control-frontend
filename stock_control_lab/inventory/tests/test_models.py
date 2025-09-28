from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from inventory.models import Produto, MovimentacaoEstoque, Category, Supplier, Location, User, StockLot

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='USER'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'USER')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_admin_user(self):
        admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            role='ADMIN'
        )
        self.assertEqual(admin_user.role, 'ADMIN')

    def test_user_string_representation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='USER'
        )
        self.assertEqual(str(user), 'testuser')


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')

    def test_category_unique_name(self):
        Category.objects.create(name='Unique Category')
        with self.assertRaises(Exception):
            Category.objects.create(name='Unique Category')  # Should raise due to unique constraint

    def test_category_string_representation(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')


class SupplierModelTest(TestCase):
    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_person='John Doe',
            email='john@example.com',
            phone='123456789'
        )
        self.assertEqual(supplier.name, 'Test Supplier')
        self.assertEqual(supplier.contact_person, 'John Doe')
        self.assertEqual(supplier.email, 'john@example.com')
        self.assertEqual(supplier.phone, '123456789')

    def test_supplier_string_representation(self):
        supplier = Supplier.objects.create(name='Test Supplier')
        self.assertEqual(str(supplier), 'Test Supplier')


class LocationModelTest(TestCase):
    def test_create_location(self):
        location = Location.objects.create(
            name='Test Location',
            description='Test Description'
        )
        self.assertEqual(location.name, 'Test Location')
        self.assertEqual(location.description, 'Test Description')

    def test_location_unique_name(self):
        Location.objects.create(name='Unique Location')
        with self.assertRaises(Exception):
            Location.objects.create(name='Unique Location')  # Should raise due to unique constraint

    def test_location_string_representation(self):
        location = Location.objects.create(name='Test Location')
        self.assertEqual(str(location), 'Test Location')


class ProdutoModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.supplier = Supplier.objects.create(name='Test Supplier')

    def test_create_produto(self):
        produto = Produto.objects.create(
            nome='Test Produto',
            descricao='Test Description',
            sku='TEST-001',
            quantidade=10,
            category=self.category,
            fornecedor=self.supplier,
            data_validade='2025-12-31'
        )
        self.assertEqual(produto.nome, 'Test Produto')
        self.assertEqual(produto.descricao, 'Test Description')
        self.assertEqual(produto.sku, 'TEST-001')
        self.assertEqual(produto.quantidade, 10)
        self.assertEqual(produto.category, self.category)
        self.assertEqual(produto.fornecedor, self.supplier)
        self.assertEqual(str(produto.data_validade), '2025-12-31')

    def test_produto_string_representation(self):
        produto = Produto.objects.create(
            nome='Test Produto',
            sku='TEST-001',
            category=self.category,
            fornecedor=self.supplier,
            quantidade=10
        )
        self.assertEqual(str(produto), 'Test Produto')

    def test_produto_unique_sku(self):
        Produto.objects.create(
            nome='Test Produto 1',
            sku='TEST-001',
            category=self.category,
            fornecedor=self.supplier,
            quantidade=10
        )
        with self.assertRaises(Exception):
            Produto.objects.create(
                nome='Test Produto 2',
                sku='TEST-001',  # Same SKU as above
                category=self.category,
                fornecedor=self.supplier,
                quantidade=5
            )


class StockLotModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.location = Location.objects.create(name='Test Location')
        self.produto = Produto.objects.create(
            nome='Test Produto',
            sku='TEST-001',
            category=self.category,
            fornecedor=self.supplier,
            quantidade=10
        )

    def test_create_stock_lot(self):
        stock_lot = StockLot.objects.create(
            produto=self.produto,
            lot_number='LOT-001',
            location=self.location,
            expiry_date='2025-12-31',
            purchase_price=100.00,
            initial_quantity=50.00,
            current_quantity=50.00
        )
        self.assertEqual(stock_lot.produto, self.produto)
        self.assertEqual(stock_lot.lot_number, 'LOT-001')
        self.assertEqual(stock_lot.location, self.location)
        self.assertEqual(str(stock_lot.expiry_date), '2025-12-31')
        self.assertEqual(stock_lot.purchase_price, 100.00)
        self.assertEqual(stock_lot.initial_quantity, 50.00)
        self.assertEqual(stock_lot.current_quantity, 50.00)

    def test_stock_lot_string_representation(self):
        stock_lot = StockLot.objects.create(
            produto=self.produto,
            lot_number='LOT-001',
            location=self.location,
            expiry_date='2025-12-31',
            purchase_price=100.00,
            initial_quantity=50.00,
            current_quantity=50.00
        )
        self.assertEqual(str(stock_lot), f'{self.produto.nome} - Lote: LOT-001')

    def test_unique_produto_lot_number_constraint(self):
        StockLot.objects.create(
            produto=self.produto,
            lot_number='LOT-001',
            location=self.location,
            expiry_date='2025-12-31',
            purchase_price=100.00,
            initial_quantity=50.00,
            current_quantity=50.00
        )
        with self.assertRaises(Exception):
            StockLot.objects.create(
                produto=self.produto,
                lot_number='LOT-001',  # Same combination of produto and lot_number
                location=self.location,
                expiry_date='2025-12-31',
                purchase_price=100.00,
                initial_quantity=30.00,
                current_quantity=30.00
            )


class MovimentacaoEstoqueModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.produto = Produto.objects.create(
            nome='Test Produto',
            sku='TEST-001',
            category=self.category,
            fornecedor=self.supplier,
            quantidade=10
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='USER'
        )

    def test_create_movimentacao_estoque(self):
        movimentacao = MovimentacaoEstoque.objects.create(
            produto=self.produto,
            quantidade=5.00,
            tipo='SAIDA',
            usuario=self.user
        )
        self.assertEqual(movimentacao.produto, self.produto)
        self.assertEqual(movimentacao.quantidade, 5.00)
        self.assertEqual(movimentacao.tipo, 'SAIDA')
        self.assertEqual(movimentacao.usuario, self.user)

    def test_movimentacao_estoque_tipo_choices(self):
        movimentacao_entrada = MovimentacaoEstoque.objects.create(
            produto=self.produto,
            quantidade=10.00,
            tipo='ENTRADA',
            usuario=self.user
        )
        movimentacao_saida = MovimentacaoEstoque.objects.create(
            produto=self.produto,
            quantidade=5.00,
            tipo='SAIDA',
            usuario=self.user
        )
        self.assertEqual(movimentacao_entrada.tipo, 'ENTRADA')
        self.assertEqual(movimentacao_saida.tipo, 'SAIDA')

    def test_movimentacao_estoque_string_representation(self):
        movimentacao = MovimentacaoEstoque.objects.create(
            produto=self.produto,
            quantidade=5.00,
            tipo='SAIDA',
            usuario=self.user
        )
        # The actual string representation may format the decimal differently (e.g., '5.0' instead of '5.00')
        # So we check that it contains the expected elements
        result_str = str(movimentacao)
        self.assertIn('SAIDA', result_str)
        self.assertIn(self.produto.nome, result_str)
        # Check if it contains the quantity (allowing for different decimal formatting)
        self.assertTrue('5.0' in result_str or '5.00' in result_str)
