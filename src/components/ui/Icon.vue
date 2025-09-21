<template>
  <i :class="iconClass" :style="iconStyle"></i>
</template>

<script>
export default {
  name: 'Icon',
  props: {
    name: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: 'md'
    },
    color: {
      type: String,
      default: 'currentColor'
    }
  },
  computed: {
    iconClass() {
      return `fa fa-${this.name}`
    },
    iconStyle() {
      let style = {}
      
      // Size styles
      switch (this.size) {
        case 'xs':
          style.fontSize = '0.75rem'
          break
        case 'sm':
          style.fontSize = '0.875rem'
          break
        case 'lg':
          style.fontSize = '1.125rem'
          break
        case 'xl':
          style.fontSize = '1.25rem'
          break
        case '2xl':
          style.fontSize = '1.5rem'
          break
        case '3xl':
          style.fontSize = '1.875rem'
          break
        default:
          style.fontSize = '1rem'
      }
      
      // Color style
      if (this.color !== 'currentColor') {
        style.color = this.color
      }
      
      return style
    }
  }
}
</script>