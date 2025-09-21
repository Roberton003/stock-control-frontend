<template>
  <button 
    :class="buttonClass" 
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    variant: {
      type: String,
      default: 'primary'
    },
    size: {
      type: String,
      default: 'md'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click'],
  computed: {
    buttonClass() {
      let baseClass = 'rounded font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 '
      
      // Variant styles
      switch (this.variant) {
        case 'primary':
          baseClass += 'bg-primary text-white hover:bg-opacity-90 focus:ring-primary '
          break
        case 'secondary':
          baseClass += 'bg-secondary text-white hover:bg-opacity-90 focus:ring-secondary '
          break
        case 'accent':
          baseClass += 'bg-accent text-white hover:bg-opacity-90 focus:ring-accent '
          break
        case 'outline':
          baseClass += 'bg-transparent border border-primary text-primary hover:bg-primary hover:text-white focus:ring-primary '
          break
        default:
          baseClass += 'bg-primary text-white hover:bg-opacity-90 focus:ring-primary '
      }
      
      // Size styles
      switch (this.size) {
        case 'sm':
          baseClass += 'px-3 py-1.5 text-sm '
          break
        case 'lg':
          baseClass += 'px-6 py-3 text-lg '
          break
        default:
          baseClass += 'px-4 py-2 text-base '
      }
      
      // Disabled state
      if (this.disabled) {
        baseClass += 'opacity-50 cursor-not-allowed '
      }
      
      return baseClass
    }
  }
}
</script>