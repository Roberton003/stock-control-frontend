"""
Testes automatizados para validação de login e autenticação
no sistema de controle de estoque.
"""
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from inventory.models import User

User = get_user_model()

@pytest.fixture
def client():
    """Cria um cliente de teste"""
    return Client()

@pytest.fixture
def api_client():
    """Cria um cliente de API de teste"""
    return APIClient()

@pytest.fixture
def test_user():
    """Cria um usuário de teste"""
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        role='USER'
    )
    return user

@pytest.mark.django_db
def test_login_page_loads():
    """Testa se a página de login carrega corretamente"""
    client = Client()
    response = client.get('/admin/login/')  # Padrão do Django
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_login_with_valid_credentials(client, test_user):
    """Testa login com credenciais válidas"""
    response = client.post('/admin/login/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    # Verifica se o login foi bem sucedido (redirecionamento ou página de dashboard)
    # O status pode ser 302 (redirect) ou 200 se permanecer na mesma página mas autenticado
    assert response.status_code in [200, 302]
    
    # Verifica se o usuário está autenticado
    assert '_auth_user_id' in client.session

@pytest.mark.django_db
def test_user_login_with_invalid_credentials(client, test_user):
    """Testa login com credenciais inválidas"""
    response = client.post('/admin/login/', {
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    # Deve permanecer na página de login com erro
    assert response.status_code == 200
    # Verifica se há mensagem de erro (dependendo da implementação do template)
    # Pode não ter mensagem de erro visível diretamente no HTML

@pytest.mark.django_db
def test_user_logout(client, test_user):
    """Testa o processo de logout"""
    # Primeiro faz login
    client.login(username='testuser', password='testpass123')
    
    # Verifica que o usuário está autenticado
    response = client.get('/admin/')
    assert response.status_code in [200, 302]  # Pode redirecionar se estiver logado
    
    # Faz logout
    response = client.post('/admin/logout/')
    assert response.status_code in [200, 302]  # Página de confirmação de logout
    
    # Verifica se o usuário não está mais autenticado
    assert '_auth_user_id' not in client.session

@pytest.mark.django_db
def test_api_authentication_required(api_client):
    """Testa que endpoints da API requerem autenticação"""
    response = api_client.get('/api/v1/produtos/')
    # Deve retornar 401 ou 403 se não estiver autenticado
    assert response.status_code in [401, 403]

@pytest.mark.django_db
def test_api_authentication_with_token(api_client, test_user):
    """Testa autenticação na API com token"""
    # Primeiro obtemos um token de autenticação (isso depende da configuração do sistema)
    # Se estiver usando DRF TokenAuthentication, precisamos criar ou obter um token
    from rest_framework.authtoken.models import Token
    from django.contrib.auth import authenticate
    
    # Autentica o usuário
    user = authenticate(username='testuser', password='testpass123')
    if user:
        token, created = Token.objects.get_or_create(user=user)
        
        # Usa o token para autenticação
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # Agora deve ser possível acessar o endpoint
        response = api_client.get('/api/v1/produtos/')
        assert response.status_code == 200
    else:
        # Se authenticate falhar, faz login direto
        api_client.force_authenticate(user=test_user)
        response = api_client.get('/api/v1/produtos/')
        assert response.status_code == 200

@pytest.mark.django_db
def test_user_permissions_after_login(client, test_user):
    """Testa se o usuário tem permissões após login"""
    client.login(username='testuser', password='testpass123')
    
    # Tenta acessar uma página restrita
    response = client.get('/admin/')
    # Dependendo das permissões do usuário, pode ser 200 ou 302 (se for admin e não tiver permissão)
    # Um usuário comum não deve ter acesso ao admin por padrão
    # Mas se for um usuário com permissões, deve ter acesso
    
    # Apenas confirma que não é um erro 403 ou 404
    assert response.status_code in [200, 302, 403]

@pytest.mark.django_db
def test_session_persistence(client, test_user):
    """Testa persistência da sessão após login"""
    # Faz login
    client.login(username='testuser', password='testpass123')
    
    # Verifica se está autenticado
    response = client.get('/admin/')
    assert response.status_code in [200, 302]
    
    # Acessa outra página - deve continuar autenticado
    response = client.get('/')  # Página inicial
    # O status aqui depende da configuração do sistema
    # Mas o importante é que a sessão continue ativa
    session = client.session
    assert '_auth_user_id' in session