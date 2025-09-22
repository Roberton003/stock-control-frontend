// Importar Alpine.js
import Alpine from 'alpinejs';

// Importar gerenciador de tema
import './theme-manager.js';

// Importar validador de formulários
import './form-validator.js';

// Importar gerenciador de estados
import './state-manager.js';

// Importar gerenciador de abas e accordions
import './tabs-accordion.js';

// Importar gerenciador de tooltips e ajuda contextual
import './tooltip-manager.js';

// Importar gerenciador de navegação entre entidades
import './entity-navigation.js';

// Importar gerenciador de formulários intuitivos
import './intuitive-forms.js';

// Importar gerenciador de autocomplete e seletores inteligentes
import './autocomplete-manager.js';

// Utilitários básicos
window.utils = {
  showToast(message, type = 'info') {
    // Implementação de toast notification
    console.log(`${type.toUpperCase()}: ${message}`);
  },
  
  formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  },
  
  // Funções de tema
  toggleTheme() {
    if (window.themeManager) {
      window.themeManager.toggleTheme();
    }
  },
  
  getCurrentTheme() {
    if (window.themeManager) {
      return window.themeManager.getCurrentTheme();
    }
    return 'light';
  }
};

// Inicializar Alpine
window.Alpine = Alpine;
Alpine.start();

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
  console.log('Frontend inicializado');
});
