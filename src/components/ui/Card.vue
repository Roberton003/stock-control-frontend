<template>
  <div :class="cardClass">
    <div v-if="$slots.header" class="border-b border-light p-4">
      <slot name="header" />
    </div>
    <div class="p-4">
      <slot />
    </div>
    <div v-if="$slots.footer" class="border-t border-light p-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    variant: {
      type: String,
      default: 'default'
    },
    shadow: {
      type: String,
      default: 'md'
    }
  },
  computed: {
    cardClass() {
      let baseClass = 'bg-white rounded-lg '
      
      // Shadow styles
      switch (this.shadow) {
        case 'sm':
          baseClass += 'shadow-sm '
          break
        case 'lg':
          baseClass += 'shadow-lg '
          break
        case 'xl':
          baseClass += 'shadow-xl '
          break
        default:
          baseClass += 'shadow-md '
      }
      
      // Variant styles
      switch (this.variant) {
        case 'primary':
          baseClass += 'border-l-4 border-primary '
          break
        case 'secondary':
          baseClass += 'border-l-4 border-secondary '
          break
        case 'accent':
          baseClass += 'border-l-4 border-accent '
          break
        default:
          baseClass += 'border border-light '
      }
      
      return baseClass
    }
  }
}
</script>