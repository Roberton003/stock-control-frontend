"""
Testes end-to-end para o sistema de controle de estoque usando Playwright
"""
import pytest
from playwright.sync_api import sync_playwright
import time

# Fixture para configurar o browser
@pytest.fixture(scope="session")
def browser():
    """Inicia e fecha o browser para todos os testes"""
    with sync_playwright() as p:
        # Iniciar o browser em modo não-headless para visualizar os testes
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        browser.close()

# Fixture para criar uma nova página
@pytest.fixture
def page(browser):
    """Cria uma nova página para cada teste"""
    page = browser.new_page()
    yield page
    page.close()

class TestAuthSystem:
    """Testes para o sistema de autenticação"""
    
    def test_login_page_loads(self, page):
        """Testa se a página de login carrega corretamente"""
        page.goto("http://localhost:8000")
        assert page.title() == "Sistema de Controle de Estoque Lab"
        assert page.is_visible("text=Login")
        
    def test_successful_login(self, page):
        """Testa login bem-sucedido"""
        page.goto("http://localhost:8000")
        
        # Preencher formulário de login
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para o dashboard
        page.wait_for_url("**/dashboard/**")
        assert page.is_visible("text=Dashboard do Laboratório")
        
    def test_failed_login(self, page):
        """Testa login com credenciais inválidas"""
        page.goto("http://localhost:8000")
        
        # Preencher formulário de login com credenciais inválidas
        page.fill("#username", "invalid_user")
        page.fill("#password", "wrong_password")
        page.click("button[type='submit']")
        
        # Verificar se permanece na página de login e mostra erro
        page.wait_for_timeout(2000)  # Esperar resposta
        assert page.url == "http://localhost:8000/"
        assert page.is_visible("text=Credenciais inválidas")

class TestNavigationSystem:
    """Testes para o sistema de navegação"""
    
    @pytest.fixture(autouse=True)
    def login(self, page):
        """Fazer login antes de cada teste de navegação"""
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard/**")
        
    def test_dashboard_navigation(self, page):
        """Testa navegação para o dashboard"""
        # Já está no dashboard após login
        assert page.is_visible("text=Dashboard do Laboratório")
        assert page.is_visible("text=Bem-vindo")
        
    def test_products_list_navigation(self, page):
        """Testa navegação para a lista de produtos"""
        # Clicar no menu de produtos
        page.click("text=Produtos")
        page.click("text=Lista de Produtos")
        
        # Verificar se está na página correta
        page.wait_for_url("**/produtos/list/**")
        assert page.is_visible("text=Lista de Produtos")
        
    def test_stock_lots_navigation(self, page):
        """Testa navegação para lotes de estoque"""
        # Clicar no menu de lotes
        page.click("text=Lotes")
        page.click("text=Lista de Lotes")
        
        # Verificar se está na página correta
        page.wait_for_url("**/stock-lots/list/**")
        assert page.is_visible("text=Lista de Lotes")
        
    def test_movements_navigation(self, page):
        """Testa navegação para movimentações"""
        # Clicar no menu de movimentações
        page.click("text=Movimentações")
        page.click("text=Lista de Movimentações")
        
        # Verificar se está na página correta
        page.wait_for_url("**/movimentacoes/list/**")
        assert page.is_visible("text=Lista de Movimentações")
        
    def test_requisitions_navigation(self, page):
        """Testa navegação para requisições"""
        # Clicar no menu de requisições
        page.click("text=Requisições")
        page.click("text=Lista de Requisições")
        
        # Verificar se está na página correta
        page.wait_for_url("**/requisitions/list/**")
        assert page.is_visible("text=Lista de Requisições")

class TestProductManagement:
    """Testes para gerenciamento de produtos"""
    
    @pytest.fixture(autouse=True)
    def login(self, page):
        """Fazer login antes de cada teste de gerenciamento de produtos"""
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard/**")
        
    def test_add_new_product(self, page):
        """Testa adição de novo produto"""
        # Navegar para a página de produtos
        page.click("text=Produtos")
        page.click("text=Lista de Produtos")
        page.wait_for_url("**/produtos/list/**")
        
        # Clicar no botão de adicionar produto
        page.click("text=Adicionar Produto")
        page.wait_for_url("**/produtos/create/**")
        
        # Preencher formulário de novo produto
        page.fill("#id_nome", "Ácido Sulfúrico 98%")
        page.fill("#id_sku", "H2SO4-98")
        page.fill("#id_descricao", "Ácido sulfúrico concentrado para laboratório")
        page.fill("#id_quantidade", "1000")
        page.select_option("#id_categoria", "Reagentes Químicos")
        page.select_option("#id_fornecedor", "Química Industrial Ltda")
        
        # Submeter formulário
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para a lista de produtos
        page.wait_for_url("**/produtos/list/**")
        assert page.is_visible("text=Produto adicionado com sucesso")
        assert page.is_visible("text=Ácido Sulfúrico 98%")
        
    def test_edit_existing_product(self, page):
        """Testa edição de produto existente"""
        # Navegar para a página de produtos
        page.click("text=Produtos")
        page.click("text=Lista de Produtos")
        page.wait_for_url("**/produtos/list/**")
        
        # Procurar um produto existente para editar
        # (assumindo que já existem produtos no sistema)
        page.click(".edit-product-button:first-child")
        page.wait_for_url("**/produtos/*/edit/**")
        
        # Alterar algum campo
        page.fill("#id_quantidade", "1500")
        
        # Submeter formulário
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para a lista de produtos
        page.wait_for_url("**/produtos/list/**")
        assert page.is_visible("text=Produto atualizado com sucesso")
        
    def test_delete_product(self, page):
        """Testa exclusão de produto"""
        # Navegar para a página de produtos
        page.click("text=Produtos")
        page.click("text=Lista de Produtos")
        page.wait_for_url("**/produtos/list/**")
        
        # Procurar um produto para excluir
        # (assumindo que já existem produtos no sistema)
        page.click(".delete-product-button:first-child")
        
        # Confirmar exclusão no modal
        page.click("button:has-text('Confirmar')")
        
        # Verificar se o produto foi excluído
        page.wait_for_timeout(2000)  # Esperar processamento
        assert page.is_visible("text=Produto excluído com sucesso")

class TestStockLotManagement:
    """Testes para gerenciamento de lotes de estoque"""
    
    @pytest.fixture(autouse=True)
    def login(self, page):
        """Fazer login antes de cada teste de gerenciamento de lotes"""
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard/**")
        
    def test_add_new_stock_lot(self, page):
        """Testa adição de novo lote de estoque"""
        # Navegar para a página de lotes
        page.click("text=Lotes")
        page.click("text=Lista de Lotes")
        page.wait_for_url("**/stock-lots/list/**")
        
        # Clicar no botão de adicionar lote
        page.click("text=Adicionar Lote")
        page.wait_for_url("**/stock-lots/create/**")
        
        # Preencher formulário de novo lote
        page.select_option("#id_produto", "1")  # Primeiro produto da lista
        page.fill("#id_numero_lote", "LOT-TEST-001")
        page.fill("#id_localizacao", "Armário A-1")
        page.fill("#id_data_validade", "2026-12-31")
        page.fill("#id_preco_compra", "50.00")
        page.fill("#id_quantidade_inicial", "1000")
        page.fill("#id_quantidade_atual", "1000")
        
        # Submeter formulário
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para a lista de lotes
        page.wait_for_url("**/stock-lots/list/**")
        assert page.is_visible("text=Lote adicionado com sucesso")
        assert page.is_visible("text=LOT-TEST-001")
        
    def test_view_stock_lot_details(self, page):
        """Testa visualização de detalhes de lote"""
        # Navegar para a página de lotes
        page.click("text=Lotes")
        page.click("text=Lista de Lotes")
        page.wait_for_url("**/stock-lots/list/**")
        
        # Clicar no primeiro lote da lista para ver detalhes
        page.click(".view-lot-button:first-child")
        page.wait_for_url("**/stock-lots/*/detail/**")
        
        # Verificar se os detalhes são exibidos
        assert page.is_visible("text=Detalhes do Lote")
        assert page.is_visible("text=Número do Lote")

class TestStockMovements:
    """Testes para movimentações de estoque"""
    
    @pytest.fixture(autouse=True)
    def login(self, page):
        """Fazer login antes de cada teste de movimentações"""
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard/**")
        
    def test_add_stock_entry(self, page):
        """Testa adição de entrada de estoque"""
        # Navegar para a página de movimentações
        page.click("text=Movimentações")
        page.click("text=Adicionar Movimentação")
        page.wait_for_url("**/movimentacoes/add/**")
        
        # Preencher formulário de entrada
        page.select_option("#id_tipo", "ENTRADA")
        page.select_option("#id_produto", "1")  # Primeiro produto da lista
        page.fill("#id_quantidade", "500")
        page.fill("#id_motivo", "Compra de reagentes")
        
        # Submeter formulário
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para a lista de movimentações
        page.wait_for_url("**/movimentacoes/list/**")
        assert page.is_visible("text=Movimentação registrada com sucesso")
        assert page.is_visible("text=Compra de reagentes")
        
    def test_add_stock_withdrawal(self, page):
        """Testa adição de saída de estoque"""
        # Navegar para a página de movimentações
        page.click("text=Movimentações")
        page.click("text=Adicionar Movimentação")
        page.wait_for_url("**/movimentacoes/add/**")
        
        # Preencher formulário de saída
        page.select_option("#id_tipo", "SAÍDA")
        page.select_option("#id_produto", "1")  # Primeiro produto da lista
        page.fill("#id_quantidade", "250")
        page.fill("#id_motivo", "Utilização em experimento")
        
        # Submeter formulário
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para a lista de movimentações
        page.wait_for_url("**/movimentacoes/list/**")
        assert page.is_visible("text=Movimentação registrada com sucesso")
        assert page.is_visible("text=Utilização em experimento")

class TestRequisitions:
    """Testes para requisições de produtos"""
    
    @pytest.fixture(autouse=True)
    def login(self, page):
        """Fazer login antes de cada teste de requisições"""
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard/**")
        
    def test_create_new_requisition(self, page):
        """Testa criação de nova requisição"""
        # Navegar para a página de requisições
        page.click("text=Requisições")
        page.click("text=Lista de Requisições")
        page.wait_for_url("**/requisitions/list/**")
        
        # Clicar no botão de criar requisição
        page.click("text=Criar Requisição")
        page.wait_for_url("**/requisitions/create/**")
        
        # Preencher formulário de requisição
        page.select_option("#id_produto", "1")  # Primeiro produto da lista
        page.fill("#id_quantidade", "100")
        page.fill("#id_finalidade", "Experimento de titulação")
        page.fill("#id_solicitante", "Dr. João Silva")
        
        # Submeter formulário
        page.click("button[type='submit']")
        
        # Verificar se foi redirecionado para a lista de requisições
        page.wait_for_url("**/requisitions/list/**")
        assert page.is_visible("text=Requisição criada com sucesso")
        assert page.is_visible("text=Dr. João Silva")
        
    def test_approve_requisition(self, page):
        """Testa aprovação de requisição"""
        # Navegar para a página de requisições
        page.click("text=Requisições")
        page.click("text=Lista de Requisições")
        page.wait_for_url("**/requisitions/list/**")
        
        # Procurar uma requisição pendente para aprovar
        # (assumindo que já existem requisições no sistema)
        page.click(".approve-requisition-button:first-child")
        
        # Confirmar aprovação no modal
        page.click("button:has-text('Aprovar')")
        
        # Verificar se a requisição foi aprovada
        page.wait_for_timeout(2000)  # Esperar processamento
        assert page.is_visible("text=Requisição aprovada com sucesso")

class TestUIComponents:
    """Testes para componentes da interface do usuário"""
    
    @pytest.fixture(autouse=True)
    def login(self, page):
        """Fazer login antes de cada teste de componentes UI"""
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard/**")
        
    def test_theme_toggle(self, page):
        """Testa alternância de tema (claro/escuro)"""
        # Verificar se o botão de tema existe
        assert page.is_visible(".theme-toggle-button")
        
        # Alternar para tema escuro
        page.click(".theme-toggle-button")
        page.wait_for_timeout(500)  # Esperar transição
        
        # Verificar se o tema escuro foi aplicado
        assert page.evaluate("() => document.documentElement.classList.contains('dark')")
        
        # Alternar de volta para tema claro
        page.click(".theme-toggle-button")
        page.wait_for_timeout(500)  # Esperar transição
        
        # Verificar se o tema claro foi aplicado
        assert not page.evaluate("() => document.documentElement.classList.contains('dark')")
        
    def test_responsive_navigation(self, page):
        """Testa navegação responsiva em dispositivos móveis"""
        # Definir tamanho de viewport para dispositivo móvel
        page.set_viewport_size({"width": 375, "height": 667})
        
        # Verificar se o botão de menu hamburguer aparece
        assert page.is_visible(".mobile-menu-toggle")
        
        # Clicar no botão de menu
        page.click(".mobile-menu-toggle")
        
        # Verificar se o menu mobile é exibido
        assert page.is_visible(".mobile-menu")
        
        # Clicar em um item do menu
        page.click("text=Dashboard")
        
        # Verificar se o menu se fecha e navega corretamente
        assert page.is_visible("text=Dashboard do Laboratório")
        
    def test_notifications_system(self, page):
        """Testa sistema de notificações"""
        # Verificar se o ícone de notificações existe
        assert page.is_visible(".notification-bell")
        
        # Clicar no ícone de notificações
        page.click(".notification-bell")
        
        # Verificar se o dropdown de notificações é exibido
        assert page.is_visible(".notification-dropdown")
        
        # Verificar se há notificações (ou mensagem de nenhuma notificação)
        assert page.is_visible("text=Notificações") or page.is_visible("text=Nenhuma notificação")

# Executar testes se este arquivo for executado diretamente
if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])