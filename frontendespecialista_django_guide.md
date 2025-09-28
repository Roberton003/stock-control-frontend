---

## Otimização e Performance

### Configuração de Build para Produção

#### Webpack Config (webpack.config.js)
```javascript
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

const isDev = process.env.NODE_ENV !== 'production';

module.exports = {
    mode: isDev ? 'development' : 'production',
    entry: {
        main: './static/src/js/main.js',
        styles: './static/src/css/main.css'
    },
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: isDev ? 'js/[name].js' : 'js/[name].[contenthash].js',
        clean: true
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.css$/,
                use: [
                    isDev ? 'style-loader' : MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader'
                ]
            },
            {
                test: /\.(png|jpe?g|gif|svg|webp)$/,
                type: 'asset/resource',
                generator: {
                    filename: 'images/[name].[hash][ext]'
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name].[hash][ext]'
                }
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: isDev ? 'css/[name].css' : 'css/[name].[contenthash].css'
        })
    ],
    optimization: {
        minimize: !isDev,
        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    compress: {
                        drop_console: true
                    }
                }
            }),
            new CssMinimizerPlugin()
        ],
        splitChunks: {
            chunks: 'all',
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    chunks: 'all'
                }
            }
        }
    },
    devtool: isDev ? 'source-map' : false
};
```

### Template Tags Customizadas

#### Template Tags para Assets (templatetags/asset_tags.py)
```python
import json
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from pathlib import Path

register = template.Library()

# Load manifest for production builds
MANIFEST_FILE = Path(settings.STATIC_ROOT) / 'manifest.json'
manifest = {}

if MANIFEST_FILE.exists():
    with open(MANIFEST_FILE, 'r') as f:
        manifest = json.load(f)

@register.simple_tag
def asset(filename):
    """Get versioned asset filename"""
    if settings.DEBUG:
        return f"{settings.STATIC_URL}src/{filename}"
    
    return f"{settings.STATIC_URL}{manifest.get(filename, filename)}"

@register.simple_tag
def inline_css(filename):
    """Inline critical CSS"""
    if settings.DEBUG:
        return f'<link rel="stylesheet" href="{asset(filename)}">'
    
    try:
        with open(settings.STATIC_ROOT / manifest.get(filename, filename), 'r') as f:
            css_content = f.read()
        return mark_safe(f'<style>{css_content}</style>')
    except FileNotFoundError:
        return f'<link rel="stylesheet" href="{asset(filename)}">'

@register.inclusion_tag('components/preload_links.html')
def preload_assets(*assets):
    """Generate preload links for assets"""
    return {'assets': [asset(a) for a in assets]}
```

#### Preload Template (templates/components/preload_links.html)
```html
{% load static %}
{% for asset_url in assets %}
    {% if '.css' in asset_url %}
        <link rel="preload" href="{{ asset_url }}" as="style">
    {% elif '.js' in asset_url %}
        <link rel="preload" href="{{ asset_url }}" as="script">
    {% elif '.woff2' in asset_url %}
        <link rel="preload" href="{{ asset_url }}" as="font" type="font/woff2" crossorigin>
    {% endif %}
{% endfor %}
```

### Performance Optimizations

#### Lazy Loading Components
```html
<!-- Image lazy loading -->
<img data-src="{% static 'images/large-image.jpg' %}" 
     src="{% static 'images/placeholder.svg' %}" 
     alt="Description" 
     class="opacity-0 transition-opacity duration-300"
     loading="lazy">

<!-- Component lazy loading -->
<div x-data="{ loaded: false }" 
     x-intersect="loaded = true" 
     x-show="loaded" 
     x-transition>
    <!-- Heavy component content -->
</div>
```

#### Critical CSS Extraction
```bash
# Install critical CSS tool
npm install -D critical

# Add to package.json scripts
"critical": "critical src/index.html --base static/dist --inline --minify > templates/critical.css"
```

---

## UI Frameworks e Bibliotecas

### Bibliotecas JavaScript Recomendadas

#### Alpine.js - Interatividade Simples
```html
<!-- Toggle example -->
<div x-data="{ open: false }">
    <button @click="open = !open" class="btn btn-primary">
        Toggle Menu
    </button>
    <div x-show="open" x-transition class="menu">
        Menu content
    </div>
</div>

<!-- Form validation -->
<form x-data="{ 
    email: '', 
    errors: {},
    validate() {
        this.errors = {};
        if (!this.email) this.errors.email = 'Email é obrigatório';
        else if (!/\S+@\S+\.\S+/.test(this.email)) this.errors.email = 'Email inválido';
    }
}">
    <input type="email" 
           x-model="email" 
           @blur="validate()" 
           :class="{ 'border-red-500': errors.email }" 
           class="form-input">
    <span x-show="errors.email" x-text="errors.email" class="text-red-500 text-sm"></span>
</form>
```

