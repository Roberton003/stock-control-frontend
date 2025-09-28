// modern_functions.js - Funções JavaScript modernas para o sistema

// Função para inicializar componentes
function initializeModernComponents() {
    // Inicializar tooltips
    initializeTooltips();
    
    // Inicializar modals
    initializeModals();
    
    // Inicializar dropdowns
    initializeDropdowns();
    
    // Inicializar gráficos
    initializeCharts();
    
    // Inicializar animações
    initializeAnimations();
}

// Função para inicializar tooltips
function initializeTooltips() {
    // Implementação de tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip';
            tooltipEl.textContent = tooltipText;
            document.body.appendChild(tooltipEl);
            
            const rect = this.getBoundingClientRect();
            tooltipEl.style.position = 'absolute';
            tooltipEl.style.left = rect.left + (rect.width / 2) - (tooltipEl.offsetWidth / 2) + 'px';
            tooltipEl.style.top = rect.top - tooltipEl.offsetHeight - 10 + 'px';
            tooltipEl.style.zIndex = '1000';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltipEl = document.querySelector('.tooltip');
            if (tooltipEl) {
                tooltipEl.remove();
            }
        });
    });
}

// Função para inicializar modals
function initializeModals() {
    // Abrir modals
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal-trigger');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('hidden');
                modal.classList.add('flex');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    // Fechar modals
    const closeModalButtons = document.querySelectorAll('[data-close-modal]');
    closeModalButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Fechar modal ao clicar no backdrop
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.add('hidden');
                this.classList.remove('flex');
                document.body.style.overflow = '';
            }
        });
    });
}

// Função para inicializar dropdowns
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('[data-dropdown-toggle]');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (trigger && menu) {
            trigger.addEventListener('click', function(e) {
                e.stopPropagation();
                menu.classList.toggle('hidden');
            });
            
            // Fechar dropdown ao clicar fora
            document.addEventListener('click', function() {
                menu.classList.add('hidden');
            });
        }
    });
}

// Função para inicializar gráficos
function initializeCharts() {
    // Esta função será chamada após carregar Chart.js
    // Os gráficos específicos serão inicializados nas páginas correspondentes
}

// Função para inicializar animações
function initializeAnimations() {
    // Animações de fade-in para elementos
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    animateElements.forEach(element => {
        observer.observe(element);
    });
}

// Função para alternar tema claro/escuro
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.classList.remove(currentTheme);
    html.classList.add(newTheme);
    
    // Salvar preferência do usuário
    localStorage.setItem('theme', newTheme);
    
    // Atualizar ícone do botão
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = newTheme === 'dark' ? 
            '<i class="fas fa-sun"></i>' : 
            '<i class="fas fa-moon"></i>';
    }
}

// Função para carregar tema salvo
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const html = document.documentElement;
    
    html.classList.remove('light', 'dark');
    html.classList.add(savedTheme);
    
    // Atualizar ícone do botão
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = savedTheme === 'dark' ? 
            '<i class="fas fa-sun"></i>' : 
            '<i class="fas fa-moon"></i>';
    }
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notification-container');
    if (!notificationContainer) return;
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} shadow-lg rounded-lg p-4 mb-4 flex items-start`;
    notification.innerHTML = `
        <div class="mr-3">
            ${type === 'success' ? '<i class="fas fa-check-circle text-green-500"></i>' : ''}
            ${type === 'error' ? '<i class="fas fa-exclamation-circle text-red-500"></i>' : ''}
            ${type === 'warning' ? '<i class="fas fa-exclamation-triangle text-yellow-500"></i>' : ''}
            ${type === 'info' ? '<i class="fas fa-info-circle text-blue-500"></i>' : ''}
        </div>
        <div class="flex-1">
            <p class="text-sm font-medium">${message}</p>
        </div>
        <button class="ml-4 text-gray-400 hover:text-gray-600" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Remover notificação após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Função para confirmar ações
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Função para formatar moeda
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para formatar data
function formatDate(dateString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

// Inicializar quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    initializeModernComponents();
    loadSavedTheme();
});

// Exportar funções para uso global
window.toggleTheme = toggleTheme;
window.showNotification = showNotification;
window.confirmAction = confirmAction;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;