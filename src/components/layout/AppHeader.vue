<template>
  <header class="bg-primary text-white shadow-md">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
      <h1 class="text-xl font-bold">Stock Control Lab</h1>
      <nav>
        <ul class="flex space-x-4">
          <li><a href="#" class="hover:text-secondary">Dashboard</a></li>
          <li><a href="#" class="hover:text-secondary">Reagents</a></li>
          <li><a href="#" class="hover:text-secondary">Stock Lots</a></li>
          <li><a href="#" class="hover:text-secondary">Requisitions</a></li>
          <li><a href="#" class="hover:text-secondary">Reports</a></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
}
</script>