# Configuração de Testes - Sistema de Controle de Estoque

## Visão Geral
Esta configuração define os parâmetros e configurações para execução dos testes automatizados e manuais do sistema de controle de estoque.

## Ambiente de Teste

### Configurações de Ambiente
```yaml
environment:
  name: "Sistema de Controle de Estoque - Testes"
  version: "1.0.0"
  python_version: "3.8+"
  django_version: "5.2.6"
  node_version: "16+"
  
  # Diretórios
  project_root: "/media/Arquivos/DjangoPython/toolkits/v2/stock_control_lab"
  test_directory: "/media/Arquivos/DjangoPython/toolkits/v2/stock_control_lab/e2e_tests"
  reports_directory: "/media/Arquivos/DjangoPython/toolkits/v2/stock_control_lab/test_reports"
  
  # Banco de dados de teste
  database:
    engine: "sqlite3"
    name: ":memory:"
    
  # Servidor de teste
  server:
    host: "localhost"
    port: 8000
    protocol: "http"
```

## Configurações do Pytest

### pytest.ini
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
testpaths = tests e2e_tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
markers =
    e2e: mark as end-to-end test
    ui: mark as user interface test
    api: mark as API test
    integration: mark as integration test
    unit: mark as unit test
    slow: mark test as slow
    fast: mark test as fast
addopts = 
    --tb=short
    --strict-markers
    --strict-config
    -ra
    --maxfail=1
```

### Configuração do Pytest para Testes E2E
```python
# conftest.py
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from inventory.models import Category, Supplier, Location, Produto, StockLot

User = get_user_model()

@pytest.fixture
def client():
    """Cliente de teste para requisições HTTP"""
    return Client()

@pytest.fixture
def authenticated_client():
    """Cliente autenticado para testes que requerem login"""
    client = Client()
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        role='USER'
    )
    client.login(username='testuser', password='testpass123')
    return client, user

@pytest.fixture
def test_data():
    """Dados de teste para uso nos testes"""
    # Criar dados de teste básicos
    category = Category.objects.create(name='Test Category')
    supplier = Supplier.objects.create(name='Test Supplier')
    location = Location.objects.create(name='Test Location')
    
    # Criar alguns produtos de teste
    produto1 = Produto.objects.create(
        nome='Produto Teste 1',
        sku='TEST-001',
        category=category,
        fornecedor=supplier,
        quantidade=100.00
    )
    
    produto2 = Produto.objects.create(
        nome='Produto Teste 2',
        sku='TEST-002',
        category=category,
        fornecedor=supplier,
        quantidade=50.00
    )
    
    # Criar lotes de estoque
    lot1 = StockLot.objects.create(
        produto=produto1,
        lot_number='LOT-TEST-001',
        location=location,
        expiry_date='2026-12-31',
        purchase_price=10.00,
        initial_quantity=100.00,
        current_quantity=100.00
    )
    
    lot2 = StockLot.objects.create(
        produto=produto2,
        lot_number='LOT-TEST-002',
        location=location,
        expiry_date='2026-06-30',
        purchase_price=15.00,
        initial_quantity=50.00,
        current_quantity=50.00
    )
    
    return {
        'category': category,
        'supplier': supplier,
        'location': location,
        'produtos': [produto1, produto2],
        'lotes': [lot1, lot2]
    }

