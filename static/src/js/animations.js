// Enhanced animations for modern frontend
class ModernAnimations {
  constructor() {
    this.init();
  }

  init() {
    this.setupIntersectionObserver();
    this.setupScrollAnimations();
    this.setupHoverEffects();
  }

  // Setup intersection observer for scroll animations
  setupIntersectionObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateElement(entry.target);
          this.observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    // Observe elements with data-animate attribute
    document.querySelectorAll('[data-animate]').forEach(el => {
      this.observer.observe(el);
    });
  }

  // Animate elements when they come into view
  animateElement(element) {
    const animationType = element.dataset.animate || 'fade-in-up';
    const delay = element.dataset.animateDelay || 0;
    const duration = element.dataset.animateDuration || 600;

    setTimeout(() => {
      element.classList.add('animate-' + animationType);
      element.style.opacity = '1';
    }, delay);
  }

  // Setup scroll-based animations
  setupScrollAnimations() {
    let ticking = false;

    const updateAnimations = () => {
      // Parallax effects
      document.querySelectorAll('[data-parallax]').forEach(el => {
        const speed = parseFloat(el.dataset.parallax) || 0.5;
        const rect = el.getBoundingClientRect();
        const yPos = -(rect.top * speed);
        el.style.transform = `translateY(${yPos}px)`;
      });

      // Progress bars
      document.querySelectorAll('[data-progress]').forEach(el => {
        const progress = parseFloat(el.dataset.progress) || 0;
        const rect = el.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;

        if (isVisible && !el.dataset.animated) {
          el.style.width = `${progress}%`;
          el.dataset.animated = true;
        }
      });

      ticking = false;
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateAnimations);
        ticking = true;
      }
    });
  }

  // Setup hover effects
  setupHoverEffects() {
    // Enhanced hover effects for cards
    document.querySelectorAll('.card-hover').forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.classList.add('hover-lift', 'shadow-lg');
      });

      card.addEventListener('mouseleave', () => {
        card.classList.remove('hover-lift', 'shadow-lg');
      });
    });
  }

  // Staggered animations
  stagger(elements, animationType = 'fade-in-up', delay = 100) {
    elements.forEach((el, index) => {
      el.dataset.animate = animationType;
      el.dataset.animateDelay = index * delay;
      this.observer.observe(el);
    });
  }

  // Counter animations
  animateCounter(element) {
    const target = parseInt(element.dataset.counter);
    const duration = parseInt(element.dataset.counterDuration) || 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 16);
  }

  // Text typing animation
  typeText(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    const type = () => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        setTimeout(type, speed);
      }
    };
    
    type();
  }

  // Loading animations
  showLoading(element, type = 'spinner') {
    if (type === 'spinner') {
      element.innerHTML = `
        <div class="flex items-center justify-center">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-current"></div>
        </div>
      `;
    } else if (type === 'skeleton') {
      element.classList.add('animate-pulse');
      element.innerHTML = '<div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>';
    }
  }
}

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.modernAnimations = new ModernAnimations();
});

// Enhanced modal animations
class ModernModal {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    this.overlay = this.modal.querySelector('.modal-overlay');
    this.content = this.modal.querySelector('.modal-content');
  }

  open() {
    this.modal.classList.remove('hidden');
    this.modal.classList.add('flex');
    
    // Trigger entrance animation
    setTimeout(() => {
      this.overlay.style.opacity = '1';
      this.content.style.opacity = '1';
      this.content.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 10);
  }

  close() {
    // Trigger exit animation
    this.overlay.style.opacity = '0';
    this.content.style.opacity = '0';
    this.content.style.transform = 'translate(-50%, -50%) scale(0.95)';
    
    setTimeout(() => {
      this.modal.classList.add('hidden');
      this.modal.classList.remove('flex');
    }, 150);
  }
}

// Add to global scope
window.ModernModal = ModernModal;

// Enhanced toast notifications
class ModernToast {
  constructor() {
    this.container = document.getElementById('toast-container');
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      this.container.className = 'fixed top-4 right-4 z-50 space-y-2';
      document.body.appendChild(this.container);
    }
  }

  show(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `flex items-center p-4 rounded-lg shadow-lg transform transition-all duration-300 ease-in-out ${
      type === 'success' ? 'bg-green-500' : 
      type === 'warning' ? 'bg-amber-500' : 
      type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    } text-white`;
    
    toast.innerHTML = `
      <div class="flex-1">
        <p class="text-sm">${message}</p>
      </div>
      <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.remove()">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    `;
    
    // Add entrance animation
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    
    this.container.appendChild(toast);
    
    // Trigger entrance animation
    setTimeout(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(0)';
    }, 10);

    // Auto remove after duration
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, duration);
  }
}

// Add to global scope
window.ModernToast = ModernToast;