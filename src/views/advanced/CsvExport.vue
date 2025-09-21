<template>
  <div class=\"p-6\">
    <div class=\"flex justify-between items-center mb-6\">
      <h1 class=\"text-2xl font-bold\">Exportação para CSV</h1>
      <Button variant=\"primary\" @click=\"toggleCsvExport\">
        <Icon :name=\"csvExportEnabled ? 'pause' : 'play'\" class=\"mr-2\" />
        {{ csvExportEnabled ? 'Desativar' : 'Ativar' }} Exportação CSV
      </Button>
    </div>
    
    <!-- Configurações da exportação CSV -->
    <Card class=\"mb-6 bg-white\">
      <template #header>
        <h2 class=\"text-lg font-semibold\">Configurações da Exportação CSV</h2>
      </template>
      <div class=\"grid grid-cols-1 md:grid-cols-3 gap-6 p-4\">
        <div>
          <label class=\"block text-sm font-medium text-gray-700 mb-1\">Delimitador</label>
          <Select 
            v-model=\"csvSettings.delimiter\" 
            :options=\"delimiterOptions\" 
            placeholder=\"Selecione o delimitador\" 
            @change=\"updateCsvSettings\"
          />
        </div>
        <div>
          <label class=\"block text-sm font-medium text-gray-700 mb-1\">Codificação</label>
          <Select 
            v-model=\"csvSettings.encoding\" 
            :options=\"encodingOptions\" 
            placeholder=\"Selecione a codificação\" 
            @change=\"updateCsvSettings\"
          />
        </div>
        <div>
          <label class=\"block text-sm font-medium text-gray-700 mb-1\">Incluir Cabeçalhos</label>
          <Toggle 
            v-model=\"csvSettings.includeHeaders\" 
            label=\"Incluir linha de cabeçalhos no CSV\" 
            @change=\"updateCsvSettings\"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de exportação CSV -->
    <Card class=\"mb-6 bg-white\">
      <template #header>
        <div class=\"flex justify-between items-center\">
          <h2 class=\"text-lg font-semibold\">Exemplo de Exportação CSV</h2>
          <Badge :variant=\"csvExportEnabled ? 'success' : 'default'\">
            {{ csvExportEnabled ? 'Ativada' : 'Desativada' }}
          </Badge>
        </div>
      </template>
      
      <div class=\"p-4\">
        <div class=\"grid grid-cols-1 md:grid-cols-2 gap-6\">
          <div>
            <h3 class=\"text-md font-medium text-gray-900 mb-2\">Dados de Exemplo</h3>
            <div class=\"overflow-x-auto\">
              <table class=\"min-w-full divide-y divide-gray-200\">
                <thead class=\"bg-gray-50\">
                  <tr>
                    <th scope=\"col\" class=\"px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider\">Nome</th>
                    <th scope=\"col\" class=\"px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider\">Categoria</th>
                    <th scope=\"col\" class=\"px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider\">Quantidade</th>
                    <th scope=\"col\" class=\"px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider\">Unidade</th>
                  </tr>
                </thead>
                <tbody class=\"bg-white divide-y divide-gray-200\">
                  <tr v-for=\"item in sampleData\" :key=\"item.id\" class=\"hover:bg-gray-50\">
                    <td class=\"px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900\">{{ item.name }}</td>
                    <td class=\"px-6 py-4 whitespace-nowrap text-sm text-gray-500\">{{ item.category }}</td>
                    <td class=\"px-6 py-4 whitespace-nowrap text-sm text-gray-500\">{{ item.quantity }}</td>
                    <td class=\"px-6 py-4 whitespace-nowrap text-sm text-gray-500\">{{ item.unit }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div>
            <h3 class=\"text-md font-medium text-gray-900 mb-2\">CSV Gerado</h3>
            <pre v-if=\"generatedCsv\" class=\"bg-gray-100 border border-dashed border-gray-300 rounded p-4 text-sm overflow-x-auto max-h-64\">
{{ generatedCsv }}
            </pre>
            <div v-else class=\"bg-gray-100 border border-dashed border-gray-300 rounded p-4 text-sm text-gray-500\">
              Nenhum CSV gerado ainda. Clique em \"Gerar CSV\" para criar um exemplo.
            </div>
            
            <div class=\"mt-4 flex space-x-3\">
              <Button 
                variant=\"primary\" 
                @click=\"generateSampleCsv\" 
                :disabled=\"!csvExportEnabled\"
              >
                <Icon name=\"file-csv\" class=\"mr-2\" />
                Gerar CSV
              </Button>
              <Button 
                variant=\"outline\" 
                @click=\"downloadSampleCsv\" 
                :disabled=\"!generatedCsv || !csvExportEnabled\"
              >
                <Icon name=\"download\" class=\"mr-2\" />
                Download CSV
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Opções de exportação avançadas -->
    <Card class=\"mb-6 bg-white\">
      <template #header>
        <h2 class=\"text-lg font-semibold\">Opções de Exportação Avançadas</h2>
      </template>
      
      <div class=\"p-4\">
        <div class=\"grid grid-cols-1 md:grid-cols-2 gap-6\">
          <div>
            <h3 class=\"text-md font-medium text-gray-900 mb-2\">Seleção de Colunas</h3>
            <div class=\"space-y-2\">
              <Checkbox 
                v-for=\"column in csvColumns\" 
                :key=\"column.value\"
                v-model=\"column.selected\"
                :label=\"column.label\"
                @change=\"updateColumnSelection\"
              />
            </div>
          </div>
          
          <div>
            <h3 class=\"text-md font-medium text-gray-900 mb-2\">Filtros de Exportação</h3>
            <div class=\"space-y-4\">
              <div>
                <label class=\"block text-sm font-medium text-gray-700 mb-1\">Categoria</label>
                <Select 
                  v-model=\"exportFilters.category\" 
                  :options=\"categories\" 
                  placeholder=\"Selecione uma categoria\"
                  @change=\"updateExportFilters\"
                />
              </div>
              
              <div>
                <label class=\"block text-sm font-medium text-gray-700 mb-1\">Período</label>
                <div class=\"flex space-x-2\">
                  <Input 
                    v-model=\"exportFilters.startDate\" 
                    type=\"date\" 
                    placeholder=\"Data inicial\"
                    @change=\"updateExportFilters\"
                  />
                  <Input 
                    v-model=\"exportFilters.endDate\" 
                    type=\"date\" 
                    placeholder=\"Data final\"
                    @change=\"updateExportFilters\"
                  />
                </div>
              </div>
              
              <div>
                <label class=\"block text-sm font-medium text-gray-700 mb-1\">Quantidade Mínima</label>
                <Input 
                  v-model=\"exportFilters.minQuantity\" 
                  type=\"number\" 
                  placeholder=\"Quantidade mínima\"
                  @change=\"updateExportFilters\"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div class=\"mt-6 flex justify-end space-x-3\">
          <Button variant=\"outline\" @click=\"resetExportFilters\">
            <Icon name=\"undo\" class=\"mr-2\" />
            Limpar Filtros
          </Button>
          <Button 
            variant=\"primary\" 
            @click=\"exportFilteredData\" 
            :disabled=\"!csvExportEnabled\"
          >
            <Icon name=\"file-export\" class=\"mr-2\" />
            Exportar Dados Filtrados
          </Button>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre exportação CSV -->
    <Card class=\"bg-white\">
      <template #header>
        <h2 class=\"text-lg font-semibold\">Informações sobre Exportação CSV</h2>
      </template>
      <div class=\"p-4\">
        <div class=\"grid grid-cols-1 md:grid-cols-2 gap-6\">
          <div>
            <h3 class=\"text-md font-medium text-gray-900 mb-2\">Benefícios da Exportação CSV</h3>
            <ul class=\"list-disc pl-5 space-y-1 text-sm text-gray-700\">
              <li>Permite análise de dados em softwares de planilha (Excel, Google Sheets, etc.)</li>
              <li>Facilita a criação de relatórios personalizados</li>
              <li>Permite backup dos dados em formato aberto</li>
              <li>Compatível com a maioria dos sistemas de análise de dados</li>
              <li>Fácil de compartilhar e integrar com outros sistemas</li>
            </ul>
          </div>
          <div>
            <h3 class=\"text-md font-medium text-gray-900 mb-2\">Configurações Atuais</h3>
            <ul class=\"space-y-2 text-sm text-gray-700\">
              <li class=\"flex justify-between\">
                <span class=\"font-medium\">Exportação CSV:</span>
                <span>{{ csvExportEnabled ? 'Ativada' : 'Desativada' }}</span>
              </li>
              <li class=\"flex justify-between\">
                <span class=\"font-medium\">Delimitador:</span>
                <span>{{ csvSettings.delimiter }}</span>
              </li>
              <li class=\"flex justify-between\">
                <span class=\"font-medium\">Codificação:</span>
                <span>{{ csvSettings.encoding }}</span>
              </li>
              <li class=\"flex justify-between\">
                <span class=\"font-medium\">Incluir Cabeçalhos:</span>
                <span>{{ csvSettings.includeHeaders ? 'Sim' : 'Não' }}</span>
              </li>
              <li class=\"flex justify-between\">
                <span class=\"font-medium\">Colunas Selecionadas:</span>
                <span>{{ selectedColumns.length }} de {{ csvColumns.length }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Toggle from '@/components/ui/Toggle.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'CsvExport',
  components: {
    Card,
    Button,
    Input,
    Select,
    Toggle,
    Checkbox,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const csvExportEnabled = ref(true)
    const generatedCsv = ref('')
    
    // Configurações da exportação CSV
    const csvSettings = ref({
      delimiter: ',',
      encoding: 'UTF-8',
      includeHeaders: true
    })
    
    // Filtros de exportação
    const exportFilters = ref({
      category: '',
      startDate: '',
      endDate: '',
      minQuantity: 0
    })
    
    // Dados fictícios para demonstração
    const sampleData = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma'
      },
      {
        id: 4,
        name: 'Ácido Nítrico',
        category: 'Ácidos',
        quantity: 15,
        unit: 'Litro'
      },
      {
        id: 5,
        name: 'Hidróxido de Sódio',
        category: 'Bases',
        quantity: 8,
        unit: 'Kilograma'
      }
    ])
    
    // Colunas disponíveis para exportação
    const csvColumns = ref([
      { value: 'id', label: 'ID', selected: true },
      { value: 'name', label: 'Nome', selected: true },
      { value: 'category', label: 'Categoria', selected: true },
      { value: 'quantity', label: 'Quantidade', selected: true },
      { value: 'unit', label: 'Unidade', selected: true }
    ])
    
    // Opções para seletores
    const delimiterOptions = ref([
      { value: ',', label: 'Vírgula (,)' },
      { value: ';', label: 'Ponto e vírgula (;)' },
      { value: '\t', label: 'Tabulação (\\t)' }
    ])
    
    const encodingOptions = ref([
      { value: 'UTF-8', label: 'UTF-8' },
      { value: 'ISO-8859-1', label: 'ISO-8859-1 (Latin-1)' },
      { value: 'Windows-1252', label: 'Windows-1252' }
    ])
    
    const categories = ref([
      { value: 'acids', label: 'Ácidos' },
      { value: 'bases', label: 'Bases' },
      { value: 'salts', label: 'Sais' },
      { value: 'solvents', label: 'Solventes' },
      { value: 'indicators', label: 'Indicadores' }
    ])
    
    // Computed properties
    const selectedColumns = computed(() => {
      return csvColumns.value.filter(column => column.selected)
    })
    
    // Métodos
    const toggleCsvExport = () => {
      csvExportEnabled.value = !csvExportEnabled.value
    }
    
    const updateCsvSettings = () => {
      // Atualizar configurações da exportação CSV
      console.log('Atualizando configurações da exportação CSV:', csvSettings.value)
    }
    
    const updateColumnSelection = () => {
      // Atualizar seleção de colunas
      console.log('Atualizando seleção de colunas:', selectedColumns.value)
    }
    
    const updateExportFilters = () => {
      // Atualizar filtros de exportação
      console.log('Atualizando filtros de exportação:', exportFilters.value)
    }
    
    const resetExportFilters = () => {
      exportFilters.value = {
        category: '',
        startDate: '',
        endDate: '',
        minQuantity: 0
      }
    }
    
    const generateSampleCsv = () => {
      if (!csvExportEnabled.value) return
      
      // Gerar CSV com base nos dados de exemplo e configurações
      const delimiter = csvSettings.value.delimiter
      const includeHeaders = csvSettings.value.includeHeaders
      
      let csvContent = ''
      
      // Adicionar cabeçalhos se necessário
      if (includeHeaders) {
        const headers = selectedColumns.value.map(column => column.label)
        csvContent += headers.join(delimiter) + '\n'
      }
      
      // Adicionar linhas de dados
      sampleData.value.forEach(item => {
        const row = selectedColumns.value.map(column => {
          const value = item[column.value]
          // Se o valor contiver o delimitador, colocá-lo entre aspas
          if (typeof value === 'string' && value.includes(delimiter)) {
            return `\"${value.replace(/\"/g, '\"\"')}\"`
          }
          return value
        })
        csvContent += row.join(delimiter) + '\n'
      })
      
      generatedCsv.value = csvContent
    }
    
    const downloadSampleCsv = () => {
      if (!generatedCsv.value || !csvExportEnabled.value) return
      
      // Criar um Blob com o conteúdo CSV
      const blob = new Blob([generatedCsv.value], { 
        type: `text/csv;charset=${csvSettings.value.encoding}` 
      })
      
      // Criar um link para download
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `dados_exportados_${new Date().toISOString().slice(0, 10)}.csv`
      
      // Simular clique no link para iniciar o download
      document.body.appendChild(link)
      link.click()
      
      // Limpar
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }
    
    const exportFilteredData = () => {
      if (!csvExportEnabled.value) return
      
      // Lógica para exportar dados filtrados
      console.log('Exportando dados filtrados:', {
        filters: exportFilters.value,
        columns: selectedColumns.value,
        settings: csvSettings.value
      })
      
      // Para fins de demonstração, vamos gerar um CSV com os dados filtrados
      generateSampleCsv()
    }
    
    return {
      csvExportEnabled,
      generatedCsv,
      csvSettings,
      exportFilters,
      sampleData,
      csvColumns,
      selectedColumns,
      delimiterOptions,
      encodingOptions,
      categories,
      toggleCsvExport,
      updateCsvSettings,
      updateColumnSelection,
      updateExportFilters,
      resetExportFilters,
      generateSampleCsv,
      downloadSampleCsv,
      exportFilteredData
    }
  }
}
</script>