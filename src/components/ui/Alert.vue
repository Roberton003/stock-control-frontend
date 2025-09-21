<template>
  <div :class="alertClass" role="alert">
    <div class="flex">
      <div class="flex-shrink-0">
        <i :class="iconClass"></i>
      </div>
      <div class="ml-3">
        <h3 class="text-sm font-medium" :class="titleClass">
          <slot name="title" />
        </h3>
        <div class="mt-2 text-sm" :class="messageClass">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Alert',
  props: {
    variant: {
      type: String,
      default: 'info'
    }
  },
  computed: {
    alertClass() {
      let baseClass = 'rounded-md p-4 '
      
      switch (this.variant) {
        case 'success':
          baseClass += 'bg-green-50 '
          break
        case 'error':
          baseClass += 'bg-red-50 '
          break
        case 'warning':
          baseClass += 'bg-yellow-50 '
          break
        case 'info':
        default:
          baseClass += 'bg-blue-50 '
      }
      
      return baseClass
    },
    iconClass() {
      let baseClass = 'h-5 w-5 '
      
      switch (this.variant) {
        case 'success':
          baseClass += 'text-green-400 '
          break
        case 'error':
          baseClass += 'text-red-400 '
          break
        case 'warning':
          baseClass += 'text-yellow-400 '
          break
        case 'info':
        default:
          baseClass += 'text-blue-400 '
      }
      
      return baseClass
    },
    titleClass() {
      let baseClass = ''
      
      switch (this.variant) {
        case 'success':
          baseClass += 'text-green-800 '
          break
        case 'error':
          baseClass += 'text-red-800 '
          break
        case 'warning':
          baseClass += 'text-yellow-800 '
          break
        case 'info':
        default:
          baseClass += 'text-blue-800 '
      }
      
      return baseClass
    },
    messageClass() {
      let baseClass = ''
      
      switch (this.variant) {
        case 'success':
          baseClass += 'text-green-700 '
          break
        case 'error':
          baseClass += 'text-red-700 '
          break
        case 'warning':
          baseClass += 'text-yellow-700 '
          break
        case 'info':
        default:
          baseClass += 'text-blue-700 '
      }
      
      return baseClass
    }
  }
}
</script>