#### HTMX - AJAX sem JavaScript
```html
<!-- Auto-refresh content -->
<div hx-get="/api/notifications/" 
     hx-trigger="every 30s" 
     hx-target="#notifications">
    <div id="notifications">
        <!-- Notifications will be loaded here -->
    </div>
</div>

<!-- Form submission -->
<form hx-post="/contact/" 
      hx-target="#form-result" 
      hx-swap="outerHTML">
    <input name="name" class="form-input" required>
    <input type="email" name="email" class="form-input" required>
    <button type="submit" class="btn btn-primary">Enviar</button>
    <div id="form-result"></div>
</form>

<!-- Infinite scroll -->
<div hx-get="/api/posts/?page=2" 
     hx-trigger="revealed" 
     hx-target="#posts" 
     hx-swap="beforeend">
    <div id="posts">
        <!-- Posts content -->
    </div>
    <div class="loading text-center py-4">Carregando...</div>
</div>
```

### Componentes Avançados

#### Charts com Chart.js
```javascript
// Chart component (static/src/js/components/chart.js)
class ChartComponent {
    constructor(canvas, config) {
        this.canvas = canvas;
        this.config = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        usePointStyle: true,
                        font: {
                            family: 'Inter',
                            size: 12
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: 'Inter'
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: 'Inter'
                        }
                    }
                }
            },
            ...config
        };
        
        this.init();
    }

    async init() {
        const Chart = await import('chart.js/auto');
        this.chart = new Chart.default(this.canvas, this.config);
    }

    updateData(data) {
        this.chart.data = data;
        this.chart.update();
    }

    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

// Usage in template
document.addEventListener('DOMContentLoaded', () => {
    const chartCanvas = document.querySelector('#sales-chart');
    if (chartCanvas) {
        const chart = new ChartComponent(chartCanvas, {
            type: 'line',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
                datasets: [{
                    label: 'Vendas',
                    data: [12, 19, 3, 5, 2],
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)'
                }]
            }
        });
    }
});
```

#### Date Picker Customizado
```html
<!-- Date picker component -->
<div x-data="datePicker('{{ initial_date|default:'' }}')" class="relative">
    <input type="text" 
           x-model="displayDate" 
           @click="open = true" 
           readonly 
           class="form-input cursor-pointer">
    
    <div x-show="open" 
         @click.outside="open = false" 
         x-transition 
         class="absolute top-full left-0 mt-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg p-4 z-10">
        
        <!-- Month/Year selector -->
        <div class="flex items-center justify-between mb-4">
            <button @click="prevMonth()" class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
            </button>
            
            <h3 x-text="monthYear" class="font-semibold"></h3>
            
            <button @click="nextMonth()" class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </button>
        </div>
        
        <!-- Days grid -->
        <div class="grid grid-cols-7 gap-1 text-center">
            <template x-for="day in ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']">
                <div x-text="day" class="text-xs font-semibold text-gray-500 p-2"></div>
            </template>
            
            <template x-for="date in calendarDays">
                <button @click="selectDate(date)" 
                        :class="{
                            'text-gray-400': !date.isCurrentMonth,
                            'bg-primary-600 text-white': date.isSelected,
                            'bg-primary-100 text-primary-800': date.isToday && !date.isSelected
                        }"
                        class="p-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                        x-text="date.day">
                </button>
            </template>
        </div>
    </div>
</div>

<script>
function datePicker(initialDate = '') {
    return {
        open: false,
        selectedDate: initialDate ? new Date(initialDate) : new Date(),
        viewingDate: new Date(),
        
        get displayDate() {
            return this.selectedDate.toLocaleDateString('pt-BR');
        },
        
        get monthYear() {
            return this.viewingDate.toLocaleDateString('pt-BR', { 
                month: 'long', 
                year: 'numeric' 
            });
        },
        
        get calendarDays() {
            const days = [];
            const firstDay = new Date(this.viewingDate.getFullYear(), this.viewingDate.getMonth(), 1);
            const lastDay = new Date(this.viewingDate.getFullYear(), this.viewingDate.getMonth() + 1, 0);
            const startDate = new Date(firstDay);
            startDate.setDate(startDate.getDate() - firstDay.getDay());
            
            for (let i = 0; i < 42; i++) {
                const date = new Date(startDate);
                date.setDate(startDate.getDate() + i);
                
                days.push({
                    day: date.getDate(),
                    date: new Date(date),
                    isCurrentMonth: date.getMonth() === this.viewingDate.getMonth(),
                    isToday: this.isToday(date),
                    isSelected: this.isSelected(date)
                });
            }
            
            return days;
        },
        
        selectDate(date) {
            this.selectedDate = new Date(date.date);
            this.open = false;
        },
        
        prevMonth() {
            this.viewingDate.setMonth(this.viewingDate.getMonth() - 1);
        },
        
        nextMonth() {
            this.viewingDate.setMonth(this.viewingDate.getMonth() + 1);
        },
        
        isToday(date) {
            const today = new Date();
            return date.toDateString() === today.toDateString();
        },
        
        isSelected(date) {
            return date.toDateString() === this.selectedDate.toDateString();
        }
    }
}
</script>
```

---

## Workflows de Desenvolvimento

### Scripts de Desenvolvimento (package.json)
```json
{
  "scripts": {
    "dev": "concurrently \"npm run css:watch\" \"npm run js:watch\" \"python manage.py runserver\"",
    "build": "npm run css:build && npm run js:build",
    "css:watch": "tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --watch",
    "css:build": "tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --minify",
    "js:watch": "vite build --watch",
    "js:build": "vite build",
    "lint": "eslint static/src/js/**/*.js",
    "lint:fix": "eslint static/src/js/**/*.js --fix",
    "format": "prettier --write static/src/**/*.{js,css}",
    "optimize:images": "imagemin static/src/images/**/* --out-dir=static/dist/images",
    "analyze": "webpack-bundle-analyzer static/dist/js/*.js"
  }
}
```

