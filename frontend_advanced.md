## ⚡ Performance e Otimização

### Lazy Loading de Componentes

**static/src/js/lazy-loader.js:**
```javascript
class ComponentLoader {
    constructor() {
        this.loadedComponents = new Set();
        this.observer = new IntersectionObserver(this.handleIntersection.bind(this), {
            threshold: 0.1,
            rootMargin: '50px'
        });
        this.init();
    }

    init() {
        // Observar elementos com atributo data-lazy-component
        document.querySelectorAll('[data-lazy-component]').forEach(el => {
            this.observer.observe(el);
        });
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadComponent(entry.target);
                this.observer.unobserve(entry.target);
            }
        });
    }

    async loadComponent(element) {
        const componentName = element.dataset.lazyComponent;
        
        if (this.loadedComponents.has(componentName)) return;
        
        try {
            // Mostrar skeleton loader
            element.innerHTML = this.getSkeletonLoader();
            
            // Carregar dados do componente
            const response = await fetch(`/api/components/${componentName}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            const html = await response.text();
            element.innerHTML = html;
            
            // Marcar como carregado
            this.loadedComponents.add(componentName);
            
            // Disparar evento customizado
            element.dispatchEvent(new CustomEvent('component-loaded', {
                detail: { componentName }
            }));
            
        } catch (error) {
            console.error(`Erro ao carregar componente ${componentName}:`, error);
            element.innerHTML = '<p class="text-red-500">Erro ao carregar componente</p>';
        }
    }

    getSkeletonLoader() {
        return `
            <div class="animate-pulse space-y-3">
                <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4"></div>
                <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-1/2"></div>
                <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-5/6"></div>
            </div>
        `;
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ComponentLoader();
});
```

### Image Optimization

**templates/components/ui/image.html:**
```html
{% comment %}
Componente de imagem otimizada com lazy loading
Uso: {% include 'components/ui/image.html' with src="/path/image.jpg" alt="Description" %}
{% endcomment %}

<div class="image-container {{ container_class|default:'' }}" 
     x-data="{ loaded: false, error: false }">
     
    <!-- Placeholder/Skeleton -->
    <div x-show="!loaded && !error" 
         class="animate-pulse bg-gray-300 dark:bg-gray-600 {{ placeholder_class|default:'h-48 w-full' }} rounded"></div>
    
    <!-- Imagem principal -->
    <img class="{{ class|default:'w-full h-auto' }} transition-opacity duration-300"
         :class="{ 'opacity-0': !loaded, 'opacity-100': loaded }"
         data-src="{{ src }}"
         alt="{{ alt }}"
         loading="lazy"
         @load="loaded = true"
         @error="error = true"
         {% if sizes %}sizes="{{ sizes }}"{% endif %}
         {% if srcset %}srcset="{{ srcset }}"{% endif %}>
    
    <!-- Fallback para erro -->
    <div x-show="error" 
         class="flex items-center justify-center bg-gray-100 dark:bg-gray-700 {{ placeholder_class|default:'h-48 w-full' }} rounded">
        <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
    </div>
</div>

<script>
// Implementar lazy loading para imagens
document.addEventListener('DOMContentLoaded', function() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});
</script>
```

### Bundle Optimization

**vite.config.js (versão otimizada):**
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
        app: resolve(__dirname, 'static/src/js/main.js'),
      },
      output: {
        manualChunks: {
          vendor: ['alpinejs'],
          utils: ['./static/src/js/utils.js']
        }
      }
    },
    // Otimizações
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  css: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
        require('cssnano')({ preset: 'default' })
      ]
    }
  },
  // Code splitting
  plugins: []
});
```

## 📱 Progressive Web App (PWA)

### Service Worker

**static/src/js/service-worker.js:**
```javascript
const CACHE_NAME = 'django-app-v1';
const STATIC_ASSETS = [
    '/',
    '/static/dist/css/main.css',
    '/static/dist/js/main.js',
    '/static/images/logo.svg',
    '/offline/',
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
    );
});

// Activate event
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - Network First com Cache Fallback
self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;
    
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Se a resposta for válida, armazenar no cache
                if (response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => cache.put(event.request, responseClone));
                }
                return response;
            })
            .catch(() => {
                // Se falhar, tentar buscar no cache
                return caches.match(event.request)
                    .then(response => {
                        return response || caches.match('/offline/');
                    });
            })
    );
});
```

### Web App Manifest

