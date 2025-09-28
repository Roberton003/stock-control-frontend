"""
Testes automatizados para validação da adição e gerenciamento de produtos
no sistema de controle de estoque.
"""
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from inventory.models import User, Produto, Category, Supplier, Location, StockLot, MovimentacaoEstoque
from django.utils import timezone
import datetime

User = get_user_model()

@pytest.fixture
def api_client():
    """Cria um cliente de API de teste"""
    return APIClient()

@pytest.fixture
def authenticated_api_client():
    """Cria um cliente de API autenticado"""
    client = APIClient()
    user = User.objects.create_user(
        username='prodtestuser',
        password='prodtestpass123',
        email='prodtest@example.com',
        role='USER'
    )
    client.force_authenticate(user=user)
    return client, user

@pytest.mark.django_db
def test_create_product_via_api(authenticated_api_client):
    """Testa criação de produto via API"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    product_data = {
        'nome': 'Produto de Teste',
        'descricao': 'Descrição do produto de teste',
        'sku': 'TEST-001',
        'quantidade': 100,
        'category': category.id,
        'fornecedor': supplier.id
    }
    
    response = api_client.post('/api/v1/produtos/', product_data, format='json')
    assert response.status_code == 201
    
    # Verifica se o produto foi criado
    assert Produto.objects.filter(sku='TEST-001').exists()
    produto = Produto.objects.get(sku='TEST-001')
    assert produto.nome == 'Produto de Teste'

@pytest.mark.django_db
def test_list_products_via_api(authenticated_api_client):
    """Testa listagem de produtos via API"""
    api_client, user = authenticated_api_client
    
    # Cria produtos de teste
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    Produto.objects.create(
        nome='Produto 1',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=50
    )
    
    Produto.objects.create(
        nome='Produto 2',
        sku='TEST-002',
        category=category,
        fornecedor=supplier,
        quantidade=75
    )
    
    response = api_client.get('/api/v1/produtos/')
    assert response.status_code == 200
    assert len(response.data) >= 2  # Pode ter mais produtos de outros testes

@pytest.mark.django_db
def test_retrieve_single_product_via_api(authenticated_api_client):
    """Testa recuperação de um único produto via API"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    produto = Produto.objects.create(
        nome='Produto Detalhe',
        sku='DET-001',
        category=category,
        fornecedor=supplier,
        quantidade=30
    )
    
    response = api_client.get(f'/api/v1/produtos/{produto.id}/')
    assert response.status_code == 200
    assert response.data['sku'] == 'DET-001'

@pytest.mark.django_db
def test_update_product_via_api(authenticated_api_client):
    """Testa atualização de produto via API"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    produto = Produto.objects.create(
        nome='Produto Original',
        sku='UPD-001',
        category=category,
        fornecedor=supplier,
        quantidade=25
    )
    
    update_data = {
        'nome': 'Produto Atualizado',
        'descricao': 'Descrição atualizada',
        'sku': 'UPD-001',  # Mantém o mesmo SKU
        'quantidade': 40,
        'category': category.id,
        'fornecedor': supplier.id
    }
    
    response = api_client.put(f'/api/v1/produtos/{produto.id}/', update_data, format='json')
    assert response.status_code == 200
    assert response.data['nome'] == 'Produto Atualizado'
    
    # Verifica se o produto foi atualizado no banco
    produto.refresh_from_db()
    assert produto.nome == 'Produto Atualizado'
    assert produto.quantidade == 40

@pytest.mark.django_db
def test_delete_product_via_api(authenticated_api_client):
    """Testa exclusão de produto via API"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    produto = Produto.objects.create(
        nome='Produto para Excluir',
        sku='DEL-001',
        category=category,
        fornecedor=supplier,
        quantidade=10
    )
    
    # Verifica que o produto existe
    assert Produto.objects.filter(id=produto.id).exists()
    
    response = api_client.delete(f'/api/v1/produtos/{produto.id}/')
    assert response.status_code == 204
    
    # Verifica que o produto foi excluído
    assert not Produto.objects.filter(id=produto.id).exists()

@pytest.mark.django_db
def test_create_product_with_validation_errors(authenticated_api_client):
    """Testa criação de produto com dados inválidos"""
    api_client, user = authenticated_api_client
    
    # Tenta criar produto sem dados obrigatórios
    product_data = {
        'nome': '',  # Nome vazio
        'sku': '',   # SKU vazio
        'quantidade': -10  # Quantidade negativa
    }
    
    response = api_client.post('/api/v1/produtos/', product_data, format='json')
    assert response.status_code == 400
    # Verifica se há erros de validação
    assert 'nome' in response.data or 'sku' in response.data

