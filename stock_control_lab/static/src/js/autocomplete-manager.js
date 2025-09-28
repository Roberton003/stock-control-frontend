/*
 * Gerenciador de Autocomplete e Seletores Inteligentes
 * Script para controlar a interação e funcionalidade dos componentes de autocomplete
 */

class AutocompleteManager {
  constructor() {
    this.autocompletes = new Map();
    this.smartSelectors = new Map();
    this.init();
  }

  init() {
    // Inicializar autocompletes existentes
    document.querySelectorAll('[data-autocomplete]').forEach(autocompleteElement => {
      this.initAutocomplete(autocompleteElement);
    });
    
    // Inicializar seletores inteligentes existentes
    document.querySelectorAll('[data-smart-selector]').forEach(selectorElement => {
      this.initSmartSelector(selectorElement);
    });
    
    // Observar mudanças no DOM para inicializar novos elementos
    this.observeDOM();
    
    // Adicionar eventos globais
    this.addGlobalEvents();
  }

  initAutocomplete(autocompleteElement) {
    const autocompleteId = autocompleteElement.id || `autocomplete-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    autocompleteElement.setAttribute('id', autocompleteId);
    
    // Criar estrutura de dados para o autocomplete
    const autocompleteData = {
      element: autocompleteElement,
      input: autocompleteElement.querySelector('input'),
      dropdown: null,
      options: [],
      filteredOptions: [],
      selectedIndex: -1,
      isOpen: false,
      isLoading: false,
      error: null,
      config: this.getAutocompleteConfig(autocompleteElement)
    };
    
    // Validar elementos necessários
    if (!autocompleteData.input) {
      console.warn(`Autocomplete element #${autocompleteId} is missing required input element`);
      return;
    }
    
    // Adicionar eventos ao input
    this.addAutocompleteEvents(autocompleteData);
    
    // Armazenar dados do autocomplete
    this.autocompletes.set(autocompleteId, autocompleteData);
    
