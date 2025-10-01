// Modern Frontend Configuration
const FrontendConfig = {
  // Theme settings
  theme: {
    default: 'system', // 'light', 'dark', or 'system'
    localStorageKey: 'theme-preference'
  },

  // Animation settings
  animations: {
    enabled: true,
    duration: 300, // ms
    staggerDelay: 50 // ms
  },

  // Performance settings
  performance: {
    lazyLoad: true,
    codeSplitting: true,
    resourceHints: true
  },

  // API settings
  api: {
    baseUrl: '/api/',
    timeout: 10000, // ms
    retryAttempts: 3
  },

  // UI settings
  ui: {
    toastDuration: 3000, // ms
    modalAnimation: true,
    dropdownAnimation: true
  },

  // PWA settings
  pwa: {
    enabled: true,
    cacheVersion: 'v1',
    offlineSupport: true
  },

  // Analytics (if needed)
  analytics: {
    enabled: false,
    trackingId: null
  }
};

// Initialize configuration
class FrontendInitializer {
  constructor() {
    this.config = FrontendConfig;
    this.init();
  }

  init() {
    this.setupTheme();
    this.setupPerformance();
    this.setupAccessibility();
    this.setupPWA();
  }

  setupTheme() {
    // Initialize theme based on user preference
    const savedTheme = localStorage.getItem(this.config.theme.localStorageKey);
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    let theme = this.config.theme.default;
    
    if (savedTheme && ['light', 'dark'].includes(savedTheme)) {
      theme = savedTheme;
    } else if (this.config.theme.default === 'system') {
      theme = systemPrefersDark ? 'dark' : 'light';
    }
    
    document.documentElement.classList.add(theme);
    localStorage.setItem(this.config.theme.localStorageKey, theme);
  }

  setupPerformance() {
    // Enable performance optimizations
    if (this.config.performance.lazyLoad) {
      // Lazy loading is handled by performance.js
    }
    
    if (this.config.performance.resourceHints) {
      // Resource hints are handled by performance.js
    }
  }

  setupAccessibility() {
    // Initialize accessibility features
    // Focus management, skip links, etc.
    this.addSkipLink();
    this.setupFocusManagement();
  }

  setupPWA() {
    // Register service worker if PWA is enabled
    if (this.config.pwa.enabled && 'serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/src/js/service-worker.js')
          .then(registration => {
            console.log('SW registered: ', registration);
          })
          .catch(registrationError => {
            console.log('SW registration failed: ', registrationError);
          });
      });
    }
  }

  addSkipLink() {
    // Add skip to content link for accessibility
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Pular para o conteúdo principal';
    skipLink.className = 'skip-to-content sr-only focusable';
    document.body.insertBefore(skipLink, document.body.firstChild);
  }

  setupFocusManagement() {
    // Add focus styles for keyboard navigation
    let keyboardActive = false;
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        keyboardActive = true;
        document.body.classList.add('keyboard-navigation');
      }
    });
    
    document.addEventListener('mousedown', () => {
      keyboardActive = false;
      document.body.classList.remove('keyboard-navigation');
    });
    
    // Add focus trap for modals
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeAllModals();
      }
    });
  }

  closeAllModals() {
    // Close any open modals
    document.querySelectorAll('[data-modal-open="true"]').forEach(modal => {
      modal.setAttribute('data-modal-open', 'false');
      modal.classList.add('hidden');
    });
  }

  // Utility methods
  formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  }

  formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(new Date(date));
  }

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
  }

  // Toast notification helper
  showToast(message, type = 'info') {
    if (window.ModernToast) {
      const toast = new ModernToast();
      toast.show(message, type, this.config.ui.toastDuration);
    } else {
      // Fallback to simple alert or console
      console.log(`${type.toUpperCase()}: ${message}`);
    }
  }
}

// Initialize frontend when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.frontendApp = new FrontendInitializer();
});

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FrontendConfig;
}