@pytest.fixture
def playwright_browser():
    """Browser para testes Playwright"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def playwright_page(playwright_browser):
    """Página para testes Playwright"""
    page = playwright_browser.new_page()
    yield page
    page.close()
```

## Configurações do Playwright

### playwright.config.js
```javascript
// @ts-check
const config = {
  testDir: './e2e_tests',
  outputDir: './test_results/playwright',
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test_results/playwright/results.json' }]
  ],
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    headless: false,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    acceptDownloads: true,
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'webkit',
      use: { browserName: 'webkit' },
    },
  ],
};

module.exports = config;
```

## Estratégia de Testes

### 1. Testes Unitários
- **Objetivo**: Validar unidades individuais de código
- **Ferramentas**: Pytest, Django Test Client
- **Cobertura**: Models, Serializers, Services, Utils
- **Critério de sucesso**: 100% de cobertura de código crítico

### 2. Testes de Integração
- **Objetivo**: Validar interação entre componentes
- **Ferramentas**: Pytest, Django Test Client
- **Cobertura**: APIs, Views, Fluxos de negócio
- **Critério de sucesso**: Todos os fluxos principais funcionando

### 3. Testes de Interface (UI)
- **Objetivo**: Validar experiência do usuário e funcionalidades visuais
- **Ferramentas**: Playwright, Selenium
- **Cobertura**: Navegação, Formulários, Componentes UI
- **Critério de sucesso**: Interface respondendo corretamente a todas as interações

### 4. Testes End-to-End (E2E)
- **Objetivo**: Validar fluxos completos do sistema
- **Ferramentas**: Playwright, Custom Scripts
- **Cobertura**: Login → Navegação → Operações → Logout
- **Critério de sucesso**: Todos os cenários de usuário completos funcionando

## Cenários de Teste Prioritários

### 1. Autenticação e Autorização
```gherkin
# Feature: Autenticação
# Scenario: Usuário realiza login com credenciais válidas
Given que o usuário acessa a página de login
When o usuário insere credenciais válidas e clica em "Entrar"
Then o usuário é redirecionado para o dashboard
And o menu de navegação é exibido

# Scenario: Usuário tenta login com credenciais inválidas
Given que o usuário acessa a página de login
When o usuário insere credenciais inválidas e clica em "Entrar"
Then uma mensagem de erro é exibida
And o usuário permanece na página de login
```

### 2. Navegação
```gherkin
# Feature: Navegação
# Scenario: Usuário navega entre páginas do sistema
Given que o usuário está autenticado no sistema
When o usuário clica em diferentes itens do menu
Then as páginas correspondentes são carregadas corretamente
And o título da página reflete o conteúdo esperado

# Scenario: Usuário acessa funcionalidades através de botões
Given que o usuário está em uma página qualquer do sistema
When o usuário clica em botões de ação
Then as funcionalidades correspondentes são acionadas
And feedback visual é fornecido ao usuário
```

### 3. Gerenciamento de Produtos
```gherkin
# Feature: Gerenciamento de Produtos
# Scenario: Usuário adiciona um novo produto
Given que o usuário está na página de listagem de produtos
When o usuário clica em "Adicionar Produto" e preenche o formulário
Then o produto é salvo com sucesso
And aparece na lista de produtos

# Scenario: Usuário edita um produto existente
Given que o usuário está na página de listagem de produtos
When o usuário seleciona um produto e clica em "Editar"
Then o formulário de edição é exibido com os dados atuais
When o usuário altera os dados e salva
Then as alterações são persistidas com sucesso

# Scenario: Usuário remove um produto
Given que o usuário está na página de listagem de produtos
When o usuário seleciona um produto e clica em "Excluir"
Then uma confirmação é solicitada
When o usuário confirma a exclusão
Then o produto é removido da lista
```

### 4. Controle de Estoque
```gherkin
# Feature: Controle de Estoque
# Scenario: Usuário registra entrada de estoque
Given que o usuário está na página de movimentações
When o usuário seleciona um produto e registra uma entrada
Then a quantidade em estoque é atualizada corretamente
And o histórico de movimentações é registrado

# Scenario: Usuário registra saída de estoque
Given que o usuário está na página de movimentações
When o usuário seleciona um produto e registra uma saída
Then a quantidade em estoque é reduzida corretamente
And o histórico de movimentações é registrado

# Scenario: Sistema alerta sobre estoque baixo
Given que um produto tem quantidade abaixo do mínimo configurado
When o usuário acessa o dashboard
Then um alerta de estoque baixo é exibido
And o produto aparece na lista de itens críticos
```

## Relatórios de Teste

### Estrutura de Relatórios
```
test_reports/
├── junit/
│   ├── unit_tests.xml
│   ├── integration_tests.xml
│   └── e2e_tests.xml
├── html/
│   ├── index.html
│   ├── unit_tests.html
│   ├── integration_tests.html
│   └── e2e_tests.html
├── json/
│   ├── results.json
│   └── coverage.json
└── playwright/
    ├── index.html
    ├── trace.zip
    └── screenshots/
```

### Métricas de Teste
- **Cobertura de Código**: ≥ 95% para código crítico
- **Taxa de Sucesso**: ≥ 98% dos testes passando
- **Tempo de Execução**: ≤ 30 minutos para todos os testes
- **Número de Defeitos**: ≤ 2 defeitos críticos encontrados

## Integração Contínua

### Pipeline de CI/CD
```yaml
# .github/workflows/test.yml
name: Testes Automatizados

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      redis:
        image: redis
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
        
    - name: Instalar dependências
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install playwright
        playwright install
        
    - name: Executar migrações
      run: python manage.py migrate
      
    - name: Executar testes unitários
      run: pytest tests/ -v --cov=inventory --cov-report=xml --junitxml=test_reports/junit/unit_tests.xml
      
    - name: Executar testes de integração
      run: pytest inventory/tests/ -v --cov=inventory --cov-report=xml --junitxml=test_reports/junit/integration_tests.xml
      
    - name: Executar testes E2E
      run: pytest e2e_tests/ -v --cov=inventory --cov-report=xml --junitxml=test_reports/junit/e2e_tests.xml
      
    - name: Upload de artefatos
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: test_reports/
```

## Monitoramento e Logging

### Configuração de Logging para Testes
```python
# test_logging_config.py
import logging
import sys

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'test_logs/test_run.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'inventory': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
```

## Ambientes de Teste

### 1. Desenvolvimento Local
- **Propósito**: Desenvolvimento e testes rápidos
- **Configuração**: SQLite, Redis embutido
- **Execução**: Manual ou automática durante desenvolvimento

### 2. Staging (Homologação)
- **Propósito**: Testes completos antes de produção
- **Configuração**: PostgreSQL, Redis separado
- **Execução**: Automática em CI/CD pipeline

### 3. Produção
- **Propósito**: Verificação final antes de deploy
- **Configuração**: Mesma que staging
- **Execução**: Automática em CI/CD pipeline

## Ferramentas Adicionais

### 1. Coverage.py
- **Propósito**: Medir cobertura de código
- **Configuração**: `.coveragerc`
```ini
[run]
source = .
omit = 
    */venv/*
    */migrations/*
    */tests/*
    manage.py
    */settings/*
    */wsgi.py
    */asgi.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### 2. Black (Formatador de Código)
- **Propósito**: Manter estilo de código consistente
- **Configuração**: `pyproject.toml`
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  | migrations
  | venv
  | node_modules
)/
'''
```

### 3. Flake8 (Linting)
- **Propósito**: Verificar qualidade de código
- **Configuração**: `.flake8`
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    venv,
    migrations,
    node_modules
```

## Plano de Execução

### Fase 1: Configuração do Ambiente (1 dia)
- [ ] Configurar ambiente de testes local
- [ ] Instalar dependências necessárias
- [ ] Configurar bases de dados de teste
- [ ] Verificar conectividade com serviços externos

### Fase 2: Desenvolvimento de Testes Unitários (3 dias)
- [ ] Criar testes para models
- [ ] Criar testes para serializers
- [ ] Criar testes para services
- [ ] Criar testes para utils

### Fase 3: Desenvolvimento de Testes de Integração (2 dias)
- [ ] Criar testes para APIs
- [ ] Criar testes para views
- [ ] Criar testes para fluxos de negócio
- [ ] Criar testes para autenticação

### Fase 4: Desenvolvimento de Testes de Interface (3 dias)
- [ ] Criar testes para navegação
- [ ] Criar testes para formulários
- [ ] Criar testes para componentes UI
- [ ] Criar testes para responsividade

### Fase 5: Desenvolvimento de Testes E2E (2 dias)
- [ ] Criar testes para fluxos completos
- [ ] Criar testes para cenários de erro
- [ ] Criar testes para casos extremos
- [ ] Criar testes de performance

### Fase 6: Integração com CI/CD (1 dia)
- [ ] Configurar pipeline de testes automático
- [ ] Configurar geração de relatórios
- [ ] Configurar notificações de falhas
- [ ] Configurar cobertura de código

### Fase 7: Documentação e Relatórios (1 dia)
- [ ] Documentar estratégia de testes
- [ ] Criar relatórios de execução
- [ ] Documentar resultados obtidos
- [ ] Criar plano de melhorias contínuas

## Critérios de Aceitação

### Testes Unitários
- [ ] 100% dos models testados
- [ ] 100% dos serializers testados
- [ ] 95%+ dos services testados
- [ ] 90%+ dos utils testados

### Testes de Integração
- [ ] Todas as APIs testadas
- [ ] Todas as views testadas
- [ ] Todos os fluxos de negócio testados
- [ ] Autenticação e autorização testadas

### Testes de Interface
- [ ] Navegação completa testada
- [ ] Todos os formulários testados
- [ ] Componentes UI testados
- [ ] Responsividade verificada

### Testes E2E
- [ ] Fluxos principais testados
- [ ] Cenários de erro cobertos
- [ ] Casos extremos verificados
- [ ] Performance medida

## Manutenção dos Testes

### Atualização de Testes
- Quando modificar código, atualizar testes correspondentes
- Revisar testes periodicamente para manter relevância
- Remover testes obsoletos
- Adicionar novos testes para novas funcionalidades

### Monitoramento de Qualidade
- Verificar cobertura de código regularmente
- Monitorar taxa de sucesso dos testes
- Analisar tempo de execução dos testes
- Identificar e corrigir testes flaky

Esta configuração de testes fornece uma base sólida para garantir a qualidade do sistema de controle de estoque, cobrindo todos os aspectos desde a autenticação até a navegação e funcionalidades completas do sistema.