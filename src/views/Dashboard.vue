<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    
    <!-- Cards de resumo -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Valor Total em Estoque</h2>
        </template>
        <div class="text-3xl font-bold text-primary">R$ 125.430,00</div>
        <div class="text-sm text-gray-500 mt-2">+2,5% em relação ao mês anterior</div>
      </Card>
      
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Itens Abaixo do Mínimo</h2>
        </template>
        <div class="text-3xl font-bold text-red-500">12</div>
        <div class="text-sm text-gray-500 mt-2">Necessita reposição urgente</div>
      </Card>
      
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Lotes Próximos ao Vencimento</h2>
        </template>
        <div class="text-3xl font-bold text-yellow-500">8</div>
        <div class="text-sm text-gray-500 mt-2">Vencem em menos de 30 dias</div>
      </Card>
      
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Movimentações Hoje</h2>
        </template>
        <div class="text-3xl font-bold text-green-500">24</div>
        <div class="text-sm text-gray-500 mt-2">Entradas: 15 | Saídas: 9</div>
      </Card>
    </div>
    
    <!-- Gráficos -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Consumo por Categoria (Últimos 30 dias)</h2>
        </template>
        <div class="h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de barras será implementado aqui</p>
        </div>
      </Card>
      
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Validade dos Lotes</h2>
        </template>
        <div class="h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de pizza será implementado aqui</p>
        </div>
      </Card>
    </div>
    
    <!-- Tabela de movimentações recentes -->
    <Card class="bg-white mb-8">
      <template #header>
        <h2 class="text-lg font-semibold">Movimentações Recentes</h2>
      </template>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reagente</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuário</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">15/09/2023 14:30</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Ácido Clorídrico</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600">Entrada</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">5 litros</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">João Silva</td>
            </tr>
            <tr>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">15/09/2023 11:45</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Etanol 96%</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600">Saída</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2 litros</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Maria Oliveira</td>
            </tr>
            <tr>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">14/09/2023 16:20</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Sulfato de Cobre</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600">Entrada</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">1 kg</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Pedro Santos</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
    
    <!-- Widgets de alerta de validade -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card class="bg-white border-l-4 border-yellow-500">
        <template #header>
          <h2 class="text-lg font-semibold text-yellow-700">Alertas de Validade</h2>
        </template>
        <ul class="space-y-2">
          <li class="flex items-center">
            <Icon name="exclamation-triangle" class="text-yellow-500 mr-2" />
            <span class="text-sm">Ácido Nítrico (Lote #A12345) - Vence em 15 dias</span>
          </li>
          <li class="flex items-center">
            <Icon name="exclamation-triangle" class="text-yellow-500 mr-2" />
            <span class="text-sm">Hidróxido de Sódio (Lote #B67890) - Vence em 22 dias</span>
          </li>
        </ul>
      </Card>
      
      <Card class="bg-white border-l-4 border-red-500">
        <template #header>
          <h2 class="text-lg font-semibold text-red-700">Estoque Baixo</h2>
        </template>
        <ul class="space-y-2">
          <li class="flex items-center">
            <Icon name="exclamation-circle" class="text-red-500 mr-2" />
            <span class="text-sm">Etanol 70% - Apenas 3 litros disponíveis</span>
          </li>
          <li class="flex items-center">
            <Icon name="exclamation-circle" class="text-red-500 mr-2" />
            <span class="text-sm">Água Destilada - Apenas 5 litros disponíveis</span>
          </li>
        </ul>
      </Card>
    </div>
  </div>
</template>

<script>
import Card from '@/components/ui/Card.vue'
import Icon from '@/components/ui/Icon.vue'

export default {
  name: 'Dashboard',
  components: {
    Card,
    Icon
  },
  setup() {
    // Dados do dashboard serão obtidos através de chamadas à API
    // Esta é uma implementação inicial com dados fictícios
    
    return {}
  }
}
</script>