### Pre-commit Hooks (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
        
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.44.0
    hooks:
      - id: eslint
        files: \.js$
        args: [--fix]
        
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        files: \.(js|css|html)$
```

### Makefile para Automação
```makefile
.PHONY: help dev build clean install test lint format

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $1, $2}'

install: ## Instalar dependências
	pip install -r requirements-dev.txt
	npm install

dev: ## Iniciar desenvolvimento
	npm run dev

build: ## Build para produção
	npm run build
	python manage.py collectstatic --noinput

clean: ## Limpar arquivos gerados
	rm -rf static/dist/*
	rm -rf node_modules/.cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

test: ## Executar testes
	python manage.py test
	npm run lint

lint: ## Verificar código
	flake8 .
	npm run lint

format: ## Formatar código
	black .
	isort .
	npm run format

optimize: ## Otimizar assets
	npm run optimize:images
	python manage.py compress

deploy-staging: ## Deploy para staging
	git push staging main
	npm run build
	python manage.py migrate
	python manage.py collectstatic --noinput

deploy-prod: ## Deploy para produção
	@echo "Fazendo backup..."
	python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json
	git push origin main
	npm run build
	python manage.py migrate
	python manage.py collectstatic --noinput
	sudo systemctl reload nginx
	sudo systemctl reload gunicorn
```

---

## Deploy e Produção

### Configuração Nginx
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        
        # Enable compression for static files
        location ~* \.(css|js)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS frontend-build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY static/src ./static/src
COPY tailwind.config.js ./
COPY vite.config.js ./
RUN npm run build

FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .
COPY --from=frontend-build /app/static/dist ./static/dist

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

### Docker Compose para Desenvolvimento
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://user:password@db:5432/dbname
    depends_on:
      - db
      - redis
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"

  frontend:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - .:/app
    command: npm run dev
    ports:
      - "3000:3000"

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=dbname
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### GitHub Actions CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install Python dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Install Node dependencies
      run: npm ci
    
    - name: Run Python tests
      env:
        DATABASE_URL: postgres://postgres:postgres@localhost:5432/testdb
      run: |
        python manage.py test
        
    - name: Run JavaScript tests
      run: npm test
      
    - name: Lint code
      run: |
        flake8 .
        npm run lint
    
    - name: Build frontend
      run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/your/project
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          npm ci
          npm run build
          python manage.py migrate
          python manage.py collectstatic --noinput
          sudo systemctl reload gunicorn
          sudo systemctl reload nginx
```

---

## Troubleshooting

### Problemas Comuns e Soluções

#### TailwindCSS não está compilando
```bash
# Verificar configuração do Tailwind
npx tailwindcss init --full

# Verificar se os paths estão corretos no tailwind.config.js
# Rebuild com verbose
npx tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --watch --verbose

# Verificar se as classes estão sendo purgadas
# Adicionar safelist no config:
module.exports = {
  // ...
  safelist: [
    'bg-red-500',
    'text-blue-600',
    // Add classes that might be purged incorrectly
  ]
}
```

#### Problemas com Assets em Produção
```python
# settings.py - Verificar configuração de static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Verificar se collectstatic está funcionando
python manage.py collectstatic --dry-run

# Debug de static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

#### JavaScript não está carregando
```html
<!-- Verificar ordem de carregamento -->
<script defer src="{% static 'dist/js/main.js' %}"></script>

<!-- Debug no navegador -->
<script>
console.log('JavaScript loaded');
if (typeof Alpine !== 'undefined') {
    console.log('Alpine.js loaded');
}
</script>
```

#### Problemas de CORS
```python
# settings.py
CORS_ALLOW_ALL_ORIGINS = True  # Apenas para desenvolvimento
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "http://localhost:3000",
]
```

#### Dark Mode não funciona
```javascript
// Verificar se a classe está sendo aplicada
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dark mode class:', document.documentElement.classList.contains('dark'));
    
    // Forçar aplicação
    if (localStorage.getItem('dark-mode') === 'true') {
        document.documentElement.classList.add('dark');
    }
});
```

---

## Recursos e Templates

### Templates de Exemplo

#### Dashboard Layout
```html
{% extends 'base/base.html' %}
{% load static %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform -translate-x-full transition-transform duration-300 ease-in-out lg:translate-x-0" x-data="{ open: false }" :class="{ 'translate-x-0': open }">
        <!-- Sidebar content -->
        <div class="flex items-center justify-center h-16 border-b dark:border-gray-700">
            <h1 class="text-xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
        </div>
        
        <nav class="mt-8">
            <a href="#" class="flex items-center px-6 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
                </svg>
                Dashboard
            </a>
            <!-- More nav items -->
        </nav>
    </div>
    
    <!-- Main content -->
    <div class="lg:ml-64">
        <!-- Top bar -->
        <div class="flex items-center justify-between h-16 bg-white dark:bg-gray-800 shadow-sm px-6">
            <button @click="open = !open" class="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
            </button>
            
            <div class="flex items-center space-x-4">
                <button class="p-2 text-gray-400 hover:text-gray-500">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM15 17V7a3 3 0 00-3-3H5a3 3 0 00-3 3v10a3 3 0 003 3h7z"></path>
                    </svg>
                </button>
            </div>
        </div>
        
        <!-- Page content -->
        <div class="p-6">
            <!-- Stats cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {% for stat in stats %}
                <div class="card">
                    <div class="p-6">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <div class="w-8 h-8 bg-primary-500 rounded-md flex items-center justify-center">
                                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                                        {{ stat.icon|safe }}
                                    </svg>
                                </div>
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">{{ stat.title }}</dt>
                                    <dd class="text-2xl font-bold text-gray-900 dark:text-white">{{ stat.value }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Charts and tables -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="card">
                    <div class="p-6">
                        <h3 class="text-lg font-semibold mb-4">Vendas por Mês</h3>
                        <canvas id="sales-chart" width="400" height="200"></canvas>
                    </div>
                </div>
                
                <div class="card">
                    <div class="p-6">
                        <h3 class="text-lg font-semibold mb-4">Atividade Recente</h3>
                        <div class="space-y-3">
                            {% for activity in recent_activities %}
                            <div class="flex items-center space-x-3">
                                <div class="flex-shrink-0 w-2 h-2 bg-primary-500 rounded-full"></div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm text-gray-900 dark:text-white">{{ activity.description }}</p>
                                    <p class="text-xs text-gray-500 dark:text-gray-400">{{ activity.created_at|timesince }} atrás</p>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Bibliotecas CSS Úteis

#### Animate.css Integration
```css
/* Custom animations with Tailwind */
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');

