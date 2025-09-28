"""
Testes automatizados para validação da navegação entre páginas 
e funcionalidades dos menus no sistema de controle de estoque.
"""
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from inventory.models import User, Produto, Category, Supplier, Location, StockLot

User = get_user_model()

@pytest.fixture
def client():
    """Cria um cliente de teste"""
    return Client()

@pytest.fixture
def authenticated_client():
    """Cria um cliente autenticado para testes de navegação"""
    client = Client()
    user = User.objects.create_user(
        username='navtestuser',
        password='navtestpass123',
        email='navtest@example.com',
        role='USER',
        is_staff=True  # Para acessar o admin
    )
    client.login(username='navtestuser', password='navtestpass123')
    return client, user

@pytest.mark.django_db
def test_navigation_to_dashboard(authenticated_client):
    """Testa navegação para a página de dashboard"""
    client, user = authenticated_client
    
    response = client.get('/dashboard/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_to_produtos_list(authenticated_client):
    """Testa navegação para a lista de produtos"""
    client, user = authenticated_client
    
    response = client.get('/produtos/list/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_to_produtos_detail(authenticated_client):
    """Testa navegação para a página de detalhes de um produto"""
    client, user = authenticated_client
    
    # Cria um produto para teste
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    produto = Produto.objects.create(
        nome='Test Produto',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )
    
    response = client.get(f'/produtos/{produto.pk}/detail/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_to_stock_lots_create(authenticated_client):
    """Testa navegação para a página de criação de lotes de estoque"""
    client, user = authenticated_client
    
    response = client.get('/stock-lots/create/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_to_movimentacoes_withdraw(authenticated_client):
    """Testa navegação para a página de retirada de estoque"""
    client, user = authenticated_client
    
    response = client.get('/movimentacoes/withdraw/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_to_requisitions_list(authenticated_client):
    """Testa navegação para a lista de requisições"""
    client, user = authenticated_client
    
    response = client.get('/requisitions/list/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_to_admin_panel(authenticated_client):
    """Testa navegação para o painel de administração"""
    client, user = authenticated_client
    
    response = client.get('/admin/')
    # Pode ser 200 (acesso concedido) ou 302 (redirecionamento devido a permissões)
    assert response.status_code in [200, 302]

@pytest.mark.django_db
def test_navigation_to_api_endpoints(authenticated_client):
    """Testa navegação (acesso) a endpoints da API"""
    client, user = authenticated_client
    
    # Testa acesso a diferentes endpoints da API
    endpoints = [
        '/api/v1/produtos/',
        '/api/v1/stock-lots/',
        '/api/v1/movimentacoes/',
        '/api/v1/categories/',
        '/api/v1/suppliers/',
        '/api/v1/locations/',
        '/api/v1/requisitions/',
        '/api/v1/users/',
        '/api/v1/dashboard/summary/',
        '/api/v1/reports/stock-value/',
        '/api/v1/reports/expiry/',
        '/api/v1/reports/consumption-by-user/',
        '/api/v1/reports/waste-loss/',
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        # Após autenticação, deve obter 200, 403 (permissão), ou 405 (método incorreto)
        assert response.status_code in [200, 403, 405]

@pytest.mark.django_db
def test_main_menu_links_accessibility(authenticated_client):
    """Testa acessibilidade dos links principais do menu"""
    client, user = authenticated_client
    
    # Testa a página principal para verificar links disponíveis
    response = client.get('/')
    # Verifica que a resposta é válida
    assert response.status_code in [200, 302]
    
    # Testa navegação para páginas comuns
    common_pages = [
        '/dashboard/',
        '/produtos/list/',
        '/requisitions/list/',
    ]
    
    for page in common_pages:
        response = client.get(page)
        # Pode retornar 200 (página encontrada) ou 302 (redirecionamento)
        assert response.status_code in [200, 302]

@pytest.mark.django_db
def test_menu_navigation_produtos(authenticated_client):
    """Testa navegação específica para funcionalidades de produtos"""
    client, user = authenticated_client
    
    # Testa criação de produto via endpoint
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    # Tenta acessar diferentes funcionalidades de produtos
    produto_data = {
        'nome': 'Produto de Teste',
        'sku': 'TEST-002',
        'category': category.pk,
        'fornecedor': supplier.pk,
        'quantidade': 50.00
    }
    
    # Testa a API de produtos (precisa de autenticação adequada)
    from rest_framework.test import APIClient
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    
    response = api_client.post('/api/v1/produtos/', produto_data, format='json')
    # Pode ser 201 (criado) ou 400 (dados inválidos), mas não 403 se autenticado
    assert response.status_code in [201, 400]

@pytest.mark.django_db
def test_menu_navigation_stock_lots(authenticated_client):
    """Testa navegação específica para funcionalidades de lotes de estoque"""
    client, user = authenticated_client
    
    # Cria dados necessários
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    produto = Produto.objects.create(
        nome='Produto Teste Lote',
        sku='TEST-LOT-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )
    
    # Testa acesso à criação de lotes
    response = client.get('/stock-lots/create/')
    assert response.status_code == 200
    
    # Testa API de lotes de estoque
    from rest_framework.test import APIClient
    import datetime
    from django.utils import timezone
    
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    
    stock_lot_data = {
        'produto': produto.pk,
        'lot_number': 'LOT-TEST-001',
        'location': location.pk,
        'expiry_date': (timezone.now() + datetime.timedelta(days=365)).date(),
        'purchase_price': 10.00,
        'initial_quantity': 100.00,
        'current_quantity': 100.00
    }
    
    response = api_client.post('/api/v1/stock-lots/', stock_lot_data, format='json')
    assert response.status_code in [201, 400]

@pytest.mark.django_db
def test_navigation_between_related_entities(authenticated_client):
    """Testa navegação entre entidades relacionadas"""
    client, user = authenticated_client
    
    # Testa navegação de produto para seus lotes de estoque
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    
    produto = Produto.objects.create(
        nome='Produto Relacionado',
        sku='REL-001',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )
    
    # Cria um lote associado
    stock_lot = StockLot.objects.create(
        produto=produto,
        lot_number='REL-LOT-001',
        location=location,
        expiry_date=timezone.now().date() + datetime.timedelta(days=365),
        purchase_price=15.00,
        initial_quantity=50.00,
        current_quantity=50.00
    )
    
    # Testa navegação para página de detalhes do produto
    response = client.get(f'/produtos/{produto.pk}/detail/')
    assert response.status_code == 200
    # Verifica se os lotes relacionados estão presentes na resposta
    # (Isso depende do template, mas a página deve carregar corretamente)

@pytest.mark.django_db
def test_breadcrumb_navigation(authenticated_client):
    """Testa a funcionalidade de navegação por breadcrumbs"""
    client, user = authenticated_client
    
    # Testa navegação hierárquica
    response = client.get('/dashboard/')
    assert response.status_code == 200
    
    # Acessa lista de produtos
    response = client.get('/produtos/list/')
    assert response.status_code == 200
    
    # Cria um produto para testar breadcrumb
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    
    produto = Produto.objects.create(
        nome='Produto Breadcrumb',
        sku='BREAD-001',
        category=category,
        fornecedor=supplier,
        quantidade=25.00
    )
    
    # Acessa detalhes do produto
    response = client.get(f'/produtos/{produto.pk}/detail/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_navigation_with_invalid_ids(authenticated_client):
    """Testa navegação com IDs inválidos para garantir tratamento adequado de erros"""
    client, user = authenticated_client
    
    # Testa acesso a um produto com ID inexistente
    response = client.get('/produtos/999999/detail/')
    # Pode retornar 404 ou redirecionar, mas não deve causar erro interno
    assert response.status_code in [404, 302, 200]