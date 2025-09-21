<template>
  <span :class="badgeClass">
    <slot />
  </span>
</template>

<script>
export default {
  name: 'Badge',
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
    badgeClass() {
      let baseClass = 'inline-flex items-center rounded-full font-medium '

      // Variant styles
      switch (this.variant) {
        case 'primary':
          baseClass += 'bg-primary bg-opacity-10 text-primary '
          break
        case 'secondary':
          baseClass += 'bg-secondary bg-opacity-10 text-secondary '
          break
        case 'accent':
          baseClass += 'bg-accent bg-opacity-10 text-accent '
          break
        case 'success':
          baseClass += 'bg-green-100 text-green-800 '
          break
        case 'warning':
          baseClass += 'bg-yellow-100 text-yellow-800 '
          break
        case 'error':
          baseClass += 'bg-red-100 text-red-800 '
          break
        default:
          baseClass += 'bg-primary bg-opacity-10 text-primary '
      }

      // Size styles
      switch (this.size) {
        case 'sm':
          baseClass += 'px-2 py-0.5 text-xs '
          break
        case 'lg':
          baseClass += 'px-3 py-1 text-base '
          break
        default:
          baseClass += 'px-2.5 py-0.5 text-sm '
      }

      return baseClass
    }
  }
}
</script>