.animate-fade-in-up {
    animation: fadeInUp 0.5s ease-out;
}

.animate-bounce-in {
    animation: bounceIn 0.6s ease-out;
}

/* Custom keyframes */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 40px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}
```

#### Loading States
```html
<!-- Skeleton loader -->
<div class="animate-pulse">
    <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4 mb-2"></div>
    <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-1/2 mb-2"></div>
    <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-5/6"></div>
</div>

<!-- Spinner -->
<div class="flex justify-center">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
</div>
```

### Comandos de Deploy Rápido

```bash
#!/bin/bash
# deploy.sh
set -e

echo "🚀 Starting deployment..."

# Frontend build
echo "📦 Building frontend assets..."
npm run build

# Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Restart services
echo "🔄 Restarting services..."
sudo systemctl reload gunicorn
sudo systemctl reload nginx

echo "✅ Deployment completed successfully!"
```

---

**Última atualização**: Setembro 2025  
**Versão**: 1.0  
**Compatibilidade**: Django 4.2+, TailwindCSS 3.4+, Node.js 18+

Este guia fornece uma base sólida para desenvolvimento frontend moderno em aplicações Django, combinando as melhores práticas com ferramentas atuais do mercado.# Guia Frontend Django - TailwindCSS e Tecnologias Modernas

Manual especializado para desenvolvimento frontend em aplicações Django usando as melhores práticas e ferramentas modernas.

## Índice

1. [Stack Frontend Recomendada](#stack-frontend-recomendada)
2. [Configuração do TailwindCSS](#configuração-do-tailwindcss)
3. [Estrutura de Assets](#estrutura-de-assets)
4. [Templates Django Modernos](#templates-django-modernos)
5. [Componentes Reutilizáveis](#componentes-reutilizáveis)
6. [JavaScript Moderno](#javascript-moderno)
7. [Otimização e Performance](#otimização-e-performance)
8. [UI Frameworks e Bibliotecas](#ui-frameworks-e-bibliotecas)
9. [Workflows de Desenvolvimento](#workflows-de-desenvolvimento)
10. [Deploy e Produção](#deploy-e-produção)
11. [Troubleshooting](#troubleshooting)
12. [Recursos e Templates](#recursos-e-templates)

---

## Stack Frontend Recomendada

### Tecnologias Principais
```yaml
CSS Framework: TailwindCSS v3.4+
Build Tool: Vite.js ou Webpack
JavaScript: ES6+ com TypeScript (opcional)
Icons: Heroicons, Lucide, Tabler Icons
Fonts: Inter, Poppins, JetBrains Mono
Animations: Framer Motion, GSAP, ou CSS puro
Charts: Chart.js, ApexCharts, D3.js
Maps: Leaflet, Mapbox
```

### Estrutura de Pastas Recomendada
```
projeto/
├── static/
│   ├── src/
│   │   ├── css/
│   │   │   ├── main.css           # Arquivo principal do Tailwind
│   │   │   ├── components.css     # Componentes customizados
│   │   │   └── utilities.css      # Utilities customizadas
│   │   ├── js/
│   │   │   ├── main.js           # JavaScript principal
│   │   │   ├── components/       # Componentes JS
│   │   │   ├── utils/            # Utilities
│   │   │   └── vendor/           # Bibliotecas externas
│   │   └── images/
│   ├── dist/                     # Assets compilados
│   └── fonts/
├── templates/
│   ├── base/
│   │   ├── base.html
│   │   ├── head.html
│   │   ├── navbar.html
│   │   └── footer.html
│   ├── components/               # Template components
│   └── pages/                    # Page templates
└── node_modules/
```

---

## Configuração do TailwindCSS

### Instalação e Setup Inicial

#### 1. Instalar dependências Node.js
```bash
# Inicializar projeto Node.js
npm init -y

