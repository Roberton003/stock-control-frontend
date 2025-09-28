/*
 * Validador de Formulários em Tempo Real
 * Sistema para validação instantânea de formulários laboratoriais
 */

class FormValidator {
  constructor(formElement) {
    this.form = formElement;
    this.fields = {};
    this.errors = {};
    this.init();
  }

  init() {
    // Encontrar todos os campos do formulário com atributos de validação
    const inputFields = this.form.querySelectorAll('input, select, textarea');
    
    inputFields.forEach(field => {
      const fieldName = field.name || field.id;
      if (fieldName) {
        this.addField(fieldName, field);
      }
    });
    
    // Adicionar eventos de validação
    this.setupValidationEvents();
  }

  addField(fieldName, fieldElement) {
    this.fields[fieldName] = {
      element: fieldElement,
      validations: this.extractValidations(fieldElement),
      isValid: true,
      errors: []
    };
  }

  extractValidations(fieldElement) {
    const validations = {};
    
    // Validações baseadas em atributos HTML5
    if (fieldElement.hasAttribute('required')) {
      validations.required = true;
    }
    
    if (fieldElement.hasAttribute('minlength')) {
      validations.minLength = parseInt(fieldElement.getAttribute('minlength'));
    }
    
    if (fieldElement.hasAttribute('maxlength')) {
      validations.maxLength = parseInt(fieldElement.getAttribute('maxlength'));
    }
    
    if (fieldElement.hasAttribute('min')) {
      validations.min = parseFloat(fieldElement.getAttribute('min'));
    }
    
    if (fieldElement.hasAttribute('max')) {
      validations.max = parseFloat(fieldElement.getAttribute('max'));
    }
    
    if (fieldElement.hasAttribute('pattern')) {
      validations.pattern = new RegExp(fieldElement.getAttribute('pattern'));
    }
    
    // Validações específicas para laboratório
    if (fieldElement.hasAttribute('data-validate-sku')) {
      validations.sku = true;
    }
    
    if (fieldElement.hasAttribute('data-validate-quantity')) {
      validations.quantity = true;
    }
    
    if (fieldElement.hasAttribute('data-validate-date')) {
      validations.date = true;
    }
    
    if (fieldElement.hasAttribute('data-validate-email')) {
      validations.email = true;
    }
    
    return validations;
  }

  setupValidationEvents() {
    Object.keys(this.fields).forEach(fieldName => {
      const field = this.fields[fieldName];
      
      // Validar no blur (quando o campo perde o foco)
      field.element.addEventListener('blur', () => {
        this.validateField(fieldName);
      });
      
      // Validar enquanto digita (debounced)
      field.element.addEventListener('input', this.debounce(() => {
        this.validateField(fieldName);
      }, 300));
    });
    
    // Validar todo o formulário antes do submit
    this.form.addEventListener('submit', (e) => {
      if (!this.validateForm()) {
        e.preventDefault();
        this.showFormErrors();
      }
    });
  }

  validateField(fieldName) {
    const field = this.fields[fieldName];
    if (!field) return;
    
    const value = field.element.value;
    const validations = field.validations;
    const errors = [];
    
    // Validação required
    if (validations.required && (!value || value.trim() === '')) {
      errors.push('Este campo é obrigatório');
    }
    
    // Validação minLength
    if (validations.minLength && value.length < validations.minLength) {
      errors.push(`O campo deve ter pelo menos ${validations.minLength} caracteres`);
    }
    
    // Validação maxLength
    if (validations.maxLength && value.length > validations.maxLength) {
      errors.push(`O campo deve ter no máximo ${validations.maxLength} caracteres`);
    }
    
    // Validação min
    if (validations.min !== undefined) {
      const numValue = parseFloat(value);
      if (!isNaN(numValue) && numValue < validations.min) {
        errors.push(`O valor mínimo é ${validations.min}`);
      }
    }
    
    // Validação max
    if (validations.max !== undefined) {
      const numValue = parseFloat(value);
      if (!isNaN(numValue) && numValue > validations.max) {
        errors.push(`O valor máximo é ${validations.max}`);
      }
    }
    
    // Validação pattern
    if (validations.pattern && value && !validations.pattern.test(value)) {
      errors.push('Formato inválido');
    }
    
    // Validações específicas para laboratório
    if (validations.sku && value) {
      if (!this.validateSKU(value)) {
        errors.push('SKU inválido. Use letras maiúsculas, números e hífens');
      }
    }
    
    if (validations.quantity && value) {
      if (!this.validateQuantity(value)) {
        errors.push('Quantidade inválida. Use números decimais positivos');
      }
    }
    
    if (validations.date && value) {
      if (!this.validateDate(value)) {
        errors.push('Data inválida. Use o formato DD/MM/AAAA');
      }
    }
    
    if (validations.email && value) {
      if (!this.validateEmail(value)) {
        errors.push('Email inválido');
      }
    }
    
    // Atualizar estado do campo
    field.isValid = errors.length === 0;
    field.errors = errors;
    
    // Mostrar feedback visual
    this.showFieldFeedback(fieldName);
    
    return field.isValid;
  }

