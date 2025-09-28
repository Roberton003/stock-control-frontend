/*
 * Gerenciador de Navegação entre Entidades Relacionadas
 * Script para controlar a navegação e contexto em sistemas complexos
 */

class EntityNavigationManager {
  constructor() {
    this.entities = new Map();
    this.navigationHistory = [];
    this.currentEntity = null;
    this.sidebarState = 'expanded';
    this.init();
  }

  init() {
    // Inicializar navegação existente
    this.initSidebar();
    this.initBreadcrumbs();
    this.initEntityNav();
    this.initQuickNav();
    
    // Observar mudanças no DOM
    this.observeDOM();
    
    // Adicionar eventos globais
    this.addGlobalEvents();
  }

  initSidebar() {
    const sidebar = document.querySelector('.sidebar-nav');
    if (!sidebar) return;
    
    // Adicionar evento para toggle da sidebar
    const toggleButton = sidebar.querySelector('.sidebar-toggle');
    if (toggleButton) {
      toggleButton.addEventListener('click', () => {
        this.toggleSidebar();
      });
    }
    
    // Adicionar eventos para itens do menu
    const menuItems = sidebar.querySelectorAll('.sidebar-item');
    menuItems.forEach(item => {
      item.addEventListener('click', (e) => {
        this.handleSidebarItemClick(e, item);
      });
    });
    
    // Adicionar eventos para submenu
    const submenuItems = sidebar.querySelectorAll('.sidebar-subitem');
    submenuItems.forEach(item => {
      item.addEventListener('click', (e) => {
        this.handleSubmenuItemClick(e, item);
      });
    });
  }

  initBreadcrumbs() {
    const breadcrumbs = document.querySelectorAll('.breadcrumb-item');
    breadcrumbs.forEach(item => {
      if (item.classList.contains('breadcrumb-item--link')) {
        item.addEventListener('click', (e) => {
          this.handleBreadcrumbClick(e, item);
        });
      }
    });
  }

