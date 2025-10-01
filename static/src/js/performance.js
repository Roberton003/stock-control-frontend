// Performance optimization utilities
class PerformanceOptimizer {
  constructor() {
    this.init();
  }

  init() {
    this.setupLazyLoading();
    this.setupCodeSplitting();
    this.setupResourceHints();
  }

  // Lazy loading for images
  setupLazyLoading() {
    // For images with loading="lazy" attribute
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
              img.src = img.dataset.src;
              img.removeAttribute('data-src');
              img.classList.remove('lazy');
              img.classList.add('loaded');
            }
            if (img.dataset.srcset) {
              img.srcset = img.dataset.srcset;
              img.removeAttribute('data-srcset');
            }
            observer.unobserve(img);
          }
        });
      });

      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });

      // For iframes
      const iframeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const iframe = entry.target;
            if (iframe.dataset.src) {
              iframe.src = iframe.dataset.src;
              iframe.removeAttribute('data-src');
            }
            observer.unobserve(iframe);
          }
        });
      });

      document.querySelectorAll('iframe[data-src]').forEach(iframe => {
        iframeObserver.observe(iframe);
      });
    } else {
      // Fallback for browsers without IntersectionObserver
      document.querySelectorAll('img[data-src]').forEach(img => {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      });
    }
  }

  // Lazy loading for components/content
  setupComponentLazyLoading() {
    if ('IntersectionObserver' in window) {
      const componentObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const component = entry.target;
            const src = component.dataset.componentSrc;
            
            if (src) {
              fetch(src)
                .then(response => response.text())
                .then(html => {
                  component.innerHTML = html;
                  component.classList.add('loaded');
                })
                .catch(error => {
                  console.error('Error loading component:', error);
                  component.innerHTML = '<div class="text-center p-4 text-red-500">Erro ao carregar componente</div>';
                });
            }
            
            observer.unobserve(component);
          }
        });
      });

      document.querySelectorAll('[data-component-src]').forEach(component => {
        componentObserver.observe(component);
      });
    }
  }

  // Resource hints for performance
  setupResourceHints() {
    // Preload critical resources
    this.preloadCriticalResources();
    
    // Prefetch likely-to-be-needed resources
    this.prefetchResources();
    
    // Preconnect to external domains
    this.preconnectExternalDomains();
  }

  preloadCriticalResources() {
    const criticalResources = [
      { href: '/static/dist/css/main.css', as: 'style' },
      { href: '/static/dist/js/main.js', as: 'script' },
    ];

    criticalResources.forEach(resource => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = resource.href;
      link.as = resource.as;
      document.head.appendChild(link);
    });
  }

  prefetchResources() {
    // Prefetch resources that might be needed soon
    const prefetchLinks = document.querySelectorAll('a[rel="prefetch"]');
    prefetchLinks.forEach(link => {
      const href = link.href;
      if (href) {
        const linkEl = document.createElement('link');
        linkEl.rel = 'prefetch';
        linkEl.href = href;
        document.head.appendChild(linkEl);
      }
    });
  }

  preconnectExternalDomains() {
    // Preconnect to external domains for performance
    const domains = [
      'https://fonts.googleapis.com',
      'https://fonts.gstatic.com',
      'https://cdnjs.cloudflare.com',
    ];

    domains.forEach(domain => {
      const link = document.createElement('link');
      link.rel = 'preconnect';
      link.href = domain;
      document.head.appendChild(link);
    });
  }

  // Code splitting for JavaScript modules
  async loadModule(modulePath) {
    try {
      const module = await import(modulePath);
      return module;
    } catch (error) {
      console.error(`Error loading module ${modulePath}:`, error);
      return null;
    }
  }

  // Dynamic imports for code splitting
  async loadFeature(featureName) {
    switch (featureName) {
      case 'charts':
        return await this.loadModule('/static/src/js/features/charts.js');
      case 'tables':
        return await this.loadModule('/static/src/js/features/tables.js');
      case 'forms':
        return await this.loadModule('/static/src/js/features/forms.js');
      case 'modals':
        return await this.loadModule('/static/src/js/features/modals.js');
      default:
        console.warn(`Unknown feature: ${featureName}`);
        return null;
    }
  }

  // Debounced resize handler
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

  // Throttled scroll handler
  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  // Optimize image loading
  optimizeImages() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
      // Set appropriate loading attribute
      if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
      
      // Add error handling
      img.addEventListener('error', () => {
        img.src = '/static/images/placeholder.png';
        img.alt = 'Imagem não disponível';
      });
    });
  }

  // Cleanup function
  destroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}

// Initialize performance optimizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.performanceOptimizer = new PerformanceOptimizer();
});

// Add performance monitoring
if ('performance' in window) {
  window.addEventListener('load', () => {
    setTimeout(() => {
      const perfData = performance.getEntriesByType('navigation')[0];
      const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
      
      // Log performance data (in a real app, you might send this to analytics)
      console.log(`Page load time: ${loadTime}ms`);
    }, 0);
  });
}