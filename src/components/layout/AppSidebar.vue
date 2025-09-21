<template>
  <aside class="bg-white w-64 shadow-md">
    <div class="p-4">
      <h2 class="text-lg font-semibold text-dark">Navigation</h2>
    </div>
    <nav>
      <ul>
        <li>
          <a href="#" class="block px-4 py-2 text-dark hover:bg-light">Dashboard</a>
        </li>
        <li>
          <a href="#" class="block px-4 py-2 text-dark hover:bg-light">Reagents</a>
        </li>
        <li>
          <a href="#" class="block px-4 py-2 text-dark hover:bg-light">Stock Lots</a>
        </li>
        <li>
          <a href="#" class="block px-4 py-2 text-dark hover:bg-light">Requisitions</a>
        </li>
        <li>
          <a href="#" class="block px-4 py-2 text-dark hover:bg-light">Reports</a>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script>
export default {
  name: 'AppSidebar'
}
</script>