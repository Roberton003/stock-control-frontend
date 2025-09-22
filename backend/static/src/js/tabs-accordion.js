/*
 * Gerenciador de Abas e Accordions
 * Script para controlar a interação de abas e seções expansíveis
 */

class TabsManager {
  constructor() {
    this.tabs = new Map();
    this.accordions = new Map();
    this.init();
  }

  init() {
    // Inicializar abas existentes
    document.querySelectorAll('[data-tabs]').forEach(tabsElement => {
      this.initTabs(tabsElement);
    });
    
    // Inicializar accordions existentes
    document.querySelectorAll('[data-accordion]').forEach(accordionElement => {
      this.initAccordion(accordionElement);
    });
    
    // Observar mudanças no DOM para inicializar novos elementos
    this.observeDOM();
  }

  initTabs(tabsElement) {
    const tabsId = tabsElement.id || `tabs-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    tabsElement.setAttribute('id', tabsId);
    
    const tabList = tabsElement.querySelector('[role="tablist"]');
    const tabButtons = tabsElement.querySelectorAll('[role="tab"]');
    const tabPanels = tabsElement.querySelectorAll('[role="tabpanel"]');
    
    if (!tabList || tabButtons.length === 0 || tabPanels.length === 0) {
      console.warn(`Tabs element #${tabsId} is missing required elements`);
      return;
    }
    
    // Criar estrutura de dados para as abas
    const tabsData = {
      element: tabsElement,
      list: tabList,
      buttons: Array.from(tabButtons),
      panels: Array.from(tabPanels),
      activeIndex: 0
    };
    