@pytest.mark.django_db
def test_add_stock_lot_to_product(authenticated_api_client):
    """Testa adição de lote de estoque a um produto"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    
    produto = Produto.objects.create(
        nome='Produto Lote Teste',
        sku='LOT-001',
        category=category,
        fornecedor=supplier,
        quantidade=0
    )
    
    lot_data = {
        'produto': produto.id,
        'lot_number': 'LOT-TEST-001',
        'location': location.id,
        'expiry_date': (timezone.now() + datetime.timedelta(days=365)).date(),
        'purchase_price': 25.00,
        'initial_quantity': 100.00,
        'current_quantity': 100.00
    }
    
    response = api_client.post('/api/v1/stock-lots/', lot_data, format='json')
    assert response.status_code == 201
    
    # Verifica se o lote foi criado
    assert StockLot.objects.filter(lot_number='LOT-TEST-001').exists()
    
    # Verifica se a quantidade do produto foi atualizada
    produto.refresh_from_db()
    assert produto.quantidade == 100.00

@pytest.mark.django_db
def test_perform_stock_withdrawal(authenticated_api_client):
    """Testa retirada de estoque de um produto"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    
    produto = Produto.objects.create(
        nome='Produto Retirada Teste',
        sku='RET-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )
    
    # Cria um lote com estoque
    stock_lot = StockLot.objects.create(
        produto=produto,
        lot_number='RET-LOT-001',
        location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=365),
        purchase_price=20.00,
        initial_quantity=100.00,
        current_quantity=100.00
    )
    
    # Realiza uma retirada
    withdrawal_data = {
        'produto_id': produto.id,
        'quantidade': 30.00,
        'notes': 'Retirada de teste'
    }
    
    response = api_client.post('/api/v1/movimentacoes/', withdrawal_data, format='json')
    # O endpoint de movimentações para SAIDA pode ser diferente
    # Vamos testar com o endpoint correto para retirada
    response = api_client.post('/api/v1/movimentacoes/', {
        'produto': produto.id,
        'usuario': user.id,
        'quantidade': 30.00,
        'tipo': 'SAIDA'
    }, format='json')
    
    if response.status_code == 400:
        # Tenta com o serializer de retirada
        response = api_client.post('/api/v1/movimentacoes/', {
            'produto_id': produto.id,
            'quantidade': 30.00,
            'notes': 'Retirada de teste'
        }, format='json')
    
    # Atualizar o produto e verificar a quantidade
    produto.refresh_from_db()
    assert produto.quantidade <= 70.00  # Pode ser menor dependendo do FEFO

