// Modern JavaScript utilities for frontend
import Alpine from 'alpinejs';

// Theme management
window.theme = {
  isDark: localStorage.getItem('theme') === 'dark',
  
  init() {
    if (this.isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  },
  
  toggle() {
    this.isDark = !this.isDark;
    document.documentElement.classList.toggle('dark', this.isDark);
    localStorage.setItem('theme', this.isDark ? 'dark' : 'light');
  }
};

// Utility functions
window.utils = {
  // Toast notifications
  showToast(message, type = 'info', duration = 3000) {
    // Create toast container if it doesn't exist
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed top-4 right-4 z-50 space-y-2';
      document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `flex items-center p-4 rounded-lg shadow-lg text-white animate-fade-in ${
      type === 'success' ? 'bg-modern-success' : 
      type === 'warning' ? 'bg-modern-warning' : 
      type === 'danger' || type === 'error' ? 'bg-modern-danger' : 'bg-modern-primary'
    }`;
    toast.innerHTML = `
      <div class="flex-1">
        <p class="text-sm">${message}</p>
      </div>
      <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.remove()">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    `;
    
    container.appendChild(toast);
    
    // Remove after duration
    setTimeout(() => {
      toast.classList.add('animate-fade-out');
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, duration);
  },
  
  // Currency formatting
  formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  },
  
  // Date formatting
  formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
  },
  
  // Debounce function
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
  
  // Throttle function
  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
};

// Modal functions
window.modal = {
  open(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('hidden');
      modal.setAttribute('aria-modal', 'true');
      modal.setAttribute('aria-hidden', 'false');
      
      // Focus first element in modal
      const focusableElement = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (focusableElement) focusableElement.focus();
    }
  },
  
  close(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('hidden');
      modal.setAttribute('aria-modal', 'false');
      modal.setAttribute('aria-hidden', 'true');
    }
  }
};

// Initialize theme on DOM load
document.addEventListener('DOMContentLoaded', () => {
  theme.init();
  
  // Initialize Alpine.js
  window.Alpine = Alpine;
  Alpine.start();
  
  // Add dark mode toggle button if not exists
  if (!document.querySelector('[data-theme-toggle]')) {
    const themeToggle = document.createElement('button');
    themeToggle.setAttribute('data-theme-toggle', 'true');
    themeToggle.className = 'fixed bottom-6 right-6 z-50 p-3 bg-modern-primary text-white rounded-full shadow-lg hover:shadow-xl transition-shadow';
    themeToggle.innerHTML = `
      <svg id="theme-icon" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
      </svg>
    `;
    themeToggle.onclick = () => {
      theme.toggle();
      const icon = document.getElementById('theme-icon');
      icon.innerHTML = theme.isDark ? 
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>' : 
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>';
    };
    document.body.appendChild(themeToggle);
  }
});

// Add theme toggle event listener
document.addEventListener('click', (e) => {
  if (e.target.closest('[data-theme-toggle]')) {
    theme.toggle();
  }
});

// Enhanced form submission with HTMX-like functionality
window.enhancedFormSubmit = async function(form, callback) {
  const formData = new FormData(form);
  const action = form.getAttribute('action') || window.location.href;
  const method = form.getAttribute('method') || 'POST';
  
  try {
    const response = await fetch(action, {
      method: method,
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      if (callback) callback(data, true);
      utils.showToast('Operação realizada com sucesso!', 'success');
    } else {
      const error = await response.json();
      if (callback) callback(error, false);
      utils.showToast('Ocorreu um erro na operação', 'danger');
    }
  } catch (error) {
    console.error('Form submission error:', error);
    utils.showToast('Erro de conexão', 'danger');
    if (callback) callback({ error: 'Erro de conexão' }, false);
  }
};