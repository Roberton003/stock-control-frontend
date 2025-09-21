<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Visualizações Gráficas</h1>
      <p class="text-gray-600">Gráficos e visualizações para análise de dados</p>
    </div>
    
    <!-- Gráficos de barras -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Consumo por Categoria</h2>
      </template>
      <div class="p-4">
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de barras representando o consumo por categoria seria exibido aqui</p>
        </div>
      </div>
    </Card>
    
    <!-- Gráficos de pizza -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Distribuição de Estoque</h2>
      </template>
      <div class="p-4">
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de pizza representando a distribuição de estoque por categoria seria exibido aqui</p>
        </div>
      </div>
    </Card>
    
    <!-- Gráficos de linha -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Tendência de Consumo</h2>
      </template>
      <div class="p-4">
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de linha representando a tendência de consumo ao longo do tempo seria exibido aqui</p>
        </div>
      </div>
    </Card>
    
    <!-- Gráficos de área -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Validade dos Lotes</h2>
      </template>
      <div class="p-4">
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de área representando a validade dos lotes seria exibido aqui</p>
        </div>
      </div>
    </Card>
    
    <!-- Gráficos combinados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Comparação de Movimentações</h2>
      </template>
      <div class="p-4">
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico combinado representando entradas e saídas de estoque seria exibido aqui</p>
        </div>
      </div>
    </Card>
    
    <!-- Controles de visualização -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Controles de Visualização</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Gráfico</label>
          <Select v-model="chartType" :options="chartTypes" placeholder="Selecione um tipo" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Período</label>
          <Select v-model="period" :options="periods" placeholder="Selecione um período" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
          <Select v-model="category" :options="categories" placeholder="Selecione uma categoria" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Reagente</label>
          <Select v-model="reagent" :options="reagents" placeholder="Selecione um reagente" />
        </div>
      </div>
      <div class="px-4 pb-4">
        <Button variant="outline" @click="applyFilters">Aplicar Filtros</Button>
      </div>
    </Card>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'

export default {
  name: 'ChartViews',
  components: {
    Card,
    Button,
    Select
  },
  setup() {
    // Estados
    const chartType = ref('')
    const period = ref('')
    const category = ref('')
    const reagent = ref('')
    
    // Opções para seletores
    const chartTypes = ref([
      { value: 'bar', label: 'Barras' },
      { value: 'pie', label: 'Pizza' },
      { value: 'line', label: 'Linha' },
      { value: 'area', label: 'Área' },
      { value: 'combined', label: 'Combinado' }
    ])
    
    const periods = ref([
      { value: 'week', label: 'Última Semana' },
      { value: 'month', label: 'Último Mês' },
      { value: 'quarter', label: 'Último Trimestre' },
      { value: 'year', label: 'Último Ano' },
      { value: 'custom', label: 'Personalizado' }
    ])
    
    const categories = ref([
      { value: 1, label: 'Ácidos' },
      { value: 2, label: 'Bases' },
      { value: 3, label: 'Sais' },
      { value: 4, label: 'Álcoois' },
      { value: 5, label: 'Indicadores' }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' },
      { value: 4, label: 'Ácido Nítrico' },
      { value: 5, label: 'Hidróxido de Sódio' }
    ])
    
    // Métodos
    const applyFilters = () => {
      // Lógica para aplicar os filtros e atualizar os gráficos
      console.log('Aplicando filtros:', {
        chartType: chartType.value,
        period: period.value,
        category: category.value,
        reagent: reagent.value
      })
    }
    
    return {
      chartType,
      period,
      category,
      reagent,
      chartTypes,
      periods,
      categories,
      reagents,
      applyFilters
    }
  }
}
</script>