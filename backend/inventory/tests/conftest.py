import pytest
from rest_framework.test import APIClient
from inventory.models import User

@pytest.fixture
def api_client():
    """Um cliente de API não autenticado."""
    return APIClient()

@pytest.fixture
def authenticated_client():
    """Um cliente de API autenticado com um usuário de teste."""
    client = APIClient()
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        role='Analista'
    )
    client.force_authenticate(user=user)
    return client, user