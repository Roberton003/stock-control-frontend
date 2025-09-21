<template>
  <table class="min-w-full divide-y divide-light">
    <thead class="bg-light">
      <tr>
        <th 
          v-for="(header, index) in headers" 
          :key="index"
          class="px-6 py-3 text-left text-xs font-medium text-dark uppercase tracking-wider"
        >
          {{ header }}
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-light">
      <tr 
        v-for="(row, rowIndex) in rows" 
        :key="rowIndex"
        class="hover:bg-light"
      >
        <td 
          v-for="(cell, cellIndex) in row" 
          :key="cellIndex"
          class="px-6 py-4 whitespace-nowrap text-sm text-dark"
        >
          {{ cell }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'Table',
  props: {
    headers: {
      type: Array,
      required: true
    },
    rows: {
      type: Array,
      required: true
    }
  }
}
</script>