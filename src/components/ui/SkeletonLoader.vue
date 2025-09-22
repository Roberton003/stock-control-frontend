<template>
  <div 
    v-if="count > 0" 
    class="animate-pulse space-y-4"
    :style="{ '--animation-duration': duration + 'ms' }"
  >
    <div 
      v-for="i in count" 
      :key="i" 
      class="flex items-center space-x-4"
    >
      <div 
        v-if="type === 'list' || type === 'default'"
        class="rounded-full bg-gray-200 h-12 w-12"
        :style="{ backgroundColor: baseColor }"
      ></div>
      <div 
        v-if="type === 'list' || type === 'default'"
        class="flex-1 space-y-2"
      >
        <div 
          class="h-4 rounded bg-gray-200"
          :style="{ backgroundColor: baseColor }"
        ></div>
        <div 
          class="h-4 rounded bg-gray-200 w-3/4"
          :style="{ backgroundColor: baseColor }"
        ></div>
      </div>
      <div 
        v-if="type === 'table'"
        class="flex-1 grid grid-cols-4 gap-4"
      >
        <div 
          v-for="j in 4" 
          :key="j"
          class="h-4 rounded bg-gray-200"
          :style="{ backgroundColor: baseColor }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SkeletonLoader',
  props: {
    count: {
      type: Number,
      default: 1
    },
    duration: {
      type: Number,
      default: 1500
    },
    baseColor: {
      type: String,
      default: '#f0f0f0'
    },
    highlightColor: {
      type: String,
      default: '#e0e0e0'
    },
    type: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'list', 'table'].includes(value)
    }
  },
  setup(props) {
    // Adicionar estilos CSS dinâmicos
    const addDynamicStyles = () => {
      const style = document.createElement('style')
      style.innerHTML = `
        .animate-pulse {
          animation: pulse var(--animation-duration, 1500ms) ease-in-out infinite;
        }
        
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }
      `
      document.head.appendChild(style)
    }
    
    // Adicionar estilos quando o componente for montado
    addDynamicStyles()
    
    return {}
  }
}
</script>

<style scoped>
.animate-pulse {
  animation: pulse var(--animation-duration, 1500ms) ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>