**static/manifest.json:**
```json
{
  "name": "Django App",
  "short_name": "DjangoApp",
  "description": "Aplicação Django moderna",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/static/images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/static/images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable any"
    }
  ],
  "shortcuts": [
    {
      "name": "Dashboard",
      "short_name": "Dashboard",
      "description": "Acessar dashboard",
      "url": "/dashboard/",
      "icons": [{"src": "/static/images/dashboard-icon.png", "sizes": "96x96"}]
    }
  ]
}
```

### PWA Integration Template

**templates/base/pwa-head.html:**
```html
<!-- PWA Meta Tags -->
<meta name="theme-color" content="#3b82f6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Django App">

<!-- Manifest -->
<link rel="manifest" href="{% static 'manifest.json' %}">

<!-- Apple Touch Icons -->
<link rel="apple-touch-icon" href="{% static 'images/icon-180.png' %}">

<!-- PWA Installation -->
<script>
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // Mostrar botão de instalação
    const installButton = document.querySelector('#pwa-install-button');
    if (installButton) {
        installButton.style.display = 'block';
        installButton.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log('PWA installation:', outcome);
                deferredPrompt = null;
                installButton.style.display = 'none';
            }
        });
    }
});

// Registrar Service Worker
if ('serviceWorker' in navigator) {
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
</script>
```

## 🎨 Animações Avançadas

### CSS Animations

**static/src/css/animations.css:**
```css
@layer utilities {
  /* Fade animations */
  .fade-in {
    animation: fadeIn 0.5s ease-in-out;
  }
  
  .fade-in-up {
    animation: fadeInUp 0.6s ease-out;
  }
  
  .fade-in-down {
    animation: fadeInDown 0.6s ease-out;
  }
  
  /* Slide animations */
  .slide-in-right {
    animation: slideInRight 0.5s ease-out;
  }
  
  .slide-in-left {
    animation: slideInLeft 0.5s ease-out;
  }
  
  /* Scale animations */
  .scale-in {
    animation: scaleIn 0.3s ease-out;
  }
  
  /* Bounce animations */
  .bounce-in {
    animation: bounceIn 0.6s ease-out;
  }
  
  /* Stagger animations */
  .stagger-1 { animation-delay: 0.1s; }
  .stagger-2 { animation-delay: 0.2s; }
  .stagger-3 { animation-delay: 0.3s; }
  .stagger-4 { animation-delay: 0.4s; }
  .stagger-5 { animation-delay: 0.5s; }
}

/* Keyframes */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

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

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translate3d(0, -40px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

@keyframes slideInRight {
  from {
    transform: translate3d(100%, 0, 0);
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

@keyframes slideInLeft {
  from {
    transform: translate3d(-100%, 0, 0);
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }
  to {
    opacity: 1;
    transform: scale3d(1, 1, 1);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }
  20% {
    transform: scale3d(1.1, 1.1, 1.1);
  }
  40% {
    transform: scale3d(0.9, 0.9, 0.9);
  }
  60% {
    opacity: 1;
    transform: scale3d(1.03, 1.03, 1.03);
  }
  80% {
    transform: scale3d(0.97, 0.97, 0.97);
  }
  100% {
    opacity: 1;
    transform: scale3d(1, 1, 1);
  }
}

/* Hover effects */
.hover-lift {
  transition: transform 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-4px);
}

.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
}

/* Loading animations */
.pulse-slow {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.spin-slow {
  animation: spin 3s linear infinite;
}

/* Parallax effects */
.parallax {
  transform-style: preserve-3d;
}

.parallax-layer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.parallax-bg {
  transform: translateZ(-1px) scale(2);
}

.parallax-mid {
  transform: translateZ(-0.5px) scale(1.5);
}

.parallax-front {
  transform: translateZ(0);
}
```

### JavaScript Animation Controller

