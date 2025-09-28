# 💻 Frontend Setup - Configuração Inicial (frontend_setup.md)

## 🎯 Objetivo

Este documento fornece as instruções básicas para configurar o ambiente frontend em projetos Django com TailwindCSS, Vite e Alpine.js.

## 📋 Stack Tecnológica

```yaml
css_framework: TailwindCSS v3.4+
build_tool: Vite.js v5.0+
javascript: Alpine.js v3.13+ (interatividade simples)
ajax: HTMX v1.9+ (atualizações dinâmicas)
icons: Heroicons, Lucide Icons
fonts: Inter (padrão), JetBrains Mono (código)
```

## 🏗️ Estrutura de Arquivos

```
projeto/
├── static/
│   ├── src/                    # Arquivos fonte (desenvolvimento)
│   │   ├── css/
│   │   │   ├── main.css        # Entrada principal do Tailwind
│   │   │   └── components.css  # Componentes customizados
│   │   ├── js/
│   │   │   ├── main.js         # JavaScript principal
│   │   │   └── components/     # Componentes JS modulares
│   │   └── images/
│   ├── dist/                   # Arquivos compilados (produção)
│   │   ├── css/
│   │   └── js/
│   └── fonts/
├── templates/
│   ├── base/
│   │   ├── base.html          # Template principal
│   │   ├── navbar.html        # Navegação
│   │   └── footer.html        # Rodapé
│   ├── components/            # Componentes reutilizáveis
│   └── pages/                 # Templates de páginas
├── package.json
├── tailwind.config.js
├── vite.config.js
└── postcss.config.js
```

## ⚙️ Configuração Passo a Passo

### 1. Inicializar Projeto Node.js

```bash
# Criar package.json
cd [diretorio_do_projeto]
npm init -y
```

### 2. Instalar Dependências

```bash
# Dependências de desenvolvimento
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npm install -D @tailwindcss/forms @tailwindcss/typography
npm install -D vite@latest

# Dependências de produção (CDN também disponível)
npm install alpinejs htmx.org
```

### 3. Configurar TailwindCSS

```bash
# Gerar arquivos de configuração
npx tailwindcss init -p
```

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/src/**/*.js',
    './apps/**/templates/**/*.html',
    './apps/**/static/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### 4. Configurar Vite

**vite.config.js:**
```javascript
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: './static/src',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'static/src/css/main.css'),
        js: resolve(__dirname, 'static/src/js/main.js'),
      }
    }
  },
  css: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ]
    }
  }
});
```

### 5. CSS Principal

**static/src/css/main.css:**
```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Fontes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Componentes básicos */
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
  }
  
  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700;
  }
  
  .btn-secondary {
    @apply bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200;
  }
  
  .card {
    @apply bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700;
  }
  
  .form-input {
    @apply block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500;
  }
  
  .form-label {
    @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1;
  }
}
```

### 6. JavaScript Principal

**static/src/js/main.js:**
```javascript
// Importar Alpine.js
import Alpine from 'alpinejs';

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
  }
};

// Inicializar Alpine
window.Alpine = Alpine;
Alpine.start();

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
  console.log('Frontend inicializado');
});
```

### 7. Scripts NPM

**package.json (scripts):**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "watch": "vite build --watch",
    "tailwind:watch": "tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --watch",
    "tailwind:build": "tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --minify"
  }
}
```

### 8. Template Base

**templates/base/base.html:**
```html
{% load static %}
<!DOCTYPE html>
<html lang="pt-BR" class="{% if request.user.profile.dark_mode %}dark{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} | Meu Site</title>
    
    <!-- CSS -->
    <link href="{% static 'dist/css/main.css' %}" rel="stylesheet">
    
    <!-- JavaScript Libs via CDN (desenvolvimento) -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.0/dist/cdn.min.js"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    
    <!-- Navigation -->
    {% include 'base/navbar.html' %}
    
    <!-- Main Content -->
    <main id="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    {% include 'base/footer.html' %}
    
    <!-- JavaScript -->
    <script src="{% static 'dist/js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 🔧 Configuração Django

### Settings.py
```python
# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static/dist',  # Arquivos compilados (produção)
    BASE_DIR / 'static/src',   # Arquivos fonte (desenvolvimento)
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## 🚀 Comandos de Desenvolvimento

```bash
# Desenvolvimento (watch mode)
npm run dev

# Build para produção
npm run build

# Watch do Tailwind apenas
npm run tailwind:watch

# Build do Tailwind para produção
npm run tailwind:build
```

## ✅ Verificação da Instalação

### Checklist de Funcionamento
- [ ] `npm run dev` inicia sem erros
- [ ] `npm run build` gera arquivos em `static/dist/`
- [ ] Template base carrega sem erros 404
- [ ] Classes Tailwind aparecem corretamente
- [ ] Alpine.js funciona (testar com `x-data`)
- [ ] Dark mode alterna corretamente

### Teste Rápido
Criar um template simples para testar:

**templates/test.html:**
```html
{% extends 'base/base.html' %}

{% block content %}
<div class="container mx-auto p-8" x-data="{ count: 0 }">
    <h1 class="text-3xl font-bold text-primary-600 mb-4">Teste Frontend</h1>
    
    <div class="card p-6 max-w-md">
        <p class="mb-4">Contador: <span x-text="count" class="font-bold"></span></p>
        <button @click="count++" class="btn btn-primary">Incrementar</button>
    </div>
</div>
{% endblock %}
```

## 🔗 Próximos Passos

Após a configuração inicial:
1. Consultar `frontend_components.md` para componentes reutilizáveis
2. Ver `frontend_advanced.md` para recursos avançados
3. Implementar componentes específicos do projeto

## ⚠️ Notas Importantes

- **Ambiente de Desenvolvimento**: Use CDN para libs JavaScript
- **Produção**: Considere bundling das dependências
- **Performance**: Sempre minificar CSS/JS para produção
- **SEO**: Manter HTML semântico mesmo com Tailwind