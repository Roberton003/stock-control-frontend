<template>
  <div class="min-h-screen bg-light flex flex-col">
    <AppHeader />
    <div class="flex flex-1">
      <AppSidebar />
      <main class="flex-1 p-6">
        <router-view />
      </main>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import { AppHeader, AppSidebar, AppFooter } from '@components/layout'

export default {
  name: 'AppLayout',
  components: {
    AppHeader,
    AppSidebar,
    AppFooter
  }
}
</script>