    // Adicionar eventos aos botões
    tabsData.buttons.forEach((button, index) => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        this.activateTab(tabsId, index);
      });
      
      button.addEventListener('keydown', (e) => {
        this.handleTabKeyDown(e, tabsId, index);
      });
    });
    
    // Armazenar dados das abas
    this.tabs.set(tabsId, tabsData);
    
    // Ativar a primeira aba se nenhuma estiver ativa
    const activeButton = tabsElement.querySelector('[role="tab"][aria-selected="true"]');
    if (!activeButton) {
      this.activateTab(tabsId, 0);
    }
  }

  activateTab(tabsId, tabIndex) {
    const tabsData = this.tabs.get(tabsId);
    if (!tabsData || tabIndex < 0 || tabIndex >= tabsData.buttons.length) {
      return;
    }
    
    // Desativar aba atual
    const currentButton = tabsData.buttons[tabsData.activeIndex];
    const currentPanel = tabsData.panels[tabsData.activeIndex];
    
    if (currentButton) {
      currentButton.setAttribute('aria-selected', 'false');
      currentButton.setAttribute('tabindex', '-1');
      currentButton.classList.remove('tab-item--active');
    }
    
    if (currentPanel) {
      currentPanel.setAttribute('aria-hidden', 'true');
      currentPanel.classList.add('tab-panel--hidden');
    }
    
    // Ativar nova aba
    const newButton = tabsData.buttons[tabIndex];
    const newPanel = tabsData.panels[tabIndex];
    
    if (newButton) {
      newButton.setAttribute('aria-selected', 'true');
      newButton.setAttribute('tabindex', '0');
      newButton.classList.add('tab-item--active');
      newButton.focus();
    }
    
    if (newPanel) {
      newPanel.setAttribute('aria-hidden', 'false');
      newPanel.classList.remove('tab-panel--hidden');
    }
    
    // Atualizar índice ativo
    tabsData.activeIndex = tabIndex;
    
    // Disparar evento personalizado
    tabsElement.dispatchEvent(new CustomEvent('tabChanged', {
      detail: { activeIndex: tabIndex, activeTab: newButton, activePanel: newPanel }
    }));
  }

  handleTabKeyDown(event, tabsId, currentIndex) {
    const tabsData = this.tabs.get(tabsId);
    if (!tabsData) return;
    
    let newIndex = currentIndex;
    
    switch (event.key) {
      case 'ArrowLeft':
        event.preventDefault();
        newIndex = currentIndex > 0 ? currentIndex - 1 : tabsData.buttons.length - 1;
        this.activateTab(tabsId, newIndex);
        break;
      case 'ArrowRight':
        event.preventDefault();
        newIndex = currentIndex < tabsData.buttons.length - 1 ? currentIndex + 1 : 0;
        this.activateTab(tabsId, newIndex);
        break;
      case 'Home':
        event.preventDefault();
        this.activateTab(tabsId, 0);
        break;
      case 'End':
        event.preventDefault();
        this.activateTab(tabsId, tabsData.buttons.length - 1);
        break;
      default:
        return;
    }
  }

  initAccordion(accordionElement) {
    const accordionId = accordionElement.id || `accordion-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    accordionElement.setAttribute('id', accordionId);
    
    const items = accordionElement.querySelectorAll('[data-accordion-item]');
    
    items.forEach((item, index) => {
      const header = item.querySelector('[data-accordion-header]');
      const content = item.querySelector('[data-accordion-content]');
      const button = header ? header.querySelector('button') : null;
      
      if (!header || !content || !button) {
        console.warn(`Accordion item #${item.id || index} is missing required elements`);
        return;
      }
      
      // Configurar atributos ARIA
      const itemId = `accordion-item-${accordionId}-${index}`;
      item.setAttribute('id', itemId);
      
      header.setAttribute('id', `accordion-header-${itemId}`);
      content.setAttribute('id', `accordion-content-${itemId}`);
      
      button.setAttribute('aria-expanded', 'false');
      button.setAttribute('aria-controls', `accordion-content-${itemId}`);
      
      content.setAttribute('aria-labelledby', `accordion-header-${itemId}`);
      content.setAttribute('aria-hidden', 'true');
      content.classList.add('accordion-content--hidden');
      
      // Adicionar evento de clique
      button.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleAccordionItem(itemId);
      });
      
      // Adicionar evento de tecla
      button.addEventListener('keydown', (e) => {
        this.handleAccordionKeyDown(e, itemId);
      });
    });
    
    // Armazenar dados do accordion
    this.accordions.set(accordionId, {
      element: accordionElement,
      items: Array.from(items)
    });
  }

  toggleAccordionItem(itemId) {
    const item = document.getElementById(itemId);
    if (!item) return;
    
    const header = item.querySelector('[data-accordion-header]');
    const content = item.querySelector('[data-accordion-content]');
    const button = header ? header.querySelector('button') : null;
    
    if (!header || !content || !button) return;
    
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    
    if (isExpanded) {
      // Colapsar
      button.setAttribute('aria-expanded', 'false');
      content.setAttribute('aria-hidden', 'true');
      content.classList.add('accordion-content--hidden');
      
      // Rotacionar ícone
      const icon = button.querySelector('.accordion-icon');
      if (icon) {
        icon.classList.remove('accordion-icon--rotated');
      }
    } else {
      // Expandir
      button.setAttribute('aria-expanded', 'true');
      content.setAttribute('aria-hidden', 'false');
      content.classList.remove('accordion-content--hidden');
      
      // Rotacionar ícone
      const icon = button.querySelector('.accordion-icon');
      if (icon) {
        icon.classList.add('accordion-icon--rotated');
      }
    }
    
    // Disparar evento personalizado
    item.dispatchEvent(new CustomEvent('accordionToggled', {
      detail: { expanded: !isExpanded, content: content }
    }));
  }

  handleAccordionKeyDown(event, itemId) {
    switch (event.key) {
      case 'Enter':
      case ' ':
        event.preventDefault();
        this.toggleAccordionItem(itemId);
        break;
      default:
        return;
    }
  }

  observeDOM() {
    // Observar mudanças no DOM para inicializar novos elementos
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Verificar se novos elementos de abas foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-tabs')) {
              this.initTabs(node);
            }
            
            // Verificar se novos elementos de accordion foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-accordion')) {
              this.initAccordion(node);
            }
            
            // Verificar elementos filhos
            node.querySelectorAll && node.querySelectorAll('[data-tabs]').forEach(tabsElement => {
              this.initTabs(tabsElement);
            });
            
            node.querySelectorAll && node.querySelectorAll('[data-accordion]').forEach(accordionElement => {
              this.initAccordion(accordionElement);
            });
          }
        });
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  // Métodos públicos para uso externo
  getTabs(tabsId) {
    return this.tabs.get(tabsId);
  }

  getAccordion(accordionId) {
    return this.accordions.get(accordionId);
  }

  activateTabById(tabsId, tabIndex) {
    this.activateTab(tabsId, tabIndex);
  }

  toggleAccordionById(itemId) {
    this.toggleAccordionItem(itemId);
  }
}

// Inicializar gerenciador quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.tabsManager = new TabsManager();
});

// Expôr funções globalmente para uso em templates
window.initTabs = (selector) => {
  const tabsElement = document.querySelector(selector);
  if (tabsElement && window.tabsManager) {
    window.tabsManager.initTabs(tabsElement);
  }
};

window.initAccordion = (selector) => {
  const accordionElement = document.querySelector(selector);
  if (accordionElement && window.tabsManager) {
    window.tabsManager.initAccordion(accordionElement);
  }
};

window.activateTab = (tabsId, tabIndex) => {
  if (window.tabsManager) {
    window.tabsManager.activateTab(tabsId, tabIndex);
  }
};

window.toggleAccordion = (itemId) => {
  if (window.tabsManager) {
    window.tabsManager.toggleAccordionItem(itemId);
  }
};