  validateSKU(sku) {
    // SKU deve conter apenas letras maiúsculas, números e hífens
    const skuRegex = /^[A-Z0-9\-]+$/;
    return skuRegex.test(sku);
  }

  validateQuantity(quantity) {
    // Quantidade deve ser um número decimal positivo
    const quantityRegex = /^\d+(\.\d{1,4})?$/;
    return quantityRegex.test(quantity) && parseFloat(quantity) > 0;
  }

  validateDate(dateString) {
    // Validar data no formato DD/MM/AAAA
    const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    if (!dateRegex.test(dateString)) {
      return false;
    }
    
    const [, day, month, year] = dateString.match(dateRegex);
    const date = new Date(`${year}-${month}-${day}`);
    
    return date instanceof Date && 
           date.getDate() == day && 
           date.getMonth() + 1 == month && 
           date.getFullYear() == year;
  }

  validateEmail(email) {
    // Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  validateForm() {
    let isFormValid = true;
    
    Object.keys(this.fields).forEach(fieldName => {
      const isFieldValid = this.validateField(fieldName);
      if (!isFieldValid) {
        isFormValid = false;
      }
    });
    
    return isFormValid;
  }

  showFieldFeedback(fieldName) {
    const field = this.fields[fieldName];
    const fieldGroup = field.element.closest('.form-group') || field.element.parentElement;
    
    // Remover mensagens de erro anteriores
    const existingError = fieldGroup.querySelector('.form-error');
    if (existingError) {
      existingError.remove();
    }
    
    if (field.isValid) {
      // Remover classes de erro
      field.element.classList.remove('form-input--error');
      fieldGroup.classList.remove('form-group--error');
    } else {
      // Adicionar classes de erro
      field.element.classList.add('form-input--error');
      fieldGroup.classList.add('form-group--error');
      
      // Adicionar mensagem de erro
      const errorDiv = document.createElement('div');
      errorDiv.className = 'form-error';
      errorDiv.textContent = field.errors[0]; // Mostrar o primeiro erro
      fieldGroup.appendChild(errorDiv);
    }
  }

  showFormErrors() {
    // Rolagem suave para o primeiro campo com erro
    const firstErrorField = Object.values(this.fields).find(field => !field.isValid);
    if (firstErrorField) {
      firstErrorField.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      firstErrorField.element.focus();
    }
  }

  // Função debounce para limitar a frequência de execução
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

  // Métodos públicos para uso externo
  getFieldState(fieldName) {
    return this.fields[fieldName];
  }

  getFormState() {
    return {
      isValid: Object.values(this.fields).every(field => field.isValid),
      fields: this.fields
    };
  }

  clearFieldErrors(fieldName) {
    const field = this.fields[fieldName];
    if (field) {
      field.isValid = true;
      field.errors = [];
      this.showFieldFeedback(fieldName);
    }
  }

  clearAllErrors() {
    Object.keys(this.fields).forEach(fieldName => {
      this.clearFieldErrors(fieldName);
    });
  }
}

// Inicializar validadores para formulários com a classe 'form-validator'
document.addEventListener('DOMContentLoaded', () => {
  const validatorForms = document.querySelectorAll('form[data-validate="true"]');
  
  validatorForms.forEach(form => {
    new FormValidator(form);
  });
});

// Expôr classe globalmente para uso em templates
window.FormValidator = FormValidator;

// Função auxiliar para inicializar validador em formulários específicos
window.initFormValidator = (formSelector) => {
  const form = document.querySelector(formSelector);
  if (form) {
    return new FormValidator(form);
  }
  return null;
};