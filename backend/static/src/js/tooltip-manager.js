/*
 * Gerenciador de Tooltips e Ajuda Contextual
 * Script para controlar a exibição e interação de tooltips e ajuda
 */

class TooltipManager {
  constructor() {
    this.tooltips = new Map();
    this.helpElements = new Map();
    this.currentTooltip = null;
    this.currentHelp = null;
    this.init();
  }

  init() {
    // Inicializar tooltips existentes
    document.querySelectorAll('[data-tooltip]').forEach(tooltipElement => {
      this.initTooltip(tooltipElement);
    });
    
    // Inicializar elementos de ajuda existentes
    document.querySelectorAll('[data-help]').forEach(helpElement => {
      this.initHelp(helpElement);
    });
    
    // Observar mudanças no DOM para inicializar novos elementos
    this.observeDOM();
    
    // Adicionar eventos globais para fechamento
    document.addEventListener('click', (e) => {
      this.closeAll(e);
    });
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeAll();
      }
    });
  }

  initTooltip(tooltipElement) {
    const tooltipId = tooltipElement.id || `tooltip-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    tooltipElement.setAttribute('id', tooltipId);
    
    // Extrair configurações do atributo data
    const config = {
      content: tooltipElement.getAttribute('data-tooltip') || '',
      position: tooltipElement.getAttribute('data-tooltip-position') || 'top',
      trigger: tooltipElement.getAttribute('data-tooltip-trigger') || 'hover',
      delay: parseInt(tooltipElement.getAttribute('data-tooltip-delay')) || 0,
      theme: tooltipElement.getAttribute('data-tooltip-theme') || 'default',
      maxWidth: tooltipElement.getAttribute('data-tooltip-max-width') || 'none'
    };
    
    // Criar estrutura de dados para o tooltip
    const tooltipData = {
      element: tooltipElement,
      config: config,
      tooltipElement: null,
      isVisible: false,
      hideTimeout: null,
      showTimeout: null
    };
    
    // Adicionar eventos conforme o trigger
    if (config.trigger === 'hover') {
      tooltipElement.addEventListener('mouseenter', () => {
        this.showTooltipWithDelay(tooltipId);
      });
      
      tooltipElement.addEventListener('mouseleave', () => {
        this.hideTooltipWithDelay(tooltipId);
      });
      
      // Para dispositivos touch, mostrar ao tocar e esconder ao tocar fora
      tooltipElement.addEventListener('touchstart', (e) => {
        e.preventDefault();
        if (tooltipData.isVisible) {
          this.hideTooltip(tooltipId);
        } else {
          this.showTooltip(tooltipId);
        }
      });
    } else if (config.trigger === 'click') {
      tooltipElement.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (tooltipData.isVisible) {
          this.hideTooltip(tooltipId);
        } else {
          this.showTooltip(tooltipId);
        }
      });
    } else if (config.trigger === 'focus') {
      tooltipElement.addEventListener('focus', () => {
        this.showTooltip(tooltipId);
      });
      
      tooltipElement.addEventListener('blur', () => {
        this.hideTooltip(tooltipId);
      });
    }
    
    // Adicionar classe para estilo
    tooltipElement.classList.add('tooltip-trigger');
    
    // Armazenar dados do tooltip
    this.tooltips.set(tooltipId, tooltipData);
  }

  initHelp(helpElement) {
    const helpId = helpElement.id || `help-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    helpElement.setAttribute('id', helpId);
    
    // Extrair configurações do atributo data
    const config = {
      title: helpElement.getAttribute('data-help-title') || '',
      content: helpElement.getAttribute('data-help') || '',
      position: helpElement.getAttribute('data-help-position') || 'top',
      trigger: helpElement.getAttribute('data-help-trigger') || 'click',
      imageUrl: helpElement.getAttribute('data-help-image') || '',
      imageCaption: helpElement.getAttribute('data-help-image-caption') || ''
    };
    
    // Criar estrutura de dados para a ajuda
    const helpData = {
      element: helpElement,
      config: config,
      helpElement: null,
      isVisible: false
    };
    
    // Adicionar eventos conforme o trigger
    if (config.trigger === 'hover') {
      helpElement.addEventListener('mouseenter', () => {
        this.showHelp(helpId);
      });
      
      helpElement.addEventListener('mouseleave', () => {
        this.hideHelp(helpId);
      });
    } else if (config.trigger === 'click') {
      helpElement.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (helpData.isVisible) {
          this.hideHelp(helpId);
        } else {
          this.showHelp(helpId);
        }
      });
    }
    
    // Adicionar classe para estilo
    helpElement.classList.add('help-button');
    
    // Armazenar dados da ajuda
    this.helpElements.set(helpId, helpData);
  }

  showTooltipWithDelay(tooltipId) {
    const tooltipData = this.tooltips.get(tooltipId);
    if (!tooltipData) return;
    
    // Cancelar timeout de ocultar
    if (tooltipData.hideTimeout) {
      clearTimeout(tooltipData.hideTimeout);
      tooltipData.hideTimeout = null;
    }
    
    // Mostrar com delay
    if (tooltipData.config.delay > 0) {
      tooltipData.showTimeout = setTimeout(() => {
        this.showTooltip(tooltipId);
      }, tooltipData.config.delay);
    } else {
      this.showTooltip(tooltipId);
    }
  }

  hideTooltipWithDelay(tooltipId) {
    const tooltipData = this.tooltips.get(tooltipId);
    if (!tooltipData) return;
    
    // Cancelar timeout de mostrar
    if (tooltipData.showTimeout) {
      clearTimeout(tooltipData.showTimeout);
      tooltipData.showTimeout = null;
    }
    
    // Ocultar com delay pequeno
    tooltipData.hideTimeout = setTimeout(() => {
      this.hideTooltip(tooltipId);
    }, 100);
  }

  showTooltip(tooltipId) {
    const tooltipData = this.tooltips.get(tooltipId);
    if (!tooltipData || !tooltipData.config.content) return;
    
    // Fechar tooltip atual se houver
    if (this.currentTooltip && this.currentTooltip !== tooltipId) {
      this.hideTooltip(this.currentTooltip);
    }
    
    // Criar elemento do tooltip se não existir
    if (!tooltipData.tooltipElement) {
      tooltipData.tooltipElement = this.createTooltipElement(tooltipData);
      document.body.appendChild(tooltipData.tooltipElement);
    }
    
    // Posicionar tooltip
    this.positionTooltip(tooltipData);
    
    // Mostrar tooltip
    tooltipData.tooltipElement.classList.add('tooltip-content--visible');
    tooltipData.isVisible = true;
    this.currentTooltip = tooltipId;
    
    // Disparar evento personalizado
    tooltipData.element.dispatchEvent(new CustomEvent('tooltipShow', {
      detail: { tooltip: tooltipData.tooltipElement }
    }));
  }

  hideTooltip(tooltipId) {
    const tooltipData = this.tooltips.get(tooltipId);
    if (!tooltipData || !tooltipData.isVisible) return;
    
    // Ocultar tooltip
    if (tooltipData.tooltipElement) {
      tooltipData.tooltipElement.classList.remove('tooltip-content--visible');
    }
    
    tooltipData.isVisible = false;
    this.currentTooltip = null;
    
    // Disparar evento personalizado
    tooltipData.element.dispatchEvent(new CustomEvent('tooltipHide', {
      detail: { tooltip: tooltipData.tooltipElement }
    }));
  }

  createTooltipElement(tooltipData) {
    const tooltip = document.createElement('div');
    tooltip.className = `tooltip-content tooltip-content--${tooltipData.config.position} tooltip-content--${tooltipData.config.theme}`;
    
    // Aplicar largura máxima se especificada
    if (tooltipData.config.maxWidth !== 'none') {
      tooltip.style.maxWidth = tooltipData.config.maxWidth;
    }
    
    // Adicionar conteúdo
    tooltip.innerHTML = `
      <div class="tooltip-arrow tooltip-arrow--${tooltipData.config.position}"></div>
      <div class="tooltip-text">${tooltipData.config.content}</div>
    `;
    
    return tooltip;
  }

  positionTooltip(tooltipData) {
    if (!tooltipData.tooltipElement) return;
    
    // Obter posição e dimensões do elemento trigger
    const triggerRect = tooltipData.element.getBoundingClientRect();
    const tooltipRect = tooltipData.tooltipElement.getBoundingClientRect();
    
    // Calcular posição baseada na posição solicitada
    let top, left;
    
    switch (tooltipData.config.position) {
      case 'top':
        top = triggerRect.top - tooltipRect.height - 8;
        left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
        break;
      case 'top-left':
        top = triggerRect.top - tooltipRect.height - 8;
        left = triggerRect.left;
        break;
      case 'top-right':
        top = triggerRect.top - tooltipRect.height - 8;
        left = triggerRect.right - tooltipRect.width;
        break;
      case 'bottom':
        top = triggerRect.bottom + 8;
        left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
        break;
      case 'bottom-left':
        top = triggerRect.bottom + 8;
        left = triggerRect.left;
        break;
      case 'bottom-right':
        top = triggerRect.bottom + 8;
        left = triggerRect.right - tooltipRect.width;
        break;
      case 'left':
        top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
        left = triggerRect.left - tooltipRect.width - 8;
        break;
      case 'right':
        top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
        left = triggerRect.right + 8;
        break;
      default:
        top = triggerRect.top - tooltipRect.height - 8;
        left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
    }
    
    // Ajustar para manter dentro da viewport
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // Ajustar horizontalmente
    if (left < 8) {
      left = 8;
    } else if (left + tooltipRect.width > viewportWidth - 8) {
      left = viewportWidth - tooltipRect.width - 8;
    }
    
    // Ajustar verticalmente
    if (top < 8) {
      top = 8;
    } else if (top + tooltipRect.height > viewportHeight - 8) {
      top = viewportHeight - tooltipRect.height - 8;
    }
    
    // Aplicar posição
    tooltipData.tooltipElement.style.top = `${top}px`;
    tooltipData.tooltipElement.style.left = `${left}px`;
  }

  showHelp(helpId) {
    const helpData = this.helpElements.get(helpId);
    if (!helpData) return;
    
    // Fechar ajuda atual se houver
    if (this.currentHelp && this.currentHelp !== helpId) {
      this.hideHelp(this.currentHelp);
    }
    
    // Criar elemento da ajuda se não existir
    if (!helpData.helpElement) {
      helpData.helpElement = this.createHelpElement(helpData);
      document.body.appendChild(helpData.helpElement);
    }
    
    // Posicionar ajuda
    this.positionHelp(helpData);
    
    // Mostrar ajuda
    helpData.helpElement.classList.add('help-content--visible');
    helpData.isVisible = true;
    this.currentHelp = helpId;
    
    // Disparar evento personalizado
    helpData.element.dispatchEvent(new CustomEvent('helpShow', {
      detail: { help: helpData.helpElement }
    }));
  }

  hideHelp(helpId) {
    const helpData = this.helpElements.get(helpId);
    if (!helpData || !helpData.isVisible) return;
    
    // Ocultar ajuda
    if (helpData.helpElement) {
      helpData.helpElement.classList.remove('help-content--visible');
    }
    
    helpData.isVisible = false;
    this.currentHelp = null;
    
    // Disparar evento personalizado
    helpData.element.dispatchEvent(new CustomEvent('helpHide', {
      detail: { help: helpData.helpElement }
    }));
  }

  createHelpElement(helpData) {
    const help = document.createElement('div');
    help.className = `help-content help-content--${helpData.config.position}`;
    
    // Criar conteúdo da ajuda
    let content = `
      <div class="help-content-inner">
        ${helpData.config.title ? `<h4 class="help-title">${helpData.config.title}</h4>` : ''}
        <div class="help-text">${helpData.config.content}</div>
        ${helpData.config.imageUrl ? `
          <div class="help-image-container">
            <img src="${helpData.config.imageUrl}" alt="${helpData.config.imageCaption || 'Imagem de ajuda'}" class="help-image">
            ${helpData.config.imageCaption ? `<p class="help-image-caption">${helpData.config.imageCaption}</p>` : ''}
          </div>
        ` : ''}
      </div>
    `;
    
    help.innerHTML = content;
    return help;
  }

  positionHelp(helpData) {
    if (!helpData.helpElement) return;
    
    // Obter posição e dimensões do elemento trigger
    const triggerRect = helpData.element.getBoundingClientRect();
    const helpRect = helpData.helpElement.getBoundingClientRect();
    
    // Calcular posição baseada na posição solicitada
    let top, left;
    
    switch (helpData.config.position) {
      case 'top':
        top = triggerRect.top - helpRect.height - 8;
        left = triggerRect.left + (triggerRect.width / 2) - (helpRect.width / 2);
        break;
      case 'bottom':
        top = triggerRect.bottom + 8;
        left = triggerRect.left + (triggerRect.width / 2) - (helpRect.width / 2);
        break;
      case 'left':
        top = triggerRect.top + (triggerRect.height / 2) - (helpRect.height / 2);
        left = triggerRect.left - helpRect.width - 8;
        break;
      case 'right':
        top = triggerRect.top + (triggerRect.height / 2) - (helpRect.height / 2);
        left = triggerRect.right + 8;
        break;
      default:
        top = triggerRect.bottom + 8;
        left = triggerRect.left + (triggerRect.width / 2) - (helpRect.width / 2);
    }
    
    // Ajustar para manter dentro da viewport
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // Ajustar horizontalmente
    if (left < 8) {
      left = 8;
    } else if (left + helpRect.width > viewportWidth - 8) {
      left = viewportWidth - helpRect.width - 8;
    }
    
    // Ajustar verticalmente
    if (top < 8) {
      top = 8;
    } else if (top + helpRect.height > viewportHeight - 8) {
      top = viewportHeight - helpRect.height - 8;
    }
    
    // Aplicar posição
    helpData.helpElement.style.top = `${top}px`;
    helpData.helpElement.style.left = `${left}px`;
  }

  closeAll(clickEvent) {
    // Fechar tooltip atual se clicar fora
    if (this.currentTooltip) {
      const tooltipData = this.tooltips.get(this.currentTooltip);
      if (tooltipData && tooltipData.tooltipElement) {
        if (!clickEvent || 
            (!tooltipData.element.contains(clickEvent.target) && 
             !tooltipData.tooltipElement.contains(clickEvent.target))) {
          this.hideTooltip(this.currentTooltip);
        }
      }
    }
    
    // Fechar ajuda atual se clicar fora
    if (this.currentHelp) {
      const helpData = this.helpElements.get(this.currentHelp);
      if (helpData && helpData.helpElement) {
        if (!clickEvent || 
            (!helpData.element.contains(clickEvent.target) && 
             !helpData.helpElement.contains(clickEvent.target))) {
          this.hideHelp(this.currentHelp);
        }
      }
    }
  }

  observeDOM() {
    // Observar mudanças no DOM para inicializar novos elementos
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Verificar se novos elementos de tooltip foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-tooltip')) {
              this.initTooltip(node);
            }
            
            // Verificar se novos elementos de ajuda foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-help')) {
              this.initHelp(node);
            }
            
            // Verificar elementos filhos
            node.querySelectorAll && node.querySelectorAll('[data-tooltip]').forEach(tooltipElement => {
              this.initTooltip(tooltipElement);
            });
            
            node.querySelectorAll && node.querySelectorAll('[data-help]').forEach(helpElement => {
              this.initHelp(helpElement);
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
  getTooltip(tooltipId) {
    return this.tooltips.get(tooltipId);
  }

  getHelp(helpId) {
    return this.helpElements.get(helpId);
  }

  showTooltipById(tooltipId) {
    this.showTooltip(tooltipId);
  }

  hideTooltipById(tooltipId) {
    this.hideTooltip(tooltipId);
  }

  showHelpById(helpId) {
    this.showHelp(helpId);
  }

  hideHelpById(helpId) {
    this.hideHelp(helpId);
  }
}

// Inicializar gerenciador quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.tooltipManager = new TooltipManager();
});

// Expôr funções globalmente para uso em templates
window.initTooltip = (selector) => {
  const tooltipElement = document.querySelector(selector);
  if (tooltipElement && window.tooltipManager) {
    window.tooltipManager.initTooltip(tooltipElement);
  }
};

window.initHelp = (selector) => {
  const helpElement = document.querySelector(selector);
  if (helpElement && window.tooltipManager) {
    window.tooltipManager.initHelp(helpElement);
  }
};

window.showTooltip = (tooltipId) => {
  if (window.tooltipManager) {
    window.tooltipManager.showTooltipById(tooltipId);
  }
};

window.hideTooltip = (tooltipId) => {
  if (window.tooltipManager) {
    window.tooltipManager.hideTooltipById(tooltipId);
  }
};

window.showHelp = (helpId) => {
  if (window.tooltipManager) {
    window.tooltipManager.showHelpById(helpId);
  }
};

window.hideHelp = (helpId) => {
  if (window.tooltipManager) {
    window.tooltipManager.hideHelpById(helpId);
  }
};