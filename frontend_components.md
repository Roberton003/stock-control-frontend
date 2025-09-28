# 🧩 Frontend Components - Componentes Reutilizáveis (frontend_components.md)

## 🎯 Objetivo

Este documento fornece componentes Django reutilizáveis com TailwindCSS e Alpine.js para acelerar o desenvolvimento frontend.

## 📁 Estrutura de Componentes

```
templates/
├── components/
│   ├── ui/                    # Componentes básicos de UI
│   │   ├── button.html
│   │   ├── card.html
│   │   ├── modal.html
│   │   └── alert.html
│   ├── forms/                 # Componentes de formulário
│   │   ├── field.html
│   │   ├── checkbox.html
│   │   └── select.html
│   ├── layout/                # Componentes de layout
│   │   ├── navbar.html
│   │   ├── sidebar.html
│   │   └── breadcrumb.html
│   └── data/                  # Componentes de exibição de dados
│       ├── table.html
│       ├── pagination.html
│       └── search.html
```

## 🔘 Componentes de UI Básicos

### Button Component

**templates/components/ui/button.html:**
```html
{% comment %}
Uso: {% include 'components/ui/button.html' with text="Salvar" type="primary" size="md" %}
Parâmetros:
- text: Texto do botão (obrigatório)
- type: primary|secondary|danger|success (default: primary)
- size: sm|md|lg (default: md)
- icon: nome do ícone (opcional)
- disabled: true|false (default: false)
- href: URL para link (opcional - transforma em <a>)
- onclick: JavaScript onclick (opcional)
{% endcomment %}

{% if href %}
<a href="{{ href }}" 
   class="btn btn-{{ type|default:'primary' }} btn-{{ size|default:'md' }} 
          {% if disabled %}opacity-50 cursor-not-allowed{% endif %}"
   {% if disabled %}aria-disabled="true"{% endif %}
   {% if onclick %}onclick="{{ onclick }}"{% endif %}>
{% else %}
<button type="button" 
        class="btn btn-{{ type|default:'primary' }} btn-{{ size|default:'md' }}"
        {% if disabled %}disabled{% endif %}
        {% if onclick %}onclick="{{ onclick }}"{% endif %}>
{% endif %}

    {% if icon %}
    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        {% if icon == 'save' %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"></path>
        {% elif icon == 'edit' %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
        {% elif icon == 'delete' %}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
        {% endif %}
    </svg>
    {% endif %}
    
    {{ text }}

{% if href %}
</a>
{% else %}
</button>
{% endif %}

<style>
@layer components {
  .btn {
    @apply inline-flex items-center justify-center font-medium rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2;
  }
  
  .btn-sm { @apply px-3 py-1.5 text-sm; }
  .btn-md { @apply px-4 py-2 text-sm; }
  .btn-lg { @apply px-6 py-3 text-base; }
  
  .btn-primary { @apply bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500; }
  .btn-secondary { @apply bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500; }
  .btn-danger { @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500; }
  .btn-success { @apply bg-green-600 text-white hover:bg-green-700 focus:ring-green-500; }
}
</style>
```

### Card Component

