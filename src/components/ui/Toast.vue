<!-- src/components/ui/Toast.vue -->
<template>
  <div class="fixed bottom-4 right-4 z-50 space-y-2">
    <transition-group name="toast" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="toastClass(toast.type)"
        class="rounded-lg p-4 shadow-lg flex items-start"
      >
        <div class="flex-shrink-0 mr-3">
          <i :class="iconClass(toast.type)"></i>
        </div>
        <div class="flex-1">
          <p class="text-sm font-medium">{{ toast.message }}</p>
        </div>
        <button
          @click="removeToast(toast.id)"
          class="ml-4 text-white hover:text-gray-200 focus:outline-none"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast'

export default {
  name: 'Toast',
  setup() {
    const { toasts, removeToast } = useToast()
    
    const toastClass = (type) => {
      switch (type) {
        case 'success':
          return 'bg-green-500 text-white'
        case 'error':
          return 'bg-red-500 text-white'
        case 'warning':
          return 'bg-yellow-500 text-white'
        case 'info':
        default:
          return 'bg-blue-500 text-white'
      }
    }
    
    const iconClass = (type) => {
      switch (type) {
        case 'success':
          return 'fas fa-check-circle'
        case 'error':
          return 'fas fa-exclamation-circle'
        case 'warning':
          return 'fas fa-exclamation-triangle'
        case 'info':
        default:
          return 'fas fa-info-circle'
      }
    }
    
    return {
      toasts,
      removeToast,
      toastClass,
      iconClass
    }
  }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>