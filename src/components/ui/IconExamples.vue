<template>
  <!-- Exemplo de uso dos ícones padrão -->
  <div class="flex space-x-4">
    <Icon name="home" size="lg" color="primary" />
    <Icon name="user" size="lg" color="secondary" />
    <Icon name="cog" size="lg" color="accent" />
    <Icon name="search" size="lg" />
    <Icon name="plus" size="lg" />
    <Icon name="edit" size="lg" />
    <Icon name="trash" size="lg" />
    <Icon name="check" size="lg" />
    <Icon name="times" size="lg" />
    <Icon name="info-circle" size="lg" />
    <Icon name="exclamation-triangle" size="lg" />
    <Icon name="exclamation-circle" size="lg" />
  </div>
</template>

<script>
import Icon from './Icon.vue'

export default {
  name: 'IconExamples',
  components: {
    Icon
  }
}
</script>