  initEntityNav() {
    const entityNav = document.querySelector('.entity-nav');
    if (!entityNav) return;
    
    // Adicionar eventos para links de navegação
    const navLinks = entityNav.querySelectorAll('.related-entity-link');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        this.handleEntityNavLinkClick(e, link);
      });
    });
  }

  initQuickNav() {
    const quickNavItems = document.querySelectorAll('.quick-nav-item');
    quickNavItems.forEach(item => {
      item.addEventListener('click', (e) => {
        this.handleQuickNavItem_click(e, item);
      });
    });
  }

  toggleSidebar() {
    const sidebar = document.querySelector('.sidebar-nav');
    if (!sidebar) return;
    
    if (this.sidebarState === 'expanded') {
      sidebar.classList.add('sidebar-nav--collapsed');
      sidebar.classList.remove('sidebar-nav--expanded');
      this.sidebarState = 'collapsed';
    } else {
      sidebar.classList.add('sidebar-nav--expanded');
      sidebar.classList.remove('sidebar-nav--collapsed');
      this.sidebarState = 'expanded';
    }
    
    // Disparar evento personalizado
    document.dispatchEvent(new CustomEvent('sidebarToggled', {
      detail: { state: this.sidebarState }
    }));
  }

  handleSidebarItemClick(event, item) {
    event.preventDefault();
    event.stopPropagation();
    
    const entityId = item.getAttribute('data-entity-id');
    const entityType = item.getAttribute('data-entity-type');
    const entityUrl = item.getAttribute('data-entity-url');
    
    // Atualizar estado ativo
    this.updateActiveSidebarItem(item);
    
    // Navegar para a entidade
    if (entityUrl) {
      this.navigateToEntity(entityUrl, entityId, entityType);
    }
    
    // Disparar evento personalizado
    item.dispatchEvent(new CustomEvent('sidebarItemClicked', {
      detail: { entityId, entityType, entityUrl }
    }));
  }

  handleSubmenuItemClick(event, item) {
    event.preventDefault();
    event.stopPropagation();
    
    const entityId = item.getAttribute('data-entity-id');
    const entityType = item.getAttribute('data-entity-type');
    const entityUrl = item.getAttribute('data-entity-url');
    
    // Atualizar estado ativo
    this.updateActiveSubmenuItem(item);
    
    // Navegar para a entidade
    if (entityUrl) {
      this.navigateToEntity(entityUrl, entityId, entityType);
    }
    
    // Disparar evento personalizado
    item.dispatchEvent(new CustomEvent('submenuItemClicked', {
      detail: { entityId, entityType, entityUrl }
    }));
  }

  handleBreadcrumbClick(event, item) {
    event.preventDefault();
    
    const breadcrumbUrl = item.getAttribute('data-breadcrumb-url');
    if (breadcrumbUrl) {
      window.location.href = breadcrumbUrl;
    }
    
    // Disparar evento personalizado
    item.dispatchEvent(new CustomEvent('breadcrumbClicked', {
      detail: { url: breadcrumbUrl }
    }));
  }

  handleEntityNavLinkClick(event, link) {
    event.preventDefault();
    
    const entityUrl = link.getAttribute('href');
    const entityId = link.getAttribute('data-entity-id');
    const entityType = link.getAttribute('data-entity-type');
    
    if (entityUrl) {
      this.navigateToEntity(entityUrl, entityId, entityType);
    }
    
    // Disparar evento personalizado
    link.dispatchEvent(new CustomEvent('entityNavLinkClicked', {
      detail: { entityId, entityType, url: entityUrl }
    }));
  }

  handleQuickNavItem_click(event, item) {
    event.preventDefault();
    
    const quickNavUrl = item.getAttribute('data-quick-nav-url');
    const quickNavAction = item.getAttribute('data-quick-nav-action');
    
    if (quickNavUrl) {
      window.location.href = quickNavUrl;
    } else if (quickNavAction) {
      // Executar ação personalizada
      this.executeQuickNavAction(quickNavAction, item);
    }
    
    // Disparar evento personalizado
    item.dispatchEvent(new CustomEvent('quickNavItemClicked', {
      detail: { url: quickNavUrl, action: quickNavAction }
    }));
  }

  updateActiveSidebarItem(activeItem) {
    // Remover classe ativa de todos os itens
    const allItems = document.querySelectorAll('.sidebar-item');
    allItems.forEach(item => {
      item.classList.remove('sidebar-item--active');
    });
    
    // Adicionar classe ativa ao item selecionado
    activeItem.classList.add('sidebar-item--active');
  }

  updateActiveSubmenuItem(activeItem) {
    // Remover classe ativa de todos os subitens
    const allSubitems = document.querySelectorAll('.sidebar-subitem');
    allSubitems.forEach(item => {
      item.classList.remove('sidebar-subitem--active');
    });
    
    // Adicionar classe ativa ao subitem selecionado
    activeItem.classList.add('sidebar-subitem--active');
  }

  navigateToEntity(url, entityId, entityType) {
    // Adicionar ao histórico de navegação
    this.addToNavigationHistory({
      url,
      entityId,
      entityType,
      timestamp: new Date()
    });
    
    // Atualizar entidade atual
    this.currentEntity = {
      id: entityId,
      type: entityType,
      url: url
    };
    
    // Navegar para a URL
    window.location.href = url;
  }

  addToNavigationHistory(navigationItem) {
    this.navigationHistory.push(navigationItem);
    
    // Limitar histórico a 50 itens
    if (this.navigationHistory.length > 50) {
      this.navigationHistory.shift();
    }
  }

  executeQuickNavAction(action, element) {
    switch (action) {
      case 'refresh':
        window.location.reload();
        break;
      case 'back':
        window.history.back();
        break;
      case 'forward':
        window.history.forward();
        break;
      case 'print':
        window.print();
        break;
      default:
        // Executar ação personalizada
        if (typeof window[action] === 'function') {
          window[action](element);
        }
        break;
    }
  }

  observeDOM() {
    // Observar mudanças no DOM para inicializar novos elementos
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Verificar se novos elementos de navegação foram adicionados
            if (node.classList && node.classList.contains('sidebar-nav')) {
              this.initSidebar();
            }
            
            if (node.classList && node.classList.contains('breadcrumb')) {
              this.initBreadcrumbs();
            }
            
            if (node.classList && node.classList.contains('entity-nav')) {
              this.initEntityNav();
            }
            
            if (node.classList && node.classList.contains('quick-nav')) {
              this.initQuickNav();
            }
            
            // Verificar elementos filhos
            const sidebar = node.querySelector && node.querySelector('.sidebar-nav');
            if (sidebar) {
              this.initSidebar();
            }
            
            const breadcrumbs = node.querySelectorAll && node.querySelectorAll('.breadcrumb-item');
            if (breadcrumbs.length > 0) {
              this.initBreadcrumbs();
            }
            
            const entityNav = node.querySelector && node.querySelector('.entity-nav');
            if (entityNav) {
              this.initEntityNav();
            }
            
            const quickNav = node.querySelector && node.querySelector('.quick-nav');
            if (quickNav) {
              this.initQuickNav();
            }
          }
        });
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  addGlobalEvents() {
    // Adicionar atalhos de teclado
    document.addEventListener('keydown', (e) => {
      // Ctrl + Shift + B para toggle da sidebar
      if (e.ctrlKey && e.shiftKey && e.key === 'B') {
        e.preventDefault();
        this.toggleSidebar();
      }
      
      // Alt + Left Arrow para voltar
      if (e.altKey && e.key === 'ArrowLeft') {
        e.preventDefault();
        window.history.back();
      }
      
      // Alt + Right Arrow para avançar
      if (e.altKey && e.key === 'ArrowRight') {
        e.preventDefault();
        window.history.forward();
      }
    });
  }

  // Métodos públicos para uso externo
  getCurrentEntity() {
    return this.currentEntity;
  }

  getNavigationHistory() {
    return [...this.navigationHistory];
  }

  getSidebarState() {
    return this.sidebarState;
  }

  setActiveEntity(entityId, entityType) {
    this.currentEntity = {
      id: entityId,
      type: entityType
    };
  }

  refreshNavigation() {
    this.initSidebar();
    this.initBreadcrumbs();
    this.initEntityNav();
    this.initQuickNav();
  }
}

// Inicializar gerenciador quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.entityNavigationManager = new EntityNavigationManager();
});

// Expôr funções globalmente para uso em templates
window.initEntityNavigation = () => {
  if (window.entityNavigationManager) {
    window.entityNavigationManager.refreshNavigation();
  }
};

window.toggleSidebar = () => {
  if (window.entityNavigationManager) {
    window.entityNavigationManager.toggleSidebar();
  }
};

window.navigateToEntity = (url, entityId, entityType) => {
  if (window.entityNavigationManager) {
    window.entityNavigationManager.navigateToEntity(url, entityId, entityType);
  }
};

window.setActiveEntity = (entityId, entityType) => {
  if (window.entityNavigationManager) {
    window.entityNavigationManager.setActiveEntity(entityId, entityType);
  }
};