**templates/components/ui/card.html:**
```html
{% comment %}
Uso: {% include 'components/ui/card.html' with title="Título" %}
Parâmetros:
- title: Título do card (opcional)
- subtitle: Subtítulo (opcional)
- image: URL da imagem (opcional)
- badge: Texto do badge (opcional)
- badge_color: Cor do badge (opcional)
- footer: true|false - mostra área do footer (default: false)
{% endcomment %}

<div class="card {{ class|default:'' }}">
    {% if image %}
    <div class="aspect-w-16 aspect-h-9">
        <img src="{{ image }}" 
             alt="{{ image_alt|default:'Card image' }}" 
             class="object-cover w-full h-full rounded-t-lg">
    </div>
    {% endif %}
    
    <div class="p-6">
        {% if badge %}
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                     bg-{{ badge_color|default:'primary' }}-100 
                     text-{{ badge_color|default:'primary' }}-800 
                     dark:bg-{{ badge_color|default:'primary' }}-900 
                     dark:text-{{ badge_color|default:'primary' }}-300 mb-3">
            {{ badge }}
        </span>
        {% endif %}
        
        {% if title %}
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            {{ title }}
        </h3>
        {% endif %}
        
        {% if subtitle %}
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">{{ subtitle }}</p>
        {% endif %}
        
        <div class="text-gray-600 dark:text-gray-400">
            {{ content|default:"Card content goes here" }}
        </div>
    </div>
    
    {% if footer %}
    <div class="px-6 py-3 bg-gray-50 dark:bg-gray-700 border-t dark:border-gray-600 rounded-b-lg">
        {% block card_footer %}
        <div class="flex justify-end space-x-2">
            {% include 'components/ui/button.html' with text="Cancelar" type="secondary" size="sm" %}
            {% include 'components/ui/button.html' with text="Salvar" type="primary" size="sm" %}
        </div>
        {% endblock %}
    </div>
    {% endif %}
</div>
```

### Modal Component

**templates/components/ui/modal.html:**
```html
{% comment %}
Uso: {% include 'components/ui/modal.html' with modal_id="confirm-delete" title="Confirmar Exclusão" %}
Parâmetros:
- modal_id: ID único do modal (obrigatório)
- title: Título do modal (opcional)
- size: sm|md|lg|xl (default: md)
- closable: true|false (default: true)
{% endcomment %}

<div x-data="{ open: false }" 
     @open-modal.window="open = ($event.detail.modalId === '{{ modal_id }}')"
     @close-modal.window="open = false"
     @keydown.escape.window="open = false">
     
    <div x-show="open" 
         x-cloak
         class="fixed inset-0 z-50 overflow-y-auto">
        
        <!-- Overlay -->
        <div x-show="open" 
             x-transition:enter="ease-out duration-300"
             x-transition:enter-start="opacity-0"
             x-transition:enter-end="opacity-100"
             x-transition:leave="ease-in duration-200"
             x-transition:leave-start="opacity-100"
             x-transition:leave-end="opacity-0"
             class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
             @click="open = false"></div>
        
        <!-- Modal Container -->
        <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0">
            <div x-show="open"
                 x-transition:enter="ease-out duration-300"
                 x-transition:enter-start="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                 x-transition:enter-end="opacity-100 translate-y-0 sm:scale-100"
                 x-transition:leave="ease-in duration-200"
                 x-transition:leave-start="opacity-100 translate-y-0 sm:scale-100"
                 x-transition:leave-end="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                 class="inline-block w-full 
                        {% if size == 'sm' %}max-w-sm{% elif size == 'lg' %}max-w-2xl{% elif size == 'xl' %}max-w-4xl{% else %}max-w-md{% endif %}
                        p-6 my-8 text-left align-middle transition-all transform 
                        bg-white dark:bg-gray-800 shadow-xl rounded-lg">
                
                {% if title %}
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
                        {{ title }}
                    </h3>
                    {% if closable|default:true %}
                    <button @click="open = false" 
                            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                    {% endif %}
                </div>
                {% endif %}
                
                <div class="text-gray-600 dark:text-gray-400">
                    {{ content|default:"Modal content goes here" }}
                </div>
                
                {% if show_actions|default:true %}
                <div class="flex justify-end space-x-3 mt-6">
                    <button @click="open = false" class="btn btn-secondary">
                        {{ cancel_text|default:"Cancelar" }}
                    </button>
                    <button class="btn btn-primary" 
                            {% if confirm_action %}@click="{{ confirm_action }}; open = false"{% endif %}>
                        {{ confirm_text|default:"Confirmar" }}
                    </button>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<script>
// Funções globais para controlar modais
window.openModal = (modalId) => {
    window.dispatchEvent(new CustomEvent('open-modal', { 
        detail: { modalId: modalId } 
    }));
};

window.closeModal = () => {
    window.dispatchEvent(new CustomEvent('close-modal'));
};
</script>