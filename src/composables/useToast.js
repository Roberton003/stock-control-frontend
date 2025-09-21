// src/composables/useToast.js
import { ref } from 'vue'

const toasts = ref([])

export function useToast() {
  const addToast = (message, type = 'info', duration = 5000) => {
    const id = Date.now()
    const toast = { id, message, type, duration }
    
    toasts.value.push(toast)
    
    // Remover o toast automaticamente após o tempo especificado
    setTimeout(() => {
      removeToast(id)
    }, duration)
    
    return id
  }
  
  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  const clearAllToasts = () => {
    toasts.value = []
  }
  
  return {
    toasts: toasts.value,
    addToast,
    removeToast,
    clearAllToasts
  }
}