**static/src/js/animations.js:**
```javascript
class AnimationController {
    constructor() {
        this.observers = new Map();
        this.init();
    }

    init() {
        // Observer para animações on-scroll
        this.setupScrollAnimations();
        
        // Observer para parallax
        this.setupParallaxEffects();
        
        // Observer para contadores animados
        this.setupCounterAnimations();
    }

    setupScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.triggerAnimation(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '50px' });

        document.querySelectorAll('[data-animate]').forEach(el => {
            observer.observe(el);
        });

        this.observers.set('scroll', observer);
    }

    triggerAnimation(element) {
        const animationType = element.dataset.animate;
        const delay = element.dataset.animateDelay || 0;
        const duration = element.dataset.animateDuration || 600;

        setTimeout(() => {
            element.classList.add(animationType, 'opacity-100');
            element.classList.remove('opacity-0');
        }, delay);
    }

    setupParallaxEffects() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        if (parallaxElements.length > 0) {
            let ticking = false;
            
            const updateParallax = () => {
                parallaxElements.forEach(el => {
                    const speed = el.dataset.parallax || 0.5;
                    const rect = el.getBoundingClientRect();
                    const yPos = -(rect.top * speed);
                    el.style.transform = `translateY(${yPos}px)`;
                });
                ticking = false;
            };

            window.addEventListener('scroll', () => {
                if (!ticking) {
                    requestAnimationFrame(updateParallax);
                    ticking = true;
                }
            });
        }
    }

    setupCounterAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('[data-counter]').forEach(el => {
            observer.observe(el);
        });
    }

    animateCounter(element) {
        const target = parseInt(element.dataset.counter);
        const duration = parseInt(element.dataset.counterDuration) || 2000;
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            element.textContent = Math.floor(current);

            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    }

    // Método para adicionar animação programaticamente
    addAnimation(element, animationType, options = {}) {
        const { delay = 0, duration = 600, callback = null } = options;
        
        setTimeout(() => {
            element.classList.add(animationType);
            
            if (callback) {
                setTimeout(callback, duration);
            }
        }, delay);
    }

    // Método para animar elementos em sequência
    staggerAnimation(elements, animationType, staggerDelay = 100) {
        elements.forEach((element, index) => {
            this.addAnimation(element, animationType, {
                delay: index * staggerDelay
            });
        });
    }

    cleanup() {
        this.observers.forEach(observer => observer.disconnect());
    }
}

// Inicializar controlador de animações
document.addEventListener('DOMContentLoaded', () => {
    window.animationController = new AnimationController();
});
```

## 🔍 SEO e Acessibilidade

### SEO Meta Tags Template

**templates/base/seo-head.html:**
```html
{% load static %}

<!-- Basic SEO -->
<title>{{ page_title|default:"Página" }} | {{ site_name|default:"Django App" }}</title>
<meta name="description" content="{{ page_description|default:'Aplicação Django moderna e responsiva' }}">
<meta name="keywords" content="{{ page_keywords|default:'django, web, app' }}">
<meta name="author" content="{{ site_author|default:'Django Team' }}">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="{{ og_type|default:'website' }}">
<meta property="og:url" content="{{ request.build_absolute_uri }}">
<meta property="og:title" content="{{ page_title|default:'Página' }} | {{ site_name|default:'Django App' }}">
<meta property="og:description" content="{{ page_description|default:'Aplicação Django moderna e responsiva' }}">
<meta property="og:image" content="{{ og_image|default:'/static/images/og-default.jpg'|add_domain:request }}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{{ request.build_absolute_uri }}">
<meta property="twitter:title" content="{{ page_title|default:'Página' }} | {{ site_name|default:'Django App' }}">
<meta property="twitter:description" content="{{ page_description|default:'Aplicação Django moderna e responsiva' }}">
<meta property="twitter:image" content="{{ og_image|default:'/static/images/og-default.jpg'|add_domain:request }}">

<!-- Canonical URL -->
<link rel="canonical" href="{{ canonical_url|default:request.build_absolute_uri }}">

<!-- JSON-LD Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "{{ schema_type|default:'WebSite' }}",
  "name": "{{ site_name|default:'Django App' }}",
  "url": "{{ request.build_absolute_uri }}"
  {% if page_description %},
  "description": "{{ page_description }}"
  {% endif %}
  {% if schema_organization %},
  "publisher": {
    "@type": "Organization",
    "name": "{{ schema_organization }}"
  }
  {% endif %}
}
</script>
```

### Accessibility Helpers