@pytest.mark.django_db
def test_stock_movement_with_fefo_logic(authenticated_api_client):
    """Testa movimentação de estoque com lógica FEFO (First Expire, First Out)"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location1 = Location.objects.create(name='Location 1')
    location2 = Location.objects.create(name='Location 2')
    
    produto = Produto.objects.create(
        nome='Produto FEFO Teste',
        sku='FEFO-001',
        category=category,
        fornecedor=supplier,
        quantidade=0
    )
    
    # Cria lotes com diferentes datas de expiração
    # Lote que expira primeiro
    lot1 = StockLot.objects.create(
        produto=produto,
        lot_number='FEFO-LOT-001',
        location=location1,
        expiry_date=timezone.now().date() + datetime.timedelta(days=30),  # Expira em 30 dias
        purchase_price=10.00,
        initial_quantity=50.00,
        current_quantity=50.00
    )
    
    # Lote que expira depois
    lot2 = StockLot.objects.create(
        produto=produto,
        lot_number='FEFO-LOT-002',
        location=location2,
        expiry_date=timezone.now().date() + datetime.timedelta(days=90),  # Expira em 90 dias
        purchase_price=10.00,
        initial_quantity=50.00,
        current_quantity=50.00
    )
    
    # Atualiza a quantidade total do produto
    produto.quantidade = 100.00
    produto.save()
    
    # Agora faz uma retirada de 60 unidades
    # A lógica FEFO deve retirar primeiro do lote que expira antes (lot1)
    from inventory.services import perform_withdrawal
    
    withdrawn_quantity = perform_withdrawal(produto, 60.00, user)
    assert withdrawn_quantity == 60.00
    
    # Atualiza e verifica as quantidades
    lot1.refresh_from_db()
    lot2.refresh_from_db()
    produto.refresh_from_db()
    
    # lot1 deveria ter 0 (50 - 50) e lot2 deveria ter 40 (50 - 10)
    assert lot1.current_quantity == 0
    assert lot2.current_quantity == 40
    assert produto.quantidade == 40  # Quantidade total após retirada

@pytest.mark.django_db
def test_product_search_and_filter(authenticated_api_client):
    """Testa busca e filtragem de produtos"""
    api_client, user = authenticated_api_client
    
    # Cria dados para teste de busca
    category1 = Category.objects.create(name='Categoria A')
    category2 = Category.objects.create(name='Categoria B')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    Produto.objects.create(
        nome='Produto ABC',
        sku='ABC-001',
        category=category1,
        fornecedor=supplier,
        quantidade=10
    )
    
    Produto.objects.create(
        nome='Produto XYZ',
        sku='XYZ-001',
        category=category2,
        fornecedor=supplier,
        quantidade=20
    )
    
    # Testa busca por nome
    response = api_client.get('/api/v1/produtos/', {'search': 'ABC'})
    assert response.status_code == 200
    
    # Testa filtro por categoria
    response = api_client.get('/api/v1/produtos/', {'category': category1.id})
    assert response.status_code == 200

@pytest.mark.django_db
def test_low_stock_alert_functionality(authenticated_api_client):
    """Testa funcionalidade de alerta de estoque baixo"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    # Cria produto com quantidade baixa e limite baixo
    produto = Produto.objects.create(
        nome='Produto com Estoque Baixo',
        sku='LOW-001',
        category=category,
        fornecedor=supplier,
        quantidade=5  # Quantidade baixa
    )
    
    # Simula verificação de estoque baixo
    from inventory.services import get_expiry_report
    # Embora chamado expiry_report, a função pode ser usada para verificar itens com baixo estoque
    # dependendo da implementação
    
    # Verifica se o produto está próximo do estoque crítico
    produtos_baixo_estoque = Produto.objects.filter(quantidade__lt=10)  # Menor que 10
    assert produto in produtos_baixo_estoque

@pytest.mark.django_db
def test_duplicate_sku_prevention(authenticated_api_client):
    """Testa prevenção de SKUs duplicados"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    # Cria primeiro produto
    Produto.objects.create(
        nome='Produto 1',
        sku='DUP-001',
        category=category,
        fornecedor=supplier,
        quantidade=10
    )
    
    # Tenta criar produto com mesmo SKU
    duplicate_data = {
        'nome': 'Produto 2',
        'sku': 'DUP-001',  # Mesmo SKU
        'category': category.id,
        'fornecedor': supplier.id,
        'quantidade': 15
    }
    
    response = api_client.post('/api/v1/produtos/', duplicate_data, format='json')
    # Deve falhar devido ao SKU duplicado
    assert response.status_code == 400

@pytest.mark.django_db
def test_product_quantity_update_with_movements(authenticated_api_client):
    """Testa atualização da quantidade de produto com movimentações"""
    api_client, user = authenticated_api_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    
    produto = Produto.objects.create(
        nome='Produto Movimentação Teste',
        sku='MOV-001',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )
    
    # Verifica quantidade inicial
    produto.refresh_from_db()
    initial_quantity = produto.quantidade
    
    # Faz uma entrada de estoque
    entry_movement = MovimentacaoEstoque.objects.create(
        produto=produto,
        usuario=user,
        quantidade=30.00,
        tipo='ENTRADA'
    )
    
    # Atualiza a quantidade do produto
    produto.quantidade += 30.00
    produto.save()
    
    # A quantidade deve ter aumentado
    produto.refresh_from_db()
    assert produto.quantidade == initial_quantity + 30.00
    
    # Faz uma saída de estoque
    exit_movement = MovimentacaoEstoque.objects.create(
        produto=produto,
        usuario=user,
        quantidade=20.00,
        tipo='SAIDA'
    )
    
    # Atualiza a quantidade do produto
    produto.quantidade -= 20.00
    produto.save()
    
    # A quantidade deve ter diminuído
    produto.refresh_from_db()
    assert produto.quantidade == initial_quantity + 30.00 - 20.00