# Instalar TailwindCSS e dependências
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npm install -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio
npm install -D vite sass

# Criar configuração do Tailwind
npx tailwindcss init -p
```

#### 2. Configurar tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/src/**/*.js',
    './apps/**/templates/**/*.html',
    './apps/**/static/**/*.js',
  ],
  darkMode: 'class', // ou 'media'
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
        },
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          900: '#111827',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

#### 3. Configurar CSS principal (static/src/css/main.css)
```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Fontes personalizadas */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Componentes customizados */
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
  }
  
  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
  }
  
  .btn-secondary {
    @apply bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600;
  }
  
  .card {
    @apply bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700;
  }
  
  .form-input {
    @apply block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white;
  }
  
  .form-label {
    @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1;
  }
}

/* Utilities customizadas */
@layer utilities {
  .text-shadow {
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .gradient-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}

/* Animações personalizadas */
.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

.slide-up {
  animation: slideUp 0.3s ease-out;
}

/* Dark mode improvements */
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
  }
}
```

#### 4. Configurar Vite (vite.config.js)
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
      },
      output: {
        assetFileNames: 'css/[name].[hash].css',
        chunkFileNames: 'js/[name].[hash].js',
        entryFileNames: 'js/[name].[hash].js',
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

---

## Estrutura de Assets

### Package.json Scripts
```json
{
  "name": "django-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "watch": "vite build --watch",
    "preview": "vite preview",
    "tailwind:watch": "tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --watch",
    "tailwind:build": "tailwindcss -i ./static/src/css/main.css -o ./static/dist/css/main.css --minify"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0",
    "@tailwindcss/aspect-ratio": "^0.4.0"
  },
  "dependencies": {
    "alpinejs": "^3.13.0",
    "htmx.org": "^1.9.0"
  }
}
```

### Configuração do Django (settings.py)
```python
# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static/dist',  # Assets compilados
    BASE_DIR / 'static/src',   # Assets de desenvolvimento
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Compressor para produção (opcional)
if not DEBUG:
    INSTALLED_APPS += ['compressor']
    STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']
    
    COMPRESS_ENABLED = True
    COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
    COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
```

---

## Templates Django Modernos

### Template Base (templates/base/base.html)
```html
{% load static %}
<!DOCTYPE html>
<html lang="pt-BR" class="{% if dark_mode %}dark{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{% block description %}{% endblock %}">
    
    <title>{% block title %}{% endblock %} | Meu Site</title>
    
    <!-- Preload critical fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- CSS -->
    <link href="{% static 'dist/css/main.css' %}" rel="stylesheet">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="{% static 'images/favicon.svg' %}">
    
    <!-- Meta tags adicionais -->
    {% block meta %}{% endblock %}
    
    <!-- Alpine.js (para interatividade simples) -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.0/dist/cdn.min.js"></script>
    
    <!-- HTMX (para interações AJAX) -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 antialiased">
    <!-- Skip to content (acessibilidade) -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary-600 text-white px-4 py-2 rounded-lg">
        Pular para o conteúdo
    </a>
    
    <!-- Navigation -->
    {% include 'base/navbar.html' %}
    
    <!-- Flash Messages -->
    {% if messages %}
        <div id="messages-container" class="fixed top-4 right-4 z-50 space-y-2">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} animate-fade-in" x-data="{ show: true }" x-show="show" x-transition>
                    <div class="flex items-center justify-between">
                        <span>{{ message }}</span>
                        <button @click="show = false" class="ml-4 text-sm hover:opacity-75">×</button>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% endif %}
    
    <!-- Main Content -->
    <main id="main-content" class="min-h-screen">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    {% include 'base/footer.html' %}
    
    <!-- JavaScript -->
    <script src="{% static 'dist/js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
    
    <!-- Dark mode toggle script -->
    <script>
        // Dark mode persistence
        if (localStorage.getItem('dark-mode') === 'true' || (!localStorage.getItem('dark-mode') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        }
        
        function toggleDarkMode() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('dark-mode', isDark);
        }
    </script>
</body>
</html>
```

### Navbar Moderna (templates/base/navbar.html)
```html
<nav class="bg-white dark:bg-gray-800 shadow-lg sticky top-0 z-40" x-data="{ mobileOpen: false }">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
                <a href="{% url 'home' %}" class="text-2xl font-bold text-primary-600 dark:text-primary-400">
                    Logo
                </a>
            </div>
            
            <!-- Desktop Navigation -->
            <div class="hidden md:block">
                <div class="ml-10 flex items-baseline space-x-4">
                    <a href="{% url 'home' %}" class="nav-link">Home</a>
                    <a href="{% url 'about' %}" class="nav-link">Sobre</a>
                    <a href="{% url 'contact' %}" class="nav-link">Contato</a>
                </div>
            </div>
            
            <!-- User Menu & Actions -->
            <div class="hidden md:flex items-center space-x-4">
                <!-- Dark Mode Toggle -->
                <button onclick="toggleDarkMode()" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg class="w-5 h-5 dark:hidden" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                    </svg>
                    <svg class="w-5 h-5 hidden dark:block" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
                    </svg>
                </button>
                
                {% if user.is_authenticated %}
                    <!-- User dropdown -->
                    <div class="relative" x-data="{ open: false }">
                        <button @click="open = !open" class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                            <img class="w-8 h-8 rounded-full" src="{{ user.profile.avatar.url|default:'/static/images/default-avatar.svg' }}" alt="{{ user.get_full_name }}">
                            <span class="text-sm font-medium">{{ user.first_name|default:user.username }}</span>
                        </button>
                        
                        <div x-show="open" @click.outside="open = false" x-transition class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg py-2">
                            <a href="{% url 'profile' %}" class="dropdown-link">Perfil</a>
                            <a href="{% url 'settings' %}" class="dropdown-link">Configurações</a>
                            <hr class="my-2 border-gray-200 dark:border-gray-700">
                            <a href="{% url 'logout' %}" class="dropdown-link text-red-600 dark:text-red-400">Sair</a>
                        </div>
                    </div>
                {% else %}
                    <a href="{% url 'login' %}" class="btn btn-secondary">Entrar</a>
                    <a href="{% url 'signup' %}" class="btn btn-primary">Cadastrar</a>
                {% endif %}
            </div>
            
            <!-- Mobile menu button -->
            <div class="md:hidden">
                <button @click="mobileOpen = !mobileOpen" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>
        </div>
    </div>
    
    <!-- Mobile menu -->
    <div x-show="mobileOpen" x-transition class="md:hidden bg-white dark:bg-gray-800 border-t dark:border-gray-700">
        <div class="px-2 pt-2 pb-3 space-y-1">
            <a href="{% url 'home' %}" class="mobile-nav-link">Home</a>
            <a href="{% url 'about' %}" class="mobile-nav-link">Sobre</a>
            <a href="{% url 'contact' %}" class="mobile-nav-link">Contato</a>
        </div>
        
        {% if user.is_authenticated %}
            <div class="px-4 py-3 border-t dark:border-gray-700">
                <div class="flex items-center space-x-3">
                    <img class="w-10 h-10 rounded-full" src="{{ user.profile.avatar.url|default:'/static/images/default-avatar.svg' }}" alt="{{ user.get_full_name }}">
                    <div>
                        <div class="text-sm font-medium">{{ user.get_full_name }}</div>
                        <div class="text-xs text-gray-500 dark:text-gray-400">{{ user.email }}</div>
                    </div>
                </div>
                <div class="mt-3 space-y-1">
                    <a href="{% url 'profile' %}" class="mobile-nav-link">Perfil</a>
                    <a href="{% url 'logout' %}" class="mobile-nav-link text-red-600 dark:text-red-400">Sair</a>
                </div>
            </div>
        {% endif %}
    </div>
</nav>

<style>
    .nav-link {
        @apply px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200;
    }
    
    .mobile-nav-link {
        @apply block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700;
    }
    
    .dropdown-link {
        @apply block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700;
    }
</style>
```

---

## Componentes Reutilizáveis

### Sistema de Componentes (templates/components/)

#### Modal Component (templates/components/modal.html)
```html
<div x-data="{ open: {{ open|default:'false' }} }" x-show="open" class="fixed inset-0 z-50 overflow-y-auto" x-cloak>
    <!-- Overlay -->
    <div x-show="open" x-transition:enter="ease-out duration-300" x-transition:enter-start="opacity-0" x-transition:enter-end="opacity-100" x-transition:leave="ease-in duration-200" x-transition:leave-start="opacity-100" x-transition:leave-end="opacity-0" class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="open = false"></div>
    
    <!-- Modal -->
    <div x-show="open" x-transition:enter="ease-out duration-300" x-transition:enter-start="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" x-transition:enter-end="opacity-100 translate-y-0 sm:scale-100" x-transition:leave="ease-in duration-200" x-transition:leave-start="opacity-100 translate-y-0 sm:scale-100" x-transition:leave-end="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" class="flex items-center justify-center min-h-screen px-4">
        <div class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-auto">
            <!-- Header -->
            {% if title %}
            <div class="flex items-center justify-between p-6 border-b dark:border-gray-700">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ title }}</h3>
                <button @click="open = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            {% endif %}
            
            <!-- Content -->
            <div class="p-6">
                {{ content|default:"Modal content goes here" }}
            </div>
            
            <!-- Footer -->
            {% if show_footer %}
            <div class="flex justify-end space-x-3 p-6 border-t dark:border-gray-700">
                <button @click="open = false" class="btn btn-secondary">Cancelar</button>
                <button class="btn btn-primary">Confirmar</button>
            </div>
            {% endif %}
        </div>
    </div>
</div>
```

#### Card Component (templates/components/card.html)
```html
<div class="card {{ class|default:'' }}">
    {% if image %}
    <div class="aspect-w-16 aspect-h-9">
        <img src="{{ image }}" alt="{{ image_alt|default:'Card image' }}" class="object-cover w-full h-full rounded-t-lg">
    </div>
    {% endif %}
    
    <div class="p-6">
        {% if badge %}
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-300 mb-3">
            {{ badge }}
        </span>
        {% endif %}
        
        {% if title %}
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">{{ title }}</h3>
        {% endif %}
        
        {% if description %}
        <p class="text-gray-600 dark:text-gray-400 mb-4">{{ description }}</p>
        {% endif %}
        
        {{ content }}
        
        {% if button_text %}
        <div class="mt-4">
            <a href="{{ button_url|default:'#' }}" class="btn btn-primary">{{ button_text }}</a>
        </div>
        {% endif %}
    </div>
</div>
```

#### Form Field Component (templates/components/form_field.html)
```html
<div class="mb-4">
    {% if field.label %}
    <label for="{{ field.id_for_label }}" class="form-label">
        {{ field.label }}
        {% if field.field.required %}<span class="text-red-500 ml-1">*</span>{% endif %}
    </label>
    {% endif %}
    
    {% if field.help_text %}
    <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">{{ field.help_text }}</p>
    {% endif %}
    
    {{ field|add_class:"form-input" }}
    
    {% if field.errors %}
    <div class="mt-1">
        {% for error in field.errors %}
        <p class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
        {% endfor %}
    </div>
    {% endif %}
</div>
```

---

## JavaScript Moderno

### JavaScript Principal (static/src/js/main.js)
```javascript
// Utils
const utils = {
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

    // Format currency
    formatCurrency(amount, currency = 'BRL') {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },

    // Copy to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Copiado para a área de transferência!', 'success');
            return true;
        } catch (err) {
            console.error('Failed to copy: ', err);
            return false;
        }
    },

    // Show toast notification
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;
        
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-black',
            info: 'bg-blue-500 text-white'
        };
        
        toast.className += ` ${colors[type] || colors.info}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.remove('translate-x-full'), 100);
        
        // Animate out and remove
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
};

// Form handling
class FormHandler {
    constructor(form, options = {}) {
        this.form = form;
        this.options = {
            showLoading: true,
            resetOnSuccess: false,
            validateOnBlur: true,
            ...options
        };
        this.init();
    }

    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        
        if (this.options.validateOnBlur) {
            this.form.querySelectorAll('input, textarea, select').forEach(field => {
                field.addEventListener('blur', this.validateField.bind(this, field));
            });
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (this.options.showLoading) {
            this.setLoading(true);
        }
        
        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.form.action, {
                method: this.form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.handleSuccess(data);
            } else {
                this.handleError(data);
            }
        } catch (error) {
            console.error('Form submission error:', error);
            utils.showToast('Erro ao enviar formulário', 'error');
        } finally {
            if (this.options.showLoading) {
                this.setLoading(false);
            }
        }
    }

    validateField(field) {
        // Remove previous error styles
        field.classList.remove('border-red-500');
        
        // Basic validation
        if (field.required && !field.value.trim()) {
            this.showFieldError(field, 'Este campo é obrigatório');
            return false;
        }
        
        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                this.showFieldError(field, 'Email inválido');
                return false;
            }
        }
        
        this.clearFieldError(field);
        return true;
    }

    showFieldError(field, message) {
        field.classList.add('border-red-500');
        
        let errorEl = field.parentNode.querySelector('.field-error');
        if (!errorEl) {
            errorEl = document.createElement('div');
            errorEl.className = 'field-error text-sm text-red-600 mt-1';
            field.parentNode.appendChild(errorEl);
        }
        errorEl.textContent = message;
    }

    clearFieldError(field) {
        field.classList.remove('border-red-500');
        const errorEl = field.parentNode.querySelector('.field-error');
        if (errorEl) {
            errorEl.remove();
        }
    }

    handleSuccess(data) {
        utils.showToast(data.message || 'Sucesso!', 'success');
        
        if (this.options.resetOnSuccess) {
            this.form.reset();
        }
        
        if (data.redirect) {
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1500);
        }
    }

    handleError(data) {
        if (data.errors) {
            Object.keys(data.errors).forEach(fieldName => {
                const field = this.form.querySelector(`[name="${fieldName}"]`);
                if (field) {
                    this.showFieldError(field, data.errors[fieldName][0]);
                }
            });
        }
        
        utils.showToast(data.message || 'Erro ao processar formulário', 'error');
    }

    setLoading(loading) {
        const submitBtn = this.form.querySelector('[type="submit"]');
        if (submitBtn) {
            if (loading) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>Enviando...';
            } else {
                submitBtn.disabled = false;
                submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Enviar';
            }
        }
    }
}

// Modal management
class ModalManager {
    static openModal(modalId) {
        const event = new CustomEvent('open-modal', { detail: { modalId } });
        document.dispatchEvent(event);
    }

    static closeModal(modalId) {
        const event = new CustomEvent('close-modal', { detail: { modalId } });
        document.dispatchEvent(event);
    }
}

// Image lazy loading
class LazyLoader {
    constructor() {
        this.images = document.querySelectorAll('img[data-src]');
        this.imageObserver = new IntersectionObserver(this.onIntersection.bind(this));
        this.init();
    }

    init() {
        this.images.forEach(img => this.imageObserver.observe(img));
    }

    onIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadImage(entry.target);
                this.imageObserver.unobserve(entry.target);
            }
        });
    }

    loadImage(img) {
        img.src = img.dataset.src;
        img.classList.remove('opacity-0');
        img.classList.add('fade-in');
    }
}

// Infinite scroll
class InfiniteScroll {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            threshold: 200,
            loadingSelector: '.loading',
            ...options
        };
        this.loading = false;
        this.init();
    }

    init() {
        window.addEventListener('scroll', utils.debounce(this.onScroll.bind(this), 100));
    }

    onScroll() {
        if (this.loading) return;

        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        
        if (scrollTop + clientHeight >= scrollHeight - this.options.threshold) {
            this.loadMore();
        }
    }

    async loadMore() {
        if (this.loading) return;
        
        this.loading = true;
        this.showLoading();
        
        try {
            const nextPage = this.getNextPage();
            if (!nextPage) return;
            
            const response = await fetch(nextPage);
            const html = await response.text();
            
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newItems = doc.querySelectorAll('.item');
            
            newItems.forEach(item => {
                this.container.appendChild(item);
            });
            
            this.updateNextPage(doc);
            
        } catch (error) {
            console.error('Error loading more items:', error);
            utils.showToast('Erro ao carregar mais itens', 'error');
        } finally {
            this.loading = false;
            this.hideLoading();
        }
    }

    getNextPage() {
        const nextLink = document.querySelector('[data-next-page]');
        return nextLink ? nextLink.dataset.nextPage : null;
    }

    updateNextPage(doc) {
        const currentNext = document.querySelector('[data-next-page]');
        const newNext = doc.querySelector('[data-next-page]');
        
        if (currentNext) {
            if (newNext) {
                currentNext.dataset.nextPage = newNext.dataset.nextPage;
            } else {
                currentNext.remove();
            }
        }
    }

    showLoading() {
        const loader = document.querySelector(this.options.loadingSelector);
        if (loader) loader.classList.remove('hidden');
    }

    hideLoading() {
        const loader = document.querySelector(this.options.loadingSelector);
        if (loader) loader.classList.add('hidden');
    }
}

// Search functionality
class SearchHandler {
    constructor(input, resultsContainer, options = {}) {
        this.input = input;
        this.resultsContainer = resultsContainer;
        this.options = {
            minLength: 2,
            delay: 300,
            endpoint: '/search/',
            ...options
        };
        this.init();
    }

    init() {
        this.input.addEventListener('input', utils.debounce(this.search.bind(this), this.options.delay));
        this.input.addEventListener('focus', this.showResults.bind(this));
        document.addEventListener('click', this.hideResults.bind(this));
    }

    async search() {
        const query = this.input.value.trim();
        
        if (query.length < this.options.minLength) {
            this.hideResults();
            return;
        }

        try {
            const response = await fetch(`${this.options.endpoint}?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            this.displayResults(data.results);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    displayResults(results) {
        this.resultsContainer.innerHTML = '';
        
        if (results.length === 0) {
            this.resultsContainer.innerHTML = '<div class="p-4 text-gray-500">Nenhum resultado encontrado</div>';
        } else {
            results.forEach(result => {
                const item = this.createResultItem(result);
                this.resultsContainer.appendChild(item);
            });
        }
        
        this.showResults();
    }

    createResultItem(result) {
        const item = document.createElement('div');
        item.className = 'p-4 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer border-b dark:border-gray-600 last:border-b-0';
        item.innerHTML = `
            <div class="font-medium text-gray-900 dark:text-gray-100">${result.title}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">${result.description}</div>
        `;
        
        item.addEventListener('click', () => {
            window.location.href = result.url;
        });
        
        return item;
    }

    showResults() {
        this.resultsContainer.classList.remove('hidden');
    }

    hideResults(e) {
        if (e && (this.input.contains(e.target) || this.resultsContainer.contains(e.target))) {
            return;
        }
        this.resultsContainer.classList.add('hidden');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize forms
    document.querySelectorAll('form[data-ajax]').forEach(form => {
        new FormHandler(form, {
            resetOnSuccess: form.hasAttribute('data-reset-on-success'),
            validateOnBlur: !form.hasAttribute('data-no-validation')
        });
    });

    // Initialize lazy loading
    if ('IntersectionObserver' in window) {
        new LazyLoader();
    }

    // Initialize infinite scroll
    const infiniteContainer = document.querySelector('[data-infinite-scroll]');
    if (infiniteContainer) {
        new InfiniteScroll(infiniteContainer);
    }

    // Initialize search
    const searchInput = document.querySelector('[data-search]');
    const searchResults = document.querySelector('[data-search-results]');
    if (searchInput && searchResults) {
        new SearchHandler(searchInput, searchResults);
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-resize textareas
    document.querySelectorAll('textarea[data-auto-resize]').forEach(textarea => {
        const resize = () => {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        };
        
        textarea.addEventListener('input', resize);
        resize(); // Initial resize
    });

    // Copy to clipboard buttons
    document.querySelectorAll('[data-copy]').forEach(btn => {
        btn.addEventListener('click', async () => {
            const text = btn.dataset.copy || btn.textContent;
            const success = await utils.copyToClipboard(text);
            
            if (success) {
                const originalText = btn.textContent;
                btn.textContent = 'Copiado!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            }
        });
    });
});

// Export for use in other scripts
window.AppUtils = utils;
window.FormHandler = FormHandler;
window.ModalManager = ModalManager;