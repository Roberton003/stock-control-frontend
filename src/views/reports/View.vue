<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-2">Visualização do Relatório</h1>
      <p class="text-gray-600">Relatório de Consumo de Reagentes - Período de 01/09/2023 a 15/09/2023</p>
    </div>
    
    <!-- Controles do relatório -->
    <Card class="mb-6 bg-white">
      <div class="p-4 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-4">
          <Button variant="outline" @click="printReport">
            <Icon name="print" class="mr-2" />
            Imprimir
          </Button>
          <Button variant="outline" @click="exportReport('pdf')">
            <Icon name="file-pdf" class="mr-2 text-red-500" />
            Exportar PDF
          </Button>
          <Button variant="outline" @click="exportReport('excel')">
            <Icon name="file-excel" class="mr-2 text-green-500" />
            Exportar Excel
          </Button>
        </div>
        <div class="flex items-center space-x-2">
          <label class="text-sm text-gray-700">Zoom:</label>
          <Select v-model="zoomLevel" :options="zoomOptions" class="w-32" />
        </div>
      </div>
    </Card>
    
    <!-- Conteúdo do relatório -->
    <div :style="{ zoom: zoomLevel }" class="bg-white p-8 shadow-sm">
      <!-- Cabeçalho do relatório -->
      <div class="mb-8 text-center">
        <h1 class="text-2xl font-bold">Relatório de Consumo de Reagentes</h1>
        <p class="mt-2 text-gray-600">Laboratório de Química - Universidade XYZ</p>
        <p class="mt-1 text-gray-600">Período: 01/09/2023 a 15/09/2023</p>
        <div class="mt-4 h-px bg-gray-300"></div>
      </div>
      
      <!-- Resumo estatístico -->
      <div class="mb-8">
        <h2 class="text-lg font-semibold mb-4">Resumo Estatístico</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card class="border border-gray-200">
            <div class="p-4">
              <div class="text-3xl font-bold text-center text-primary">24</div>
              <div class="mt-2 text-center text-gray-600">Reagentes Consumidos</div>
            </div>
          </Card>
          <Card class="border border-gray-200">
            <div class="p-4">
              <div class="text-3xl font-bold text-center text-secondary">125.430,00</div>
              <div class="mt-2 text-center text-gray-600">Valor Total (R$)</div>
            </div>
          </Card>
          <Card class="border border-gray-200">
            <div class="p-4">
              <div class="text-3xl font-bold text-center text-accent">8</div>
              <div class="mt-2 text-center text-gray-600">Lotes Próximos ao Vencimento</div>
            </div>
          </Card>
        </div>
      </div>
      
      <!-- Gráficos -->
      <div class="mb-8">
        <h2 class="text-lg font-semibold mb-4">Consumo por Categoria</h2>
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de barras representando o consumo por categoria seria exibido aqui</p>
        </div>
      </div>
      
      <div class="mb-8">
        <h2 class="text-lg font-semibold mb-4">Validade dos Lotes</h2>
        <div class="bg-gray-100 border border-dashed border-gray-300 rounded h-64 flex items-center justify-center">
          <p class="text-gray-500">Gráfico de pizza representando a validade dos lotes seria exibido aqui</p>
        </div>
      </div>
      
      <!-- Tabela de dados -->
      <div class="mb-8">
        <h2 class="text-lg font-semibold mb-4">Detalhamento de Consumo</h2>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead>
              <tr class="bg-gray-50">
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reagente</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade Consumida</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Valor (R$)</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in reportData" :key="index">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.reagent }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.unit }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Rodapé do relatório -->
      <div class="pt-8 text-center text-sm text-gray-500 border-t border-gray-300">
        <p>Relatório gerado em {{ currentDate }} por João Silva</p>
        <p class="mt-1">Este relatório é confidencial e destinado apenas para uso interno.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'
import Icon from '@/components/ui/Icon.vue'

export default {
  name: 'ReportView',
  components: {
    Card,
    Button,
    Select,
    Icon
  },
  setup() {
    // Estados
    const zoomLevel = ref('100%')
    
    // Dados fictícios para demonstração
    const zoomOptions = ref([
      { value: '50%', label: '50%' },
      { value: '75%', label: '75%' },
      { value: '90%', label: '90%' },
      { value: '100%', label: '100%' },
      { value: '125%', label: '125%' },
      { value: '150%', label: '150%' }
    ])
    
    const reportData = ref([
      {
        reagent: 'Ácido Clorídrico',
        category: 'Ácidos',
        unit: 'Litro',
        quantity: 15,
        value: '675,00'
      },
      {
        reagent: 'Etanol 96%',
        category: 'Álcoois',
        unit: 'Litro',
        quantity: 25,
        value: '375,00'
      },
      {
        reagent: 'Sulfato de Cobre',
        category: 'Sais',
        unit: 'Kilograma',
        quantity: 3,
        value: '180,00'
      },
      {
        reagent: 'Hidróxido de Sódio',
        category: 'Bases',
        unit: 'Kilograma',
        quantity: 2,
        value: '120,00'
      },
      {
        reagent: 'Ácido Nítrico',
        category: 'Ácidos',
        unit: 'Litro',
        quantity: 10,
        value: '450,00'
      }
    ])
    
    // Data atual formatada
    const currentDate = new Date().toLocaleDateString('pt-BR')
    
    // Métodos
    const printReport = () => {
      window.print()
    }
    
    const exportReport = (format) => {
      // Lógica para exportar o relatório no formato especificado
      console.log(`Exportando relatório como ${format.toUpperCase()}`)
    }
    
    return {
      zoomLevel,
      zoomOptions,
      reportData,
      currentDate,
      printReport,
      exportReport
    }
  }
}
</script>

<style scoped>
@media print {
  body * {
    visibility: hidden;
  }
  
  .p-6, .p-6 * {
    visibility: visible;
  }
  
  .p-6 {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    padding: 0;
  }
}
</style>