    // Disparar evento personalizado
    autocompleteElement.dispatchEvent(new CustomEvent('autocompleteInitialized', {
      detail: { autocompleteId, autocompleteData }
    }));
  }

  getAutocompleteConfig(autocompleteElement) {
    return {
      minLength: parseInt(autocompleteElement.getAttribute('data-min-length')) || 1,
      maxResults: parseInt(autocompleteElement.getAttribute('data-max-results')) || 10,
      debounceTime: parseInt(autocompleteElement.getAttribute('data-debounce-time')) || 300,
      placeholder: autocompleteElement.getAttribute('data-placeholder') || 'Digite para buscar...',
      loadingText: autocompleteElement.getAttribute('data-loading-text') || 'Carregando...',
      emptyText: autocompleteElement.getAttribute('data-empty-text') || 'Nenhum resultado encontrado',
      errorText: autocompleteElement.getAttribute('data-error-text') || 'Erro ao carregar dados',
      multiple: autocompleteElement.hasAttribute('data-multiple'),
      allowCustom: autocompleteElement.hasAttribute('data-allow-custom'),
      autoFocus: autocompleteElement.hasAttribute('data-auto-focus'),
      clearOnSelect: autocompleteElement.hasAttribute('data-clear-on-select'),
      closeOnSelect: !autocompleteElement.hasAttribute('data-keep-open'),
      highlightMatches: autocompleteElement.hasAttribute('data-highlight-matches'),
      groupBy: autocompleteElement.getAttribute('data-group-by') || null,
      sortBy: autocompleteElement.getAttribute('data-sort-by') || null,
      endpoint: autocompleteElement.getAttribute('data-endpoint') || null,
      dataSource: autocompleteElement.getAttribute('data-source') || 'api',
      customData: autocompleteElement.getAttribute('data-custom-data') || null
    };
  }

  addAutocompleteEvents(autocompleteData) {
    const { element, input, config } = autocompleteData;
    
    // Debounce para limitar a frequência de chamadas
    let debounceTimer;
    
    // Evento de digitação no input
    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        this.handleInput(autocompleteData, e.target.value);
      }, config.debounceTime);
    });
    
    // Evento de foco no input
    input.addEventListener('focus', () => {
      this.handleFocus(autocompleteData);
    });
    
    // Evento de blur no input
    input.addEventListener('blur', () => {
      // Pequeno atraso para permitir cliques no dropdown
      setTimeout(() => {
        this.handleBlur(autocompleteData);
      }, 200);
    });
    
    // Evento de teclas especiais
    input.addEventListener('keydown', (e) => {
      this.handleKeydown(autocompleteData, e);
    });
    
    // Evento de colar
    input.addEventListener('paste', (e) => {
      setTimeout(() => {
        this.handleInput(autocompleteData, e.target.value);
      }, 100);
    });
    
    // Evento de mudança
    input.addEventListener('change', (e) => {
      this.handleChange(autocompleteData, e);
    });
  }

  handleInput(autocompleteData, value) {
    const { config } = autocompleteData;
    
    // Se o valor for muito curto, fechar o dropdown
    if (value.length < config.minLength) {
      this.closeDropdown(autocompleteData);
      return;
    }
    
    // Carregar opções com base no valor digitado
    this.loadOptions(autocompleteData, value);
  }

  async loadOptions(autocompleteData, searchTerm) {
    const { config } = autocompleteData;
    
    // Mostrar estado de carregamento
    this.showLoading(autocompleteData);
    
    try {
      let options = [];
      
      // Determinar fonte de dados
      if (config.dataSource === 'api' && config.endpoint) {
        // Carregar do endpoint da API
        options = await this.fetchApiOptions(autocompleteData, searchTerm);
      } else if (config.dataSource === 'custom' && config.customData) {
        // Carregar de dados personalizados
        options = this.parseCustomData(autocompleteData, config.customData, searchTerm);
      } else {
        // Carregar do elemento pai (opções pré-existentes)
        options = this.extractOptionsFromElement(autocompleteData, searchTerm);
      }
      
      // Filtrar e ordenar opções
      autocompleteData.options = this.processOptions(autocompleteData, options, searchTerm);
      autocompleteData.filteredOptions = [...autocompleteData.options];
      autocompleteData.selectedIndex = -1;
      
      // Mostrar dropdown com opções
      this.showDropdown(autocompleteData);
      
      // Disparar evento personalizado
      autocompleteData.element.dispatchEvent(new CustomEvent('optionsLoaded', {
        detail: { options: autocompleteData.options, searchTerm }
      }));
    } catch (error) {
      console.error('Error loading autocomplete options:', error);
      this.showError(autocompleteData, error.message);
      
      // Disparar evento personalizado
      autocompleteData.element.dispatchEvent(new CustomEvent('optionsLoadError', {
        detail: { error: error.message, searchTerm }
      }));
    } finally {
      this.hideLoading(autocompleteData);
    }
  }

  async fetchApiOptions(autocompleteData, searchTerm) {
    const { config } = autocompleteData;
    
    try {
      const response = await fetch(`${config.endpoint}?q=${encodeURIComponent(searchTerm)}`, {
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      throw new Error(`Falha ao carregar opções: ${error.message}`);
    }
  }

  parseCustomData(autocompleteData, customData, searchTerm) {
    try {
      // Parsear dados personalizados (JSON ou CSV)
      let data;
      
      if (customData.startsWith('[') || customData.startsWith('{')) {
        // JSON
        data = JSON.parse(customData);
      } else {
        // CSV ou texto separado por vírgulas
        data = customData.split(',').map(item => ({
          value: item.trim(),
          label: item.trim()
        }));
      }
      
      return Array.isArray(data) ? data : [data];
    } catch (error) {
      console.error('Error parsing custom data:', error);
      return [];
    }
  }

  extractOptionsFromElement(autocompleteData, searchTerm) {
    // Extrair opções de elementos filhos (select, ul, etc.)
    const selectElement = autocompleteData.element.querySelector('select');
    if (selectElement) {
      return Array.from(selectElement.options).map(option => ({
        value: option.value,
        label: option.text,
        selected: option.selected
      }));
    }
    
    const listElement = autocompleteData.element.querySelector('ul, ol');
    if (listElement) {
      return Array.from(listElement.children).map(li => ({
        value: li.getAttribute('data-value') || li.textContent,
        label: li.textContent,
        selected: li.hasAttribute('data-selected')
      }));
    }
    
    return [];
  }

  processOptions(autocompleteData, options, searchTerm) {
    const { config } = autocompleteData;
    
    // Filtrar opções com base no termo de busca
    let filteredOptions = options.filter(option => {
      const label = option.label || option.value || '';
      return label.toLowerCase().includes(searchTerm.toLowerCase());
    });
    
    // Ordenar opções
    if (config.sortBy === 'label') {
      filteredOptions.sort((a, b) => {
        const labelA = (a.label || a.value || '').toLowerCase();
        const labelB = (b.label || b.value || '').toLowerCase();
        return labelA.localeCompare(labelB);
      });
    } else if (config.sortBy === 'value') {
      filteredOptions.sort((a, b) => {
        const valueA = (a.value || '').toLowerCase();
        const valueB = (b.value || '').toLowerCase();
        return valueA.localeCompare(valueB);
      });
    }
    
    // Limitar número de resultados
    if (config.maxResults > 0) {
      filteredOptions = filteredOptions.slice(0, config.maxResults);
    }
    
    // Agrupar opções se necessário
    if (config.groupBy) {
      filteredOptions = this.groupOptions(filteredOptions, config.groupBy);
    }
    
    return filteredOptions;
  }

  groupOptions(options, groupBy) {
    const groups = {};
    
    options.forEach(option => {
      const groupKey = option[groupBy] || 'Sem grupo';
      if (!groups[groupKey]) {
        groups[groupKey] = {
          label: groupKey,
          options: []
        };
      }
      groups[groupKey].options.push(option);
    });
    
    return Object.values(groups);
  }

  showLoading(autocompleteData) {
    autocompleteData.isLoading = true;
    
    // Criar ou atualizar dropdown com estado de carregamento
    this.createOrUpdateDropdown(autocompleteData, 'loading');
  }

  hideLoading(autocompleteData) {
    autocompleteData.isLoading = false;
  }

  showError(autocompleteData, message) {
    autocompleteData.error = message;
    
    // Criar ou atualizar dropdown com mensagem de erro
    this.createOrUpdateDropdown(autocompleteData, 'error', message);
  }

  clearError(autocompleteData) {
    autocompleteData.error = null;
  }

  showDropdown(autocompleteData) {
    this.createOrUpdateDropdown(autocompleteData, 'options');
  }

  closeDropdown(autocompleteData) {
    if (autocompleteData.dropdown) {
      autocompleteData.dropdown.remove();
      autocompleteData.dropdown = null;
      autocompleteData.isOpen = false;
      autocompleteData.selectedIndex = -1;
    }
  }

  createOrUpdateDropdown(autocompleteData, type, message = null) {
    const { element, input, config } = autocompleteData;
    
    // Criar dropdown se não existir
    if (!autocompleteData.dropdown) {
      autocompleteData.dropdown = document.createElement('div');
      autocompleteData.dropdown.className = 'autocomplete-dropdown';
      autocompleteData.dropdown.setAttribute('role', 'listbox');
      
      // Posicionar dropdown
      const rect = input.getBoundingClientRect();
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      autocompleteData.dropdown.style.position = 'absolute';
      autocompleteData.dropdown.style.top = `${rect.bottom + scrollTop}px`;
      autocompleteData.dropdown.style.left = `${rect.left}px`;
      autocompleteData.dropdown.style.width = `${rect.width}px`;
      autocompleteData.dropdown.style.zIndex = '1000';
      
      // Adicionar ao body
      document.body.appendChild(autocompleteData.dropdown);
      autocompleteData.isOpen = true;
    }
    
    // Atualizar conteúdo do dropdown
    switch (type) {
      case 'loading':
        autocompleteData.dropdown.innerHTML = `
          <div class="autocomplete-message autocomplete-message--loading">
            <div class="autocomplete-spinner"></div>
            <span>${config.loadingText}</span>
          </div>
        `;
        break;
        
      case 'error':
        autocompleteData.dropdown.innerHTML = `
          <div class="autocomplete-message autocomplete-message--error">
            <svg class="w-5 h-5 mr-2 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>${message || config.errorText}</span>
          </div>
        `;
        break;
        
      case 'options':
        if (autocompleteData.filteredOptions.length === 0) {
          autocompleteData.dropdown.innerHTML = `
            <div class="autocomplete-message autocomplete-message--empty">
              <svg class="w-5 h-5 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>${config.emptyText}</span>
            </div>
          `;
        } else {
          this.renderOptions(autocompleteData);
        }
        break;
    }
  }

  renderOptions(autocompleteData) {
    const { dropdown, filteredOptions, config } = autocompleteData;
    
    let html = '';
    
    filteredOptions.forEach((option, index) => {
      if (option.options) {
        // Opção agrupada
        html += `
          <div class="autocomplete-option-group autocomplete-option-group--with-label">
            <div class="autocomplete-option-group-label">${option.label}</div>
            ${option.options.map((subOption, subIndex) => this.renderOption(autocompleteData, subOption, `${index}-${subIndex}`)).join('')}
          </div>
        `;
      } else {
        // Opção simples
        html += this.renderOption(autocompleteData, option, index);
      }
    });
    
    dropdown.innerHTML = html;
    
    // Adicionar eventos às opções
    dropdown.querySelectorAll('.autocomplete-option').forEach((optionElement, index) => {
      optionElement.addEventListener('click', (e) => {
        e.preventDefault();
        this.selectOption(autocompleteData, index);
      });
      
      optionElement.addEventListener('mouseenter', () => {
        this.highlightOption(autocompleteData, index);
      });
    });
  }

  renderOption(autocompleteData, option, index) {
    const { config } = autocompleteData;
    const isSelected = index === autocompleteData.selectedIndex;
    
    return `
      <div 
        class="autocomplete-option ${isSelected ? 'autocomplete-option--focused' : ''}"
        role="option"
        aria-selected="${isSelected}"
        data-index="${index}"
      >
        ${option.icon ? `<div class="autocomplete-option-icon">${option.icon}</div>` : ''}
        <div class="autocomplete-option-text">
          <span class="autocomplete-option-text--primary">${this.highlightText(option.label || option.value, autocompleteData.input.value, config.highlightMatches)}</span>
          ${option.secondary ? `<span class="autocomplete-option-text--secondary">${option.secondary}</span>` : ''}
        </div>
      </div>
    `;
  }

  highlightText(text, searchTerm, shouldHighlight) {
    if (!shouldHighlight || !searchTerm) {
      return text;
    }
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<span class="autocomplete-option-text--highlighted">$1</span>');
  }

  selectOption(autocompleteData, index) {
    const { config, filteredOptions } = autocompleteData;
    
    // Encontrar opção real (considerando agrupamento)
    let selectedOption = null;
    let flatIndex = 0;
    
    for (const option of filteredOptions) {
      if (option.options) {
        // Grupo
        for (const subOption of option.options) {
          if (flatIndex === index) {
            selectedOption = subOption;
            break;
          }
          flatIndex++;
        }
      } else {
        // Opção simples
        if (flatIndex === index) {
          selectedOption = option;
          break;
        }
        flatIndex++;
      }
      
      if (selectedOption) break;
    }
    
    if (!selectedOption) return;
    
    // Atualizar valor do input
    autocompleteData.input.value = selectedOption.label || selectedOption.value;
    
    // Fechar dropdown se configurado
    if (config.closeOnSelect) {
      this.closeDropdown(autocompleteData);
    }
    
    // Limpar input se configurado
    if (config.clearOnSelect) {
      setTimeout(() => {
        autocompleteData.input.value = '';
      }, 100);
    }
    
    // Disparar evento personalizado
    autocompleteData.element.dispatchEvent(new CustomEvent('optionSelected', {
      detail: { option: selectedOption, index }
    }));
  }

  highlightOption(autocompleteData, index) {
    const { dropdown } = autocompleteData;
    
    // Remover destaque atual
    dropdown.querySelectorAll('.autocomplete-option').forEach(option => {
      option.classList.remove('autocomplete-option--focused');
      option.setAttribute('aria-selected', 'false');
    });
    
    // Adicionar destaque à opção
    const optionToHighlight = dropdown.querySelector(`[data-index="${index}"]`);
    if (optionToHighlight) {
      optionToHighlight.classList.add('autocomplete-option--focused');
      optionToHighlight.setAttribute('aria-selected', 'true');
      optionToHighlight.scrollIntoView({ block: 'nearest' });
    }
    
    autocompleteData.selectedIndex = index;
  }

  handleFocus(autocompleteData) {
    // Reabrir dropdown se houver opções filtradas
    if (autocompleteData.filteredOptions && autocompleteData.filteredOptions.length > 0) {
      this.showDropdown(autocompleteData);
    }
    
    // Adicionar classe de foco
    autocompleteData.input.classList.add('autocomplete-input--focused');
    
    // Disparar evento personalizado
    autocompleteData.element.dispatchEvent(new CustomEvent('autocompleteFocused'));
  }

  handleBlur(autocompleteData) {
    // Remover classe de foco
    autocompleteData.input.classList.remove('autocomplete-input--focused');
    
    // Fechar dropdown
    this.closeDropdown(autocompleteData);
    
    // Disparar evento personalizado
    autocompleteData.element.dispatchEvent(new CustomEvent('autocompleteBlurred'));
  }

  handleChange(autocompleteData, event) {
    // Disparar evento personalizado
    autocompleteData.element.dispatchEvent(new CustomEvent('autocompleteChanged', {
      detail: { value: event.target.value, event }
    }));
  }

  handleKeydown(autocompleteData, event) {
    const { dropdown, isOpen, selectedIndex, filteredOptions } = autocompleteData;
    
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        if (!isOpen) {
          this.showDropdown(autocompleteData);
        } else if (filteredOptions.length > 0) {
          const newIndex = selectedIndex < filteredOptions.length - 1 ? selectedIndex + 1 : 0;
          this.highlightOption(autocompleteData, newIndex);
        }
        break;
        
      case 'ArrowUp':
        event.preventDefault();
        if (!isOpen) {
          this.showDropdown(autocompleteData);
        } else if (filteredOptions.length > 0) {
          const newIndex = selectedIndex > 0 ? selectedIndex - 1 : filteredOptions.length - 1;
          this.highlightOption(autocompleteData, newIndex);
        }
        break;
        
      case 'Enter':
        event.preventDefault();
        if (isOpen && selectedIndex >= 0) {
          this.selectOption(autocompleteData, selectedIndex);
        } else if (autocompleteData.config.allowCustom) {
          // Permitir valor personalizado
          this.handleCustomValue(autocompleteData);
        }
        break;
        
      case 'Escape':
        event.preventDefault();
        this.closeDropdown(autocompleteData);
        break;
        
      case 'Tab':
        // Fechar dropdown ao pressionar Tab
        this.closeDropdown(autocompleteData);
        break;
    }
  }

  handleCustomValue(autocompleteData) {
    const { input, config } = autocompleteData;
    const value = input.value.trim();
    
    if (value && config.allowCustom) {
      // Criar opção personalizada
      const customOption = {
        value: value,
        label: value,
        custom: true
      };
      
      // Disparar evento personalizado
      autocompleteData.element.dispatchEvent(new CustomEvent('customOptionCreated', {
        detail: { option: customOption }
      }));
      
      // Fechar dropdown
      this.closeDropdown(autocompleteData);
    }
  }

  // Métodos para seletores inteligentes
  initSmartSelector(selectorElement) {
    const selectorId = selectorElement.id || `smart-selector-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    selectorElement.setAttribute('id', selectorId);
    
    // Criar estrutura de dados para o seletor inteligente
    const selectorData = {
      element: selectorElement,
      input: selectorElement.querySelector('input'),
      dropdown: null,
      options: [],
      filteredOptions: [],
      selectedOptions: [],
      selectedIndex: -1,
      isOpen: false,
      isLoading: false,
      error: null,
      config: this.getSmartSelectorConfig(selectorElement)
    };
    
    // Validar elementos necessários
    if (!selectorData.input) {
      console.warn(`Smart selector element #${selectorId} is missing required input element`);
      return;
    }
    
    // Adicionar eventos ao input
    this.addSmartSelectorEvents(selectorData);
    
    // Armazenar dados do seletor
    this.smartSelectors.set(selectorId, selectorData);
    
    // Disparar evento personalizado
    selectorElement.dispatchEvent(new CustomEvent('smartSelectorInitialized', {
      detail: { selectorId, selectorData }
    }));
  }

  getSmartSelectorConfig(selectorElement) {
    return {
      minLength: parseInt(selectorElement.getAttribute('data-min-length')) || 1,
      maxResults: parseInt(selectorElement.getAttribute('data-max-results')) || 10,
      debounceTime: parseInt(selectorElement.getAttribute('data-debounce-time')) || 300,
      placeholder: selectorElement.getAttribute('data-placeholder') || 'Selecione opções...',
      loadingText: selectorElement.getAttribute('data-loading-text') || 'Carregando...',
      emptyText: selectorElement.getAttribute('data-empty-text') || 'Nenhuma opção encontrada',
      errorText: selectorElement.getAttribute('data-error-text') || 'Erro ao carregar opções',
      multiple: selectorElement.hasAttribute('data-multiple'),
      allowCustom: selectorElement.hasAttribute('data-allow-custom'),
      autoFocus: selectorElement.hasAttribute('data-auto-focus'),
      clearOnSelect: selectorElement.hasAttribute('data-clear-on-select'),
      closeOnSelect: !selectorElement.hasAttribute('data-keep-open'),
      highlightMatches: selectorElement.hasAttribute('data-highlight-matches'),
      groupBy: selectorElement.getAttribute('data-group-by') || null,
      sortBy: selectorElement.getAttribute('data-sort-by') || null,
      endpoint: selectorElement.getAttribute('data-endpoint') || null,
      dataSource: selectorElement.getAttribute('data-source') || 'api',
      customData: selectorElement.getAttribute('data-custom-data') || null,
      maxSelections: parseInt(selectorElement.getAttribute('data-max-selections')) || 0
    };
  }

  addSmartSelectorEvents(selectorData) {
    const { element, input, config } = selectorData;
    
    // Debounce para limitar a frequência de chamadas
    let debounceTimer;
    
    // Evento de digitação no input
    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        this.handleSmartSelectorInput(selectorData, e.target.value);
      }, config.debounceTime);
    });
    
    // Evento de foco no input
    input.addEventListener('focus', () => {
      this.handleSmartSelectorFocus(selectorData);
    });
    
    // Evento de blur no input
    input.addEventListener('blur', () => {
      // Pequeno atraso para permitir cliques no dropdown
      setTimeout(() => {
        this.handleSmartSelectorBlur(selectorData);
      }, 200);
    });
    
    // Evento de teclas especiais
    input.addEventListener('keydown', (e) => {
      this.handleSmartSelectorKeydown(selectorData, e);
    });
    
    // Evento de colar
    input.addEventListener('paste', (e) => {
      setTimeout(() => {
        this.handleSmartSelectorInput(selectorData, e.target.value);
      }, 100);
    });
    
    // Evento de mudança
    input.addEventListener('change', (e) => {
      this.handleSmartSelectorChange(selectorData, e);
    });
  }

  handleSmartSelectorInput(selectorData, value) {
    const { config } = selectorData;
    
    // Se o valor for muito curto, fechar o dropdown
    if (value.length < config.minLength) {
      this.closeSmartSelectorDropdown(selectorData);
      return;
    }
    
    // Carregar opções com base no valor digitado
    this.loadSmartSelectorOptions(selectorData, value);
  }

  async loadSmartSelectorOptions(selectorData, searchTerm) {
    const { config } = selectorData;
    
    // Mostrar estado de carregamento
    this.showSmartSelectorLoading(selectorData);
    
    try {
      let options = [];
      
      // Determinar fonte de dados
      if (config.dataSource === 'api' && config.endpoint) {
        // Carregar do endpoint da API
        options = await this.fetchApiOptions(selectorData, searchTerm);
      } else if (config.dataSource === 'custom' && config.customData) {
        // Carregar de dados personalizados
        options = this.parseCustomData(selectorData, config.customData, searchTerm);
      } else {
        // Carregar do elemento pai (opções pré-existentes)
        options = this.extractOptionsFromElement(selectorData, searchTerm);
      }
      
      // Filtrar opções já selecionadas
      const selectedValues = selectorData.selectedOptions.map(opt => opt.value);
      options = options.filter(option => !selectedValues.includes(option.value));
      
      // Filtrar e ordenar opções
      selectorData.options = this.processOptions(selectorData, options, searchTerm);
      selectorData.filteredOptions = [...selectorData.options];
      selectorData.selectedIndex = -1;
      
      // Mostrar dropdown com opções
      this.showSmartSelectorDropdown(selectorData);
      
      // Disparar evento personalizado
      selectorData.element.dispatchEvent(new CustomEvent('optionsLoaded', {
        detail: { options: selectorData.options, searchTerm }
      }));
    } catch (error) {
      console.error('Error loading smart selector options:', error);
      this.showSmartSelectorError(selectorData, error.message);
      
      // Disparar evento personalizado
      selectorData.element.dispatchEvent(new CustomEvent('optionsLoadError', {
        detail: { error: error.message, searchTerm }
      }));
    } finally {
      this.hideSmartSelectorLoading(selectorData);
    }
  }

  showSmartSelectorLoading(selectorData) {
    selectorData.isLoading = true;
    
    // Criar ou atualizar dropdown com estado de carregamento
    this.createOrUpdateSmartSelectorDropdown(selectorData, 'loading');
  }

  hideSmartSelectorLoading(selectorData) {
    selectorData.isLoading = false;
  }

  showSmartSelectorError(selectorData, message) {
    selectorData.error = message;
    
    // Criar ou atualizar dropdown com mensagem de erro
    this.createOrUpdateSmartSelectorDropdown(selectorData, 'error', message);
  }

  clearSmartSelectorError(selectorData) {
    selectorData.error = null;
  }

  showSmartSelectorDropdown(selectorData) {
    this.createOrUpdateSmartSelectorDropdown(selectorData, 'options');
  }

  closeSmartSelectorDropdown(selectorData) {
    if (selectorData.dropdown) {
      selectorData.dropdown.remove();
      selectorData.dropdown = null;
      selectorData.isOpen = false;
      selectorData.selectedIndex = -1;
    }
  }

  createOrUpdateSmartSelectorDropdown(selectorData, type, message = null) {
    const { element, input, config } = selectorData;
    
    // Criar dropdown se não existir
    if (!selectorData.dropdown) {
      selectorData.dropdown = document.createElement('div');
      selectorData.dropdown.className = 'smart-selector-dropdown';
      selectorData.dropdown.setAttribute('role', 'listbox');
      
      // Posicionar dropdown
      const rect = input.getBoundingClientRect();
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      selectorData.dropdown.style.position = 'absolute';
      selectorData.dropdown.style.top = `${rect.bottom + scrollTop}px`;
      selectorData.dropdown.style.left = `${rect.left}px`;
      selectorData.dropdown.style.width = `${rect.width}px`;
      selectorData.dropdown.style.zIndex = '1000';
      
      // Adicionar ao body
      document.body.appendChild(selectorData.dropdown);
      selectorData.isOpen = true;
    }
    
    // Atualizar conteúdo do dropdown
    switch (type) {
      case 'loading':
        selectorData.dropdown.innerHTML = `
          <div class="smart-selector-message smart-selector-message--loading">
            <div class="smart-selector-spinner"></div>
            <span>${config.loadingText}</span>
          </div>
        `;
        break;
        
      case 'error':
        selectorData.dropdown.innerHTML = `
          <div class="smart-selector-message smart-selector-message--error">
            <svg class="w-5 h-5 mr-2 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>${message || config.errorText}</span>
          </div>
        `;
        break;
        
      case 'options':
        if (selectorData.filteredOptions.length === 0) {
          selectorData.dropdown.innerHTML = `
            <div class="smart-selector-message smart-selector-message--empty">
              <svg class="w-5 h-5 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>${config.emptyText}</span>
            </div>
          `;
        } else {
          this.renderSmartSelectorOptions(selectorData);
        }
        break;
    }
  }

  renderSmartSelectorOptions(selectorData) {
    const { dropdown, filteredOptions, config } = selectorData;
    
    let html = '';
    
    filteredOptions.forEach((option, index) => {
      if (option.options) {
        // Opção agrupada
        html += `
          <div class="smart-selector-group smart-selector-group--with-label">
            <div class="smart-selector-group-label">${option.label}</div>
            ${option.options.map((subOption, subIndex) => this.renderSmartSelectorOption(selectorData, subOption, `${index}-${subIndex}`)).join('')}
          </div>
        `;
      } else {
        // Opção simples
        html += this.renderSmartSelectorOption(selectorData, option, index);
      }
    });
    
    dropdown.innerHTML = html;
    
    // Adicionar eventos às opções
    dropdown.querySelectorAll('.smart-selector-option').forEach((optionElement, index) => {
      optionElement.addEventListener('click', (e) => {
        e.preventDefault();
        this.selectSmartSelectorOption(selectorData, index);
      });
      
      optionElement.addEventListener('mouseenter', () => {
        this.highlightSmartSelectorOption(selectorData, index);
      });
    });
  }

  renderSmartSelectorOption(selectorData, option, index) {
    const { config } = selectorData;
    const isSelected = index === selectorData.selectedIndex;
    
    return `
      <div 
        class="smart-selector-option ${isSelected ? 'smart-selector-option--focused' : ''}"
        role="option"
        aria-selected="${isSelected}"
        data-index="${index}"
      >
        ${option.icon ? `<div class="smart-selector-option-icon">${option.icon}</div>` : ''}
        <div class="smart-selector-option-text">
          <span class="smart-selector-option-text--primary">${this.highlightText(option.label || option.value, selectorData.input.value, config.highlightMatches)}</span>
          ${option.secondary ? `<span class="smart-selector-option-text--secondary">${option.secondary}</span>` : ''}
        </div>
      </div>
    `;
  }

  selectSmartSelectorOption(selectorData, index) {
    const { config, filteredOptions } = selectorData;
    
    // Encontrar opção real (considerando agrupamento)
    let selectedOption = null;
    let flatIndex = 0;
    
    for (const option of filteredOptions) {
      if (option.options) {
        // Grupo
        for (const subOption of option.options) {
          if (flatIndex === index) {
            selectedOption = subOption;
            break;
          }
          flatIndex++;
        }
      } else {
        // Opção simples
        if (flatIndex === index) {
          selectedOption = option;
          break;
        }
        flatIndex++;
      }
      
      if (selectedOption) break;
    }
    
    if (!selectedOption) return;
    
    // Verificar limite de seleções
    if (config.maxSelections > 0 && selectorData.selectedOptions.length >= config.maxSelections) {
      // Disparar evento de erro
      selectorData.element.dispatchEvent(new CustomEvent('selectionLimitReached', {
        detail: { maxSelections: config.maxSelections }
      }));
      return;
    }
    
    // Adicionar opção às seleções
    selectorData.selectedOptions.push(selectedOption);
    
    // Atualizar valor do input
    if (config.multiple) {
      selectorData.input.value = selectorData.selectedOptions.map(opt => opt.label || opt.value).join(', ');
    } else {
      selectorData.input.value = selectedOption.label || selectedOption.value;
    }
    
    // Fechar dropdown se configurado
    if (config.closeOnSelect && !config.multiple) {
      this.closeSmartSelectorDropdown(selectorData);
    }
    
    // Limpar input se configurado
    if (config.clearOnSelect) {
      setTimeout(() => {
        selectorData.input.value = '';
      }, 100);
    }
    
    // Disparar evento personalizado
    selectorData.element.dispatchEvent(new CustomEvent('optionSelected', {
      detail: { option: selectedOption, index, selectedOptions: selectorData.selectedOptions }
    }));
  }

  highlightSmartSelectorOption(selectorData, index) {
    const { dropdown } = selectorData;
    
    // Remover destaque atual
    dropdown.querySelectorAll('.smart-selector-option').forEach(option => {
      option.classList.remove('smart-selector-option--focused');
      option.setAttribute('aria-selected', 'false');
    });
    
    // Adicionar destaque à opção
    const optionToHighlight = dropdown.querySelector(`[data-index="${index}"]`);
    if (optionToHighlight) {
      optionToHighlight.classList.add('smart-selector-option--focused');
      optionToHighlight.setAttribute('aria-selected', 'true');
      optionToHighlight.scrollIntoView({ block: 'nearest' });
    }
    
    selectorData.selectedIndex = index;
  }

  handleSmartSelectorFocus(selectorData) {
    // Reabrir dropdown se houver opções filtradas
    if (selectorData.filteredOptions && selectorData.filteredOptions.length > 0) {
      this.showSmartSelectorDropdown(selectorData);
    }
    
    // Adicionar classe de foco
    selectorData.input.classList.add('smart-selector-input--focused');
    
    // Disparar evento personalizado
    selectorData.element.dispatchEvent(new CustomEvent('smartSelectorFocused'));
  }

  handleSmartSelectorBlur(selectorData) {
    // Remover classe de foco
    selectorData.input.classList.remove('smart-selector-input--focused');
    
    // Fechar dropdown
    this.closeSmartSelectorDropdown(selectorData);
    
    // Disparar evento personalizado
    selectorData.element.dispatchEvent(new CustomEvent('smartSelectorBlurred'));
  }

  handleSmartSelectorChange(selectorData, event) {
    // Disparar evento personalizado
    selectorData.element.dispatchEvent(new CustomEvent('smartSelectorChanged', {
      detail: { value: event.target.value, event }
    }));
  }

  handleSmartSelectorKeydown(selectorData, event) {
    const { dropdown, isOpen, selectedIndex, filteredOptions } = selectorData;
    
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        if (!isOpen) {
          this.showSmartSelectorDropdown(selectorData);
        } else if (filteredOptions.length > 0) {
          const newIndex = selectedIndex < filteredOptions.length - 1 ? selectedIndex + 1 : 0;
          this.highlightSmartSelectorOption(selectorData, newIndex);
        }
        break;
        
      case 'ArrowUp':
        event.preventDefault();
        if (!isOpen) {
          this.showSmartSelectorDropdown(selectorData);
        } else if (filteredOptions.length > 0) {
          const newIndex = selectedIndex > 0 ? selectedIndex - 1 : filteredOptions.length - 1;
          this.highlightSmartSelectorOption(selectorData, newIndex);
        }
        break;
        
      case 'Enter':
        event.preventDefault();
        if (isOpen && selectedIndex >= 0) {
          this.selectSmartSelectorOption(selectorData, selectedIndex);
        } else if (selectorData.config.allowCustom) {
          // Permitir valor personalizado
          this.handleSmartSelectorCustomValue(selectorData);
        }
        break;
        
      case 'Escape':
        event.preventDefault();
        this.closeSmartSelectorDropdown(selectorData);
        break;
        
      case 'Tab':
        // Fechar dropdown ao pressionar Tab
        this.closeSmartSelectorDropdown(selectorData);
        break;
        
      case 'Delete':
      case 'Backspace':
        // Remover última seleção em modo múltiplo
        if (selectorData.config.multiple && selectorData.selectedOptions.length > 0 && selectorData.input.value === '') {
          event.preventDefault();
          this.removeLastSelectedOption(selectorData);
        }
        break;
    }
  }

  handleSmartSelectorCustomValue(selectorData) {
    const { input, config } = selectorData;
    const value = input.value.trim();
    
    if (value && config.allowCustom) {
      // Criar opção personalizada
      const customOption = {
        value: value,
        label: value,
        custom: true
      };
      
      // Disparar evento personalizado
      selectorData.element.dispatchEvent(new CustomEvent('customOptionCreated', {
        detail: { option: customOption }
      }));
      
      // Fechar dropdown
      this.closeSmartSelectorDropdown(selectorData);
    }
  }

  removeLastSelectedOption(selectorData) {
    if (selectorData.selectedOptions.length > 0) {
      // Remover última opção
      const removedOption = selectorData.selectedOptions.pop();
      
      // Atualizar valor do input
      if (selectorData.config.multiple) {
        selectorData.input.value = selectorData.selectedOptions.map(opt => opt.label || opt.value).join(', ');
      } else {
        selectorData.input.value = '';
      }
      
      // Disparar evento personalizado
      selectorData.element.dispatchEvent(new CustomEvent('optionRemoved', {
        detail: { option: removedOption, removedOptions: [removedOption] }
      }));
    }
  }

  // Métodos públicos para uso externo
  getAutocomplete(autocompleteId) {
    return this.autocompletes.get(autocompleteId);
  }

  getSmartSelector(selectorId) {
    return this.smartSelectors.get(selectorId);
  }

  refreshAutocomplete(autocompleteId) {
    const autocompleteData = this.autocompletes.get(autocompleteId);
    if (autocompleteData) {
      this.loadOptions(autocompleteData, autocompleteData.input.value);
    }
  }

  refreshSmartSelector(selectorId) {
    const selectorData = this.smartSelectors.get(selectorId);
    if (selectorData) {
      this.loadSmartSelectorOptions(selectorData, selectorData.input.value);
    }
  }

  clearAutocomplete(autocompleteId) {
    const autocompleteData = this.autocompletes.get(autocompleteId);
    if (autocompleteData) {
      autocompleteData.input.value = '';
      this.closeDropdown(autocompleteData);
      autocompleteData.options = [];
      autocompleteData.filteredOptions = [];
      autocompleteData.selectedIndex = -1;
    }
  }

  clearSmartSelector(selectorId) {
    const selectorData = this.smartSelectors.get(selectorId);
    if (selectorData) {
      selectorData.input.value = '';
      this.closeSmartSelectorDropdown(selectorData);
      selectorData.options = [];
      selectorData.filteredOptions = [];
      selectorData.selectedOptions = [];
      selectorData.selectedIndex = -1;
    }
  }

  // Observar mudanças no DOM
  observeDOM() {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Verificar se novos elementos de autocomplete foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-autocomplete')) {
              this.initAutocomplete(node);
            }
            
            // Verificar se novos elementos de seletor inteligente foram adicionados
            if (node.hasAttribute && node.hasAttribute('data-smart-selector')) {
              this.initSmartSelector(node);
            }
            
            // Verificar elementos filhos
            node.querySelectorAll && node.querySelectorAll('[data-autocomplete]').forEach(autocompleteElement => {
              this.initAutocomplete(autocompleteElement);
            });
            
            node.querySelectorAll && node.querySelectorAll('[data-smart-selector]').forEach(selectorElement => {
              this.initSmartSelector(selectorElement);
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

  // Adicionar eventos globais
  addGlobalEvents() {
    // Adicionar atalhos de teclado
    document.addEventListener('keydown', (e) => {
      // ESC para fechar todos os dropdowns
      if (e.key === 'Escape') {
        this.autocompletes.forEach(autocompleteData => {
          this.closeDropdown(autocompleteData);
        });
        
        this.smartSelectors.forEach(selectorData => {
          this.closeSmartSelectorDropdown(selectorData);
        });
      }
    });
  }
}

// Inicializar gerenciador quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.autocompleteManager = new AutocompleteManager();
});

// Expôr funções globalmente para uso em templates
window.initAutocomplete = (selector) => {
  const autocompleteElement = document.querySelector(selector);
  if (autocompleteElement && window.autocompleteManager) {
    window.autocompleteManager.initAutocomplete(autocompleteElement);
  }
};

window.initSmartSelector = (selector) => {
  const selectorElement = document.querySelector(selector);
  if (selectorElement && window.autocompleteManager) {
    window.autocompleteManager.initSmartSelector(selectorElement);
  }
};

window.refreshAutocomplete = (autocompleteId) => {
  if (window.autocompleteManager) {
    window.autocompleteManager.refreshAutocomplete(autocompleteId);
  }
};

window.refreshSmartSelector = (selectorId) => {
  if (window.autocompleteManager) {
    window.autocompleteManager.refreshSmartSelector(selectorId);
  }
};

window.clearAutocomplete = (autocompleteId) => {
  if (window.autocompleteManager) {
    window.autocompleteManager.clearAutocomplete(autocompleteId);
  }
};

window.clearSmartSelector = (selectorId) => {
  if (window.autocompleteManager) {
    window.autocompleteManager.clearSmartSelector(selectorId);
  }
};