**static/src/js/accessibility.js:**
```javascript
class AccessibilityHelper {
    constructor() {
        this.init();
    }

    init() {
        this.setupKeyboardNavigation();
        this.setupSkipLinks();
        this.setupAriaLiveRegions();
        this.setupFocusManagement();
        this.setupReducedMotion();
    }

    setupKeyboardNavigation() {
        // Navegação por tab mais inteligente
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // Escape para fechar modais/dropdowns
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeOpenElements();
            }
        });
    }

    setupSkipLinks() {
        // Criar skip links automáticos
        const skipLinks = document.createElement('div');
        skipLinks.className = 'skip-links sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0 z-50';
        skipLinks.innerHTML = `
            <a href="#main-content" class="btn btn-primary">Pular para conteúdo</a>
            <a href="#navigation" class="btn btn-primary">Pular para navegação</a>
        `;
        document.body.insertBefore(skipLinks, document.body.firstChild);
    }

    setupAriaLiveRegions() {
        // Região para anúncios dinâmicos
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        liveRegion.id = 'aria-live-region';
        document.body.appendChild(liveRegion);

        // Método global para anunciar mudanças
        window.announceToScreenReader = (message) => {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        };
    }

    setupFocusManagement() {
        // Gerenciar foco em modais
        document.addEventListener('modal-opened', (e) => {
            const modal = e.target;
            const focusableElements = modal.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            if (focusableElements.length > 0) {
                focusableElements[0].focus();
            }

            // Trap focus dentro do modal
            this.trapFocus(modal, focusableElements);
        });
    }

    trapFocus(container, focusableElements) {
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        container.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstFocusable) {
                        e.preventDefault();
                        lastFocusable.focus();
                    }
                } else {
                    if (document.activeElement === lastFocusable) {
                        e.preventDefault();
                        firstFocusable.focus();
                    }
                }
            }
        });
    }

    setupReducedMotion() {
        // Respeitar preferência do usuário por movimento reduzido
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        const handleReducedMotion = (mq) => {
            if (mq.matches) {
                document.body.classList.add('reduce-motion');
                // Desabilitar animações desnecessárias
                const style = document.createElement('style');
                style.textContent = `
                    *, *::before, *::after {
                        animation-duration: 0.01ms !important;
                        animation-iteration-count: 1 !important;
                        transition-duration: 0.01ms !important;
                        scroll-behavior: auto !important;
                    }
                `;
                document.head.appendChild(style);
            }
        };

        mediaQuery.addListener(handleReducedMotion);
        handleReducedMotion(mediaQuery);
    }

    closeOpenElements() {
        // Fechar dropdowns abertos
        document.querySelectorAll('[x-data]').forEach(el => {
            if (el._x_dataStack && el._x_dataStack[0].open) {
                el._x_dataStack[0].open = false;
            }
        });

        // Disparar evento personalizado para modais
        document.dispatchEvent(new CustomEvent('close-all-modals'));
    }

    // Método para melhorar contraste
    toggleHighContrast() {
        document.body.classList.toggle('high-contrast');
        localStorage.setItem('high-contrast', 
            document.body.classList.contains('high-contrast')
        );
    }

    // Método para aumentar tamanho da fonte
    increaseFontSize() {
        const currentSize = parseInt(getComputedStyle(document.documentElement).fontSize);
        document.documentElement.style.fontSize = (currentSize + 2) + 'px';
        localStorage.setItem('font-size', currentSize + 2);
    }

    decreaseFontSize() {
        const currentSize = parseInt(getComputedStyle(document.documentElement).fontSize);
        if (currentSize > 14) {
            document.documentElement.style.fontSize = (currentSize - 2) + 'px';
            localStorage.setItem('font-size', currentSize - 2);
        }
    }

    resetFontSize() {
        document.documentElement.style.fontSize = '';
        localStorage.removeItem('font-size');
    }
}

// Inicializar helper de acessibilidade
document.addEventListener('DOMContentLoaded', () => {
    window.accessibilityHelper = new AccessibilityHelper();
    
    // Restaurar preferências salvas
    if (localStorage.getItem('high-contrast') === 'true') {
        document.body.classList.add('high-contrast');
    }
    
    const savedFontSize = localStorage.getItem('font-size');
    if (savedFontSize) {
        document.documentElement.style.fontSize = savedFontSize + 'px';
    }
});
```

## 🔧 Integração com APIs Externas

### Generic API Client

**static/src/js/api-client.js:**
```javascript
class ApiClient {
    constructor(baseURL = '/api/') {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        };
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: { ...this.defaultHeaders },
            ...options
        };

        // Adicionar CSRF token se necessário
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (csrfToken && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(config.method)) {
            config.headers['X-CSRFToken'] = csrfToken;
        }

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    get(endpoint, params = {}) {
        const queryString = new URLSearch# 🚀 Frontend Advanced - Recursos Avançados (frontend_advanced.md)

## 🎯 Objetivo

Este documento cobre recursos avançados de frontend para projetos Django: animações, PWA, performance, SEO e integrações complexas.

## ⚡ Performance e Otimização