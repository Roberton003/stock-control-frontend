<template>
  <div :class="spinnerClass" role="status">
    <span class="sr-only">Loading...</span>
  </div>
</template>

<script>
export default {
  name: 'Spinner',
  props: {
    variant: {
      type: String,
      default: 'primary'
    },
    size: {
      type: String,
      default: 'md'
    }
  },
  computed: {
    spinnerClass() {
      let baseClass = 'inline-block animate-spin rounded-full '

      // Variant styles
      switch (this.variant) {
        case 'primary':
          baseClass += 'border-primary '
          break
        case 'secondary':
          baseClass += 'border-secondary '
          break
        case 'accent':
          baseClass += 'border-accent '
          break
        default:
          baseClass += 'border-primary '
      }

      // Size styles
      switch (this.size) {
        case 'sm':
          baseClass += 'h-4 w-4 border-2 '
          break
        case 'lg':
          baseClass += 'h-8 w-8 border-4 '
          break
        default:
          baseClass += 'h-6 w-6 border-3 '
      }

      // Add border styling
      baseClass += 'border-t-transparent '

      return baseClass
    }
  }
}
</script>