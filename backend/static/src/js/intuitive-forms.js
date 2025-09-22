/*
 * Gerenciador de Formulários Intuitivos
 * Script para controlar a interação e validação de formulários
 */

class IntuitiveFormManager {
  constructor() {
    this.forms = new Map();
    this.validators = new Map();
    this.init();
  }

  init() {
    // Inicializar formulários existentes
    document.querySelectorAll('[data-intuitive-form]').forEach(formElement => {
      this.initForm(formElement);
    });
    
    // Observar mudanças no DOM para inicializar novos formulários
    this.observeDOM();
    
    // Adicionar eventos globais
    this.addGlobalEvents();
  }

  initForm(formElement) {
    const formId = formElement.id || `form-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    formElement.setAttribute('id', formId);
    
    // Criar estrutura de dados para o formulário
    const formData = {
      element: formElement,
      fields: new Map(),
      isValid: true,
      errors: [],
      isSubmitting: false
    };
    
    // Inicializar campos do formulário
    this.initFormFields(formElement, formData);
    
    // Adicionar eventos ao formulário
    this.addFormEvents(formElement, formData);
    
    // Armazenar dados do formulário
    this.forms.set(formId, formData);
    
    // Disparar evento personalizado
    formElement.dispatchEvent(new CustomEvent('formInitialized', {
      detail: { formId, formData }
    }));
  }

  initFormFields(formElement, formData) {
    // Encontrar todos os campos do formulário
    const fieldElements = formElement.querySelectorAll('input, select, textarea');
    
    fieldElements.forEach(fieldElement => {
      const fieldName = fieldElement.name || fieldElement.id;
      if (!fieldName) return;
      
      // Criar estrutura de dados para o campo
      const fieldData = {
        element: fieldElement,
        name: fieldName,
        type: fieldElement.type,
        value: fieldElement.value,
        isValid: true,
        errors: [],
        validators: this.getFieldValidators(fieldElement)
      };
      
      // Adicionar eventos ao campo
      this.addFieldEvents(fieldElement, fieldData, formData);
      
      // Armazenar dados do campo
      formData.fields.set(fieldName, fieldData);
    });
  }

  getFieldValidators(fieldElement) {
    const validators = [];
    
    // Validadores baseados em atributos HTML5
    if (fieldElement.hasAttribute('required')) {
      validators.push({
        name: 'required',
        validate: (value) => value !== null && value !== undefined && value.toString().trim() !== '',
        message: 'Este campo é obrigatório'
      });
    }
    
    if (fieldElement.hasAttribute('minlength')) {
      const minLength = parseInt(fieldElement.getAttribute('minlength'));
      validators.push({
        name: 'minlength',
        validate: (value) => value === null || value === undefined || value.toString().length >= minLength,
        message: `O campo deve ter pelo menos ${minLength} caracteres`
      });
    }
    
    if (fieldElement.hasAttribute('maxlength')) {
      const maxLength = parseInt(fieldElement.getAttribute('maxlength'));
      validators.push({
        name: 'maxlength',
        validate: (value) => value === null || value === undefined || value.toString().length <= maxLength,
        message: `O campo deve ter no máximo ${maxLength} caracteres`
      });
    }
    
    if (fieldElement.hasAttribute('min')) {
      const min = parseFloat(fieldElement.getAttribute('min'));
      validators.push({
        name: 'min',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          const numValue = parseFloat(value);
          return isNaN(numValue) || numValue >= min;
        },
        message: `O valor mínimo é ${min}`
      });
    }
    
    if (fieldElement.hasAttribute('max')) {
      const max = parseFloat(fieldElement.getAttribute('max'));
      validators.push({
        name: 'max',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          const numValue = parseFloat(value);
          return isNaN(numValue) || numValue <= max;
        },
        message: `O valor máximo é ${max}`
      });
    }
    
    if (fieldElement.hasAttribute('pattern')) {
      const pattern = fieldElement.getAttribute('pattern');
      const regex = new RegExp(pattern);
      validators.push({
        name: 'pattern',
        validate: (value) => value === null || value === undefined || regex.test(value),
        message: 'Formato inválido'
      });
    }
    
    // Validadores específicos para laboratório
    if (fieldElement.hasAttribute('data-validate-sku')) {
      validators.push({
        name: 'sku',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // SKU deve conter apenas letras maiúsculas, números e hífens
          const skuRegex = /^[A-Z0-9\-]+$/;
          return skuRegex.test(value);
        },
        message: 'SKU inválido. Use letras maiúsculas, números e hífens'
      });
    }
    
    if (fieldElement.hasAttribute('data-validate-quantity')) {
      validators.push({
        name: 'quantity',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // Quantidade deve ser um número decimal positivo
          const quantityRegex = /^\d+(\.\d{1,4})?$/;
          return quantityRegex.test(value) && parseFloat(value) > 0;
        },
        message: 'Quantidade inválida. Use números decimais positivos'
      });
    }
    
    if (fieldElement.hasAttribute('data-validate-date')) {
      validators.push({
        name: 'date',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // Validar data no formato DD/MM/AAAA
          const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
          if (!dateRegex.test(value)) {
            return false;
          }
          
          const [, day, month, year] = value.match(dateRegex);
          const date = new Date(`${year}-${month}-${day}`);
          
          return date instanceof Date && 
                 date.getDate() == day && 
                 date.getMonth() + 1 == month && 
                 date.getFullYear() == year;
        },
        message: 'Data inválida. Use o formato DD/MM/AAAA'
      });
    }
    
    if (fieldElement.hasAttribute('data-validate-email')) {
      validators.push({
        name: 'email',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // Validar formato de email
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          return emailRegex.test(value);
        },
        message: 'Email inválido'
      });
    }
    
    if (fieldElement.hasAttribute('data-validate-phone')) {
      validators.push({
        name: 'phone',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // Validar formato de telefone brasileiro
          const phoneRegex = /^\(\d{2}\) \d{4,5}-\d{4}$/;
          return phoneRegex.test(value);
        },
        message: 'Telefone inválido. Use o formato (XX) XXXX-XXXX ou (XX) XXXXX-XXXX'
      });
    }
    
    if (fieldElement.hasAttribute('data-validate-cnpj')) {
      validators.push({
        name: 'cnpj',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // Validar formato de CNPJ
          const cnpjRegex = /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/;
          return cnpjRegex.test(value);
        },
        message: 'CNPJ inválido. Use o formato XX.XXX.XXX/XXXX-XX'
      });
    }
    
    if (fieldElement.hasAttribute('data-validate-cpf')) {
      validators.push({
        name: 'cpf',
        validate: (value) => {
          if (value === null || value === undefined) return true;
          // Validar formato de CPF
          const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
          return cpfRegex.test(value);
        },
        message: 'CPF inválido. Use o formato XXX.XXX.XXX-XX'
      });
    }
    
    return validators;
  }

  addFieldEvents(fieldElement, fieldData, formData) {
    // Validar no blur (quando o campo perde o foco)
    fieldElement.addEventListener('blur', () => {
      this.validateField(fieldData, formData);
    });
    
    // Validar enquanto digita (debounced)
    fieldElement.addEventListener('input', this.debounce(() => {
      this.validateField(fieldData, formData);
    }, 300));
    
    // Atualizar valor no campo
    fieldElement.addEventListener('change', () => {
      fieldData.value = fieldElement.value;
    });
  }

  addFormEvents(formElement, formData) {
    // Validar todo o formulário antes do submit
    formElement.addEventListener('submit', (e) => {
      if (!this.validateForm(formData)) {
        e.preventDefault();
        this.showFormErrors(formData);
      } else {
        // Disparar evento personalizado antes do submit
        const submitEvent = new CustomEvent('formSubmit', {
          detail: { formData, isValid: true },
          cancelable: true
        });
        
        const shouldProceed = formElement.dispatchEvent(submitEvent);
        if (!shouldProceed) {
          e.preventDefault();
        }
      }
    });
    
    // Adicionar evento para reset do formulário
    formElement.addEventListener('reset', () => {
      this.resetForm(formData);
    });
  }

  validateField(fieldData, formData) {
    fieldData.isValid = true;
    fieldData.errors = [];
    
    // Executar todos os validadores
    for (const validator of fieldData.validators) {
      if (!validator.validate(fieldData.value)) {
        fieldData.isValid = false;
        fieldData.errors.push(validator.message);
      }
    }
    
    // Mostrar feedback visual
    this.showFieldFeedback(fieldData, formData);
    
    return fieldData.isValid;
  }

  validateForm(formData) {
    let isFormValid = true;
    
    // Validar todos os campos
    for (const [fieldName, fieldData] of formData.fields) {
      const isFieldValid = this.validateField(fieldData, formData);
      if (!isFieldValid) {
        isFormValid = false;
      }
    }
    
    // Atualizar estado do formulário
    formData.isValid = isFormValid;
    
    return isFormValid;
  }

  showFieldFeedback(fieldData, formData) {
    // Remover classes de erro anteriores
    fieldData.element.classList.remove('form-field--error', 'form-field--success');
    
    // Remover mensagens de erro anteriores
    const existingError = fieldData.element.parentNode.querySelector('.form-field-error');
    if (existingError) {
      existingError.remove();
    }
    
    if (fieldData.isValid) {
      // Adicionar classe de sucesso se o campo não estiver vazio
      if (fieldData.value && fieldData.value.toString().trim() !== '') {
        fieldData.element.classList.add('form-field--success');
      }
    } else {
      // Adicionar classe de erro
      fieldData.element.classList.add('form-field--error');
      
      // Adicionar mensagem de erro
      const errorDiv = document.createElement('div');
      errorDiv.className = 'form-field-error';
      errorDiv.textContent = fieldData.errors[0]; // Mostrar o primeiro erro
      fieldData.element.parentNode.appendChild(errorDiv);
    }
  }

  showFormErrors(formData) {
    // Rolagem suave para o primeiro campo com erro
    const firstErrorField = Array.from(formData.fields.values()).find(field => !field.isValid);
    if (firstErrorField) {
      firstErrorField.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      firstErrorField.element.focus();
    }
  }

  resetForm(formData) {
    // Limpar todos os campos
    for (const [fieldName, fieldData] of formData.fields) {
      fieldData.element.value = '';
      fieldData.value = '';
      fieldData.isValid = true;
      fieldData.errors = [];
      
      // Remover classes de validação
      fieldData.element.classList.remove('form-field--error', 'form-field--success');
      
      // Remover mensagens de erro
      const existingError = fieldData.element.parentNode.querySelector('.form-field-error');
      if (existingError) {
        existingError.remove();
      }
    }
    
    // Resetar estado do formulário
    formData.isValid = true;
    formData.errors = [];
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

  // Observar mudanças no DOM
  observeDOM() {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Verificar se novos formulários foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-intuitive-form')) {
              this.initForm(node);
            }
            
            // Verificar elementos filhos
            const forms = node.querySelectorAll && node.querySelectorAll('[data-intuitive-form]');
            if (forms.length > 0) {
              forms.forEach(form => this.initForm(form));
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

  // Adicionar eventos globais
  addGlobalEvents() {
    // Adicionar atalhos de teclado
    document.addEventListener('keydown', (e) => {
      // Ctrl + Enter para submeter formulário
      if (e.ctrlKey && e.key === 'Enter') {
        const activeForm = document.querySelector('[data-intuitive-form]:focus-within');
        if (activeForm) {
          activeForm.dispatchEvent(new Event('submit'));
        }
      }
      
      // Escape para limpar campo
      if (e.key === 'Escape') {
        const activeElement = document.activeElement;
        if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'SELECT')) {
          activeElement.value = '';
          activeElement.dispatchEvent(new Event('input'));
        }
      }
    });
  }

  // Métodos públicos para uso externo
  getForm(formId) {
    return this.forms.get(formId);
  }

  getField(formId, fieldName) {
    const formData = this.forms.get(formId);
    if (!formData) return null;
    return formData.fields.get(fieldName);
  }

  validateFormField(formId, fieldName) {
    const formData = this.forms.get(formId);
    const fieldData = this.getField(formId, fieldName);
    
    if (!formData || !fieldData) return false;
    
    return this.validateField(fieldData, formData);
  }

  validateFormById(formId) {
    const formData = this.forms.get(formId);
    if (!formData) return false;
    
    return this.validateForm(formData);
  }

  showFieldError(formId, fieldName, errorMessage) {
    const fieldData = this.getField(formId, fieldName);
    if (!fieldData) return;
    
    fieldData.isValid = false;
    fieldData.errors = [errorMessage];
    
    const formData = this.forms.get(formId);
    if (formData) {
      this.showFieldFeedback(fieldData, formData);
    }
  }

  clearFieldError(formId, fieldName) {
    const fieldData = this.getField(formId, fieldName);
    if (!fieldData) return;
    
    fieldData.isValid = true;
    fieldData.errors = [];
    
    const formData = this.forms.get(formId);
    if (formData) {
      this.showFieldFeedback(fieldData, formData);
    }
  }

  resetFormById(formId) {
    const formData = this.forms.get(formId);
    if (!formData) return;
    
    this.resetForm(formData);
  }

  addCustomValidator(formId, fieldName, validator) {
    const fieldData = this.getField(formId, fieldName);
    if (!fieldData) return;
    
    fieldData.validators.push(validator);
  }

  removeCustomValidator(formId, fieldName, validatorName) {
    const fieldData = this.getField(formId, fieldName);
    if (!fieldData) return;
    
    fieldData.validators = fieldData.validators.filter(v => v.name !== validatorName);
  }
}

// Inicializar gerenciador quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.intuitiveFormManager = new IntuitiveFormManager();
});

// Expôr funções globalmente para uso em templates
window.initIntuitiveForm = (selector) => {
  const formElement = document.querySelector(selector);
  if (formElement && window.intuitiveFormManager) {
    window.intuitiveFormManager.initForm(formElement);
  }
};

window.validateFormField = (formId, fieldName) => {
  if (window.intuitiveFormManager) {
    return window.intuitiveFormManager.validateFormField(formId, fieldName);
  }
  return false;
};

window.validateFormById = (formId) => {
  if (window.intuitiveFormManager) {
    return window.intuitiveFormManager.validateFormById(formId);
  }
  return false;
};

window.showFieldError = (formId, fieldName, errorMessage) => {
  if (window.intuitiveFormManager) {
    window.intuitiveFormManager.showFieldError(formId, fieldName, errorMessage);
  }
};

window.clearFieldError = (formId, fieldName) => {
  if (window.intuitiveFormManager) {
    window.intuitiveFormManager.clearFieldError(formId, fieldName);
  }
};

window.resetFormById = (formId) => {
  if (window.intuitiveFormManager) {
    window.intuitiveFormManager.resetFormById(formId);
  }
};

window.addCustomValidator = (formId, fieldName, validator) => {
  if (window.intuitiveFormManager) {
    window.intuitiveFormManager.addCustomValidator(formId, fieldName, validator);
  }
};

window.removeCustomValidator = (formId, fieldName, validatorName) => {
  if (window.intuitiveFormManager) {
    window.intuitiveFormManager.removeCustomValidator(formId, fieldName, validatorName);
  }
};