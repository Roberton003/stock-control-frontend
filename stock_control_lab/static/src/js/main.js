// main.js - Arquivo principal JavaScript do sistema

// Importar funções modernas
import './modern_functions.js';

// Verificar se o DOM está pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Função de inicialização principal
function initializeApp() {
    console.log('Sistema LabStock Control inicializado');
    
    // Inicializar componentes modernos
    if (typeof initializeModernComponents === 'function') {
        initializeModernComponents();
    }
    
    // Inicializar funcionalidades específicas da página
    initializePageSpecificFeatures();
    
    // Configurar eventos globais
    setupGlobalEvents();
}

// Função para inicializar funcionalidades específicas da página
function initializePageSpecificFeatures() {
    const currentPage = document.body.dataset.page;
    
    switch (currentPage) {
        case 'dashboard':
            initializeDashboardFeatures();
            break;
        case 'products':
            initializeProductsFeatures();
            break;
        case 'lots':
            initializeLotsFeatures();
            break;
        case 'movements':
            initializeMovementsFeatures();
            break;
        default:
            console.log('Página sem inicializações específicas');
    }
}

// Funções de inicialização por página
function initializeDashboardFeatures() {
    console.log('Inicializando funcionalidades do dashboard');
    
    // Inicializar gráficos do dashboard
    initializeDashboardCharts();
    
    // Configurar atualizações em tempo real
    setupDashboardRealTimeUpdates();
}

function initializeProductsFeatures() {
    console.log('Inicializando funcionalidades de produtos');
    
    // Configurar filtros de produtos
    setupProductFilters();
    
    // Configurar pesquisa em tempo real
    setupProductSearch();
}

function initializeLotsFeatures() {
    console.log('Inicializando funcionalidades de lotes');
    
    // Configurar filtros de lotes
    setupLotFilters();
    
    // Configurar destaque de lotes próximos do vencimento
    highlightExpiringLots();
}

function initializeMovementsFeatures() {
    console.log('Inicializando funcionalidades de movimentações');
    
    // Configurar validações de movimentações
    setupMovementValidations();
}

// Função para inicializar gráficos do dashboard
function initializeDashboardCharts() {
    // Esta função será chamada nas páginas que precisam de gráficos
    // Os gráficos específicos são inicializados nos templates
}

// Função para configurar atualizações em tempo real do dashboard
function setupDashboardRealTimeUpdates() {
    // Implementar atualizações periódicas dos dados do dashboard
    setInterval(updateDashboardData, 30000); // Atualizar a cada 30 segundos
}

// Função para atualizar dados do dashboard
function updateDashboardData() {
    // Esta função seria implementada para buscar novos dados via AJAX
    console.log('Atualizando dados do dashboard...');
}

// Função para configurar filtros de produtos
function setupProductFilters() {
    const categoryFilter = document.getElementById('category-filter');
    const searchInput = document.getElementById('product-search');
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterProducts);
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterProducts, 300));
    }
}

// Função para configurar pesquisa em tempo real de produtos
function setupProductSearch() {
    const searchInput = document.getElementById('product-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(performSearch, 300));
    }
}

// Função para configurar filtros de lotes
function setupLotFilters() {
    const expiryFilter = document.getElementById('expiry-filter');
    if (expiryFilter) {
        expiryFilter.addEventListener('change', filterLots);
    }
}

// Função para destacar lotes próximos do vencimento
function highlightExpiringLots() {
    const expiringLots = document.querySelectorAll('.lot-expiring');
    expiringLots.forEach(lot => {
        lot.classList.add('bg-yellow-100', 'border-l-4', 'border-yellow-500');
    });
}

// Função para configurar validações de movimentações
function setupMovementValidations() {
    const movementForm = document.getElementById('movement-form');
    if (movementForm) {
        movementForm.addEventListener('submit', validateMovementForm);
    }
}

// Funções utilitárias
function filterProducts() {
    console.log('Filtrando produtos...');
    // Implementação do filtro de produtos
}

function performSearch() {
    console.log('Realizando pesquisa...');
    // Implementação da pesquisa
}

function filterLots() {
    console.log('Filtrando lotes...');
    // Implementação do filtro de lotes
}

function validateMovementForm(event) {
    console.log('Validando formulário de movimentação...');
    // Implementação da validação
}

// Função debounce para limitar chamadas de função
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Função para configurar eventos globais
function setupGlobalEvents() {
    // Configurar evento de clique para fechar dropdowns
    document.addEventListener('click', function(event) {
        const dropdowns = document.querySelectorAll('.dropdown-menu:not(.hidden)');
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(event.target) && !event.target.hasAttribute('data-dropdown-toggle')) {
                dropdown.classList.add('hidden');
            }
        });
    });
    
    // Configurar evento de tecla ESC para fechar modals
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.flex');
            openModals.forEach(modal => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                document.body.style.overflow = '';
            });
        }
    });
}

// Exportar funções para uso global
window.initializeApp = initializeApp;