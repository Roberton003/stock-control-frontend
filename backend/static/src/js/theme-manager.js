/*
 * Gerenciador de Tema Dark Mode
 * Script para alternar entre temas claro e escuro
 */

class ThemeManager {
  constructor() {
    this.themeToggle = document.getElementById('theme-toggle');
    this.themeToggleCheckbox = document.getElementById('theme-toggle-checkbox');
    this.currentTheme = this.getCurrentTheme();
    this.init();
  }

  init() {
    // Aplicar tema salvo ou preferência do sistema
    this.applyTheme(this.currentTheme);
    
    // Adicionar evento ao toggle
    if (this.themeToggleCheckbox) {
      this.themeToggleCheckbox.addEventListener('change', (e) => {
        const newTheme = e.target.checked ? 'dark' : 'light';
        this.setTheme(newTheme);
      });
    }
    
    // Escutar mudanças no sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        this.applyTheme(e.matches ? 'dark' : 'light');
        this.updateToggleState(e.matches ? 'dark' : 'light');
      }
    });
  }

  getCurrentTheme() {
    // Verificar tema salvo no localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    
    // Verificar preferência do sistema
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return systemPrefersDark ? 'dark' : 'light';
  }

  setTheme(theme) {
    // Salvar tema no localStorage
    localStorage.setItem('theme', theme);
    
    // Aplicar tema
    this.applyTheme(theme);
    
    // Atualizar estado do toggle
    this.updateToggleState(theme);
  }

  applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  updateToggleState(theme) {
    if (this.themeToggleCheckbox) {
      this.themeToggleCheckbox.checked = theme === 'dark';
    }
  }

  toggleTheme() {
    const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    this.setTheme(newTheme);
  }
}

// Inicializar gerenciador de tema quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.themeManager = new ThemeManager();
});

// Expôr funções globalmente para uso em templates
window.toggleTheme = () => {
  if (window.themeManager) {
    window.themeManager.toggleTheme();
  }
};