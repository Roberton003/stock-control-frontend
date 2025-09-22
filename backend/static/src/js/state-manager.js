/*
 * Gerenciador de Estados de Loading e Erro
 * Script para controlar estados visuais de carregamento e erro
 */

class StateManager {
  constructor() {
    this.loadingStates = new Map();
    this.errorStates = new Map();
  }

  // Mostrar estado de loading
  showLoading(elementId, options = {}) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const {
      type = 'spinner', // spinner, skeleton, progress
      message = '',
      overlay = false,
      fullscreen = false
    } = options;
    
    // Salvar estado atual para restauração posterior
    this.loadingStates.set(elementId, {
      html: element.innerHTML,
      classes: element.className
    });
    
    // Criar elemento de loading
    let loadingHtml = '';
    
    switch (type) {
      case 'spinner':
        loadingHtml = this.createSpinnerLoading(message, fullscreen);
        break;
      case 'skeleton':
        loadingHtml = this.createSkeletonLoading(options.skeletonCount || 3);
        break;
      case 'progress':
        loadingHtml = this.createProgressLoading(message);
        break;
      default:
        loadingHtml = this.createSpinnerLoading(message, fullscreen);
    }
    
    // Aplicar loading
    if (overlay) {
      const overlayElement = document.createElement('div');
      overlayElement.className = 'loading-container--overlay';
      overlayElement.innerHTML = loadingHtml;
      element.style.position = 'relative';
      element.appendChild(overlayElement);
    } else {
      element.innerHTML = loadingHtml;
      if (fullscreen) {
        element.className = 'loading-container--fullscreen';
      } else {
        element.className = 'loading-container';
      }
    }
  }
  
  // Esconder estado de loading
  hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const savedState = this.loadingStates.get(elementId);
    if (savedState) {
      element.innerHTML = savedState.html;
      element.className = savedState.classes;
      this.loadingStates.delete(elementId);
    } else {
      element.innerHTML = '';
      element.className = '';
    }
  }
  
  // Mostrar estado de erro
  showError(elementId, error, options = {}) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const {
      title = 'Ocorreu um erro',
      message = 'Não foi possível carregar os dados.',
      retryCallback = null,
      fullscreen = false
    } = options;
    
    // Salvar estado atual
    this.errorStates.set(elementId, {
      html: element.innerHTML,
      classes: element.className
    });
    
    // Criar elemento de erro
    const errorHtml = this.createErrorElement(title, message, retryCallback);
    
    element.innerHTML = errorHtml;
    if (fullscreen) {
      element.className = 'error-container--fullscreen';
    } else {
      element.className = 'error-container';
    }
  }
  
  // Esconder estado de erro
  hideError(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const savedState = this.errorStates.get(elementId);
    if (savedState) {
      element.innerHTML = savedState.html;
      element.className = savedState.classes;
      this.errorStates.delete(elementId);
    } else {
      element.innerHTML = '';
      element.className = '';
    }
  }
  
  // Mostrar estado vazio
  showEmptyState(elementId, options = {}) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const {
      icon = 'folder-open',
      title = 'Nenhum item encontrado',
      message = 'Não há itens para exibir neste momento.',
      actionText = '',
      actionCallback = null
    } = options;
    
    const emptyHtml = this.createEmptyState(icon, title, message, actionText, actionCallback);
    
    element.innerHTML = emptyHtml;
    element.className = 'empty-state';
  }
  
  // Criar spinner de loading
  createSpinnerLoading(message = '', fullscreen = false) {
    return `
      <div class="flex flex-col items-center justify-center ${fullscreen ? 'h-full' : ''}">
        <div class="loading-spinner loading-spinner--large"></div>
        ${message ? `<p class="loading-text ${fullscreen ? 'loading-text--centered' : ''}">${message}</p>` : ''}
      </div>
    `;
  }
  
  // Criar skeleton loading
  createSkeletonLoading(count = 3) {
    let skeletonHtml = '<div class="space-y-4 w-full">';
    
    for (let i = 0; i < count; i++) {
      skeletonHtml += `
        <div class="lab-loading-row">
          <div class="lab-loading-avatar"></div>
          <div class="lab-loading-text-group">
            <div class="lab-loading-text-line"></div>
            <div class="lab-loading-text-line lab-loading-text-line--short"></div>
          </div>
        </div>
      `;
    }
    
    skeletonHtml += '</div>';
    return skeletonHtml;
  }
  
  // Criar progress loading
  createProgressLoading(message = '') {
    return `
      <div class="w-full max-w-md">
        ${message ? `<p class="loading-text mb-4 text-center">${message}</p>` : ''}
        <div class="loading-progress">
          <div class="loading-progress-bar loading-progress--indeterminate"></div>
        </div>
      </div>
    `;
  }
  
  // Criar elemento de erro
  createErrorElement(title, message, retryCallback) {
    return `
      <div class="flex flex-col items-center justify-center p-8">
        <svg class="error-icon error-icon--large mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h2 class="error-title error-title--large mb-2">${title}</h2>
        <p class="error-message error-message--large mb-8">${message}</p>
        <div class="error-actions">
          <button 
            class="btn btn-primary"
            onclick="${retryCallback ? retryCallback + '()' : 'location.reload()'}"
          >
            Tentar novamente
          </button>
          <button 
            class="btn btn-secondary"
            onclick="history.back()"
          >
            Voltar
          </button>
        </div>
      </div>
    `;
  }
  
  // Criar estado vazio
  createEmptyState(icon, title, message, actionText, actionCallback) {
    return `
      <div class="flex flex-col items-center justify-center p-8">
        <svg class="empty-state-icon empty-state-icon--large mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="empty-state-title">${title}</h3>
        <p class="empty-state-message">${message}</p>
        ${actionText ? `
          <button 
            class="btn btn-primary"
            onclick="${actionCallback ? actionCallback + '()' : ''}"
          >
            ${actionText}
          </button>
        ` : ''}
      </div>
    `;
  }
  
  // Mostrar toast de feedback
  showToast(message, type = 'info', duration = 3000) {
    // Remover toasts antigos
    const existingToast = document.querySelector('.feedback-toast');
    if (existingToast) {
      existingToast.remove();
    }
    
    // Criar toast
    const toast = document.createElement('div');
    toast.className = `feedback-toast feedback-toast--enter feedback-toast--${type}`;
    
    let icon = '';
    switch (type) {
      case 'success':
        icon = '<svg class="w-5 h-5 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>';
        break;
      case 'error':
        icon = '<svg class="w-5 h-5 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
        break;
      case 'warning':
        icon = '<svg class="w-5 h-5 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>';
        break;
      default:
        icon = '<svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
    }
    
    toast.innerHTML = `
      <div class="flex items-start space-x-3">
        ${icon}
        <div class="flex-1">
          <p class="text-sm font-medium">${message}</p>
        </div>
        <button class="text-gray-400 hover:text-gray-500" onclick="this.parentElement.parentElement.remove()">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    `;
    
    // Adicionar ao body
    document.body.appendChild(toast);
    
    // Animação de entrada
    setTimeout(() => {
      toast.classList.remove('feedback-toast--enter');
    }, 10);
    
    // Remover automaticamente após o tempo especificado
    if (duration > 0) {
      setTimeout(() => {
        toast.classList.add('feedback-toast--exit');
        setTimeout(() => {
          if (toast.parentElement) {
            toast.remove();
          }
        }, 300);
      }, duration);
    }
  }
}

// Inicializar gerenciador de estados quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.stateManager = new StateManager();
});

// Expôr funções globalmente para uso em templates
window.showLoading = (elementId, options) => {
  if (window.stateManager) {
    window.stateManager.showLoading(elementId, options);
  }
};

window.hideLoading = (elementId) => {
  if (window.stateManager) {
    window.stateManager.hideLoading(elementId);
  }
};

window.showError = (elementId, error, options) => {
  if (window.stateManager) {
    window.stateManager.showError(elementId, error, options);
  }
};

window.hideError = (elementId) => {
  if (window.stateManager) {
    window.stateManager.hideError(elementId);
  }
};

window.showEmptyState = (elementId, options) => {
  if (window.stateManager) {
    window.stateManager.showEmptyState(elementId, options);
  }
};

window.showToast = (message, type, duration) => {
  if (window.stateManager) {
    window.stateManager.showToast(message, type, duration);
  }
};