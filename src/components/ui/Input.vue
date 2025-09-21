<template>
  <input
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :class="inputClass"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script>
export default {
  name: 'Input',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    placeholder: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    variant: {
      type: String,
      default: 'default'
    }
  },
  emits: ['update:modelValue'],
  computed: {
    inputClass() {
      let baseClass = 'block w-full rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 '
      
      // Variant styles
      switch (this.variant) {
        case 'primary':
          baseClass += 'border-light focus:border-primary focus:ring-primary '
          break
        case 'secondary':
          baseClass += 'border-light focus:border-secondary focus:ring-secondary '
          break
        default:
          baseClass += 'border-light focus:border-primary focus:ring-primary '
      }
      
      // Disabled state
      if (this.disabled) {
        baseClass += 'bg-light text-dark cursor-not-allowed '
      } else {
        baseClass += 'bg-white text-dark '
      }
      
      return baseClass
    }
  }
}
</script>