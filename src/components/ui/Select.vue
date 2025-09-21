<template>
  <select
    :value="modelValue"
    :disabled="disabled"
    :class="selectClass"
    @change="$emit('update:modelValue', $event.target.value)"
  >
    <option 
      v-for="(option, index) in options" 
      :key="index"
      :value="option.value"
    >
      {{ option.label }}
    </option>
  </select>
</template>

<script>
export default {
  name: 'Select',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    options: {
      type: Array,
      default: () => []
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
    selectClass() {
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