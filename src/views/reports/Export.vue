<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Exportação de Dados</h1>
      <Button variant="primary" @click="openExportModal">
        <Icon name="download" class="mr-2" />
        Exportar Dados
      </Button>
    </div>
    
    <!-- Opções de exportação -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Opções de Exportação</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Formato *</label>
          <Select v-model="exportOptions.format" :options="formats" placeholder="Selecione um formato" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Período</label>
          <div class="flex space-x-2">
            <Input v-model="exportOptions.startDate" type="date" placeholder="Data inicial" />
            <Input v-model="exportOptions.endDate" type="date" placeholder="Data final" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Dados a Exportar</label>
          <Select 
            v-model="exportOptions.dataType" 
            :options="dataTypes" 
            placeholder="Selecione o tipo de dados"
          />
        </div>
      </div>
      <div class="px-4 pb-4">
        <Button variant="outline" @click="applyExportOptions">Aplicar Opções</Button>
      </div>
    </Card>
    
    <!-- Visualização dos dados a serem exportados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Visualização dos Dados</h2>
      </template>
      <div class="overflow-x-auto p-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data de Validade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in previewData" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ item.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(item.expiryDate) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getStatusVariant(item.status)">
                  {{ item.status }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Paginação -->
      <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Mostrando <span class="font-medium">1</span> a <span class="font-medium">10</span> de <span class="font-medium">97</span> resultados
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm" disabled>Anterior</Button>
          <Button variant="outline" size="sm">Próximo</Button>
        </div>
      </div>
    </Card>
    
    <!-- Modal de exportação -->
    <Modal :visible="showExportModal" @close="closeExportModal">
      <template #header>
        <h3 class="text-lg font-medium">Exportar Dados</h3>
      </template>
      
      <div class="p-4">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Formato de Exportação</label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Button 
              v-for="format in formats" 
              :key="format.value"
              :variant="exportOptions.format === format.value ? 'primary' : 'outline'"
              @click="selectFormat(format.value)"
              class="flex flex-col items-center justify-center p-4"
            >
              <Icon :name="getFormatIcon(format.value)" class="text-2xl mb-2" />
              <span>{{ format.label }}</span>
            </Button>
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Opções Adicionais</label>
          <div class="space-y-2">
            <label class="flex items-center">
              <input 
                v-model="exportOptions.includeHeaders" 
                type="checkbox" 
                class="rounded border-gray-300 text-primary shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50"
              />
              <span class="ml-2 text-sm text-gray-700">Incluir cabeçalhos</span>
            </label>
            <label class="flex items-center">
              <input 
                v-model="exportOptions.includeTimestamp" 
                type="checkbox" 
                class="rounded border-gray-300 text-primary shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50"
              />
              <span class="ml-2 text-sm text-gray-700">Incluir data/hora da exportação</span>
            </label>
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Destino da Exportação</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Button 
              :variant="exportOptions.destination === 'download' ? 'primary' : 'outline'"
              @click="selectDestination('download')"
              class="flex flex-col items-center justify-center p-4"
            >
              <Icon name="download" class="text-2xl mb-2" />
              <span>Download</span>
            </Button>
            <Button 
              :variant="exportOptions.destination === 'email' ? 'primary' : 'outline'"
              @click="selectDestination('email')"
              class="flex flex-col items-center justify-center p-4"
              disabled
            >
              <Icon name="envelope" class="text-2xl mb-2" />
              <span>Email (Em breve)</span>
            </Button>
          </div>
        </div>
        
        <div v-if="exportOptions.destination === 'email'" class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Email de Destino</label>
          <Input v-model="exportOptions.email" type="email" placeholder="Digite o email de destino" />
        </div>
      </div>
      
      <template #footer>
        <Button variant="outline" @click="closeExportModal">Cancelar</Button>
        <Button variant="primary" @click="exportData">Exportar</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'DataExport',
  components: {
    Card,
    Button,
    Input,
    Select,
    Modal,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const showExportModal = ref(false)
    
    // Opções de exportação
    const exportOptions = ref({
      format: 'pdf',
      startDate: '',
      endDate: '',
      dataType: 'all',
      includeHeaders: true,
      includeTimestamp: true,
      destination: 'download',
      email: ''
    })
    
    // Formatos disponíveis
    const formats = ref([
      { value: 'pdf', label: 'PDF' },
      { value: 'excel', label: 'Excel' },
      { value: 'csv', label: 'CSV' }
    ])
    
    // Tipos de dados
    const dataTypes = ref([
      { value: 'all', label: 'Todos os Dados' },
      { value: 'reagents', label: 'Reagentes' },
      { value: 'stock-lots', label: 'Lotes de Estoque' },
      { value: 'movements', label: 'Movimentações' },
      { value: 'requisitions', label: 'Requisições' }
    ])
    
    // Dados de visualização (fictícios para demonstração)
    const previewData = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro',
        expiryDate: '2024-12-31',
        status: 'Ativo'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro',
        expiryDate: '2024-06-30',
        status: 'Expirando'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma',
        expiryDate: '2025-03-15',
        status: 'Ativo'
      }
    ])
    
    // Métodos
    const openExportModal = () => {
      showExportModal.value = true
    }
    
    const closeExportModal = () => {
      showExportModal.value = false
    }
    
    const selectFormat = (format) => {
      exportOptions.value.format = format
    }
    
    const selectDestination = (destination) => {
      exportOptions.value.destination = destination
    }
    
    const applyExportOptions = () => {
      // Lógica para aplicar as opções de exportação
      console.log('Aplicando opções de exportação:', exportOptions.value)
    }
    
    const exportData = () => {
      // Lógica para exportar os dados no formato selecionado
      console.log('Exportando dados no formato:', exportOptions.value.format)
      closeExportModal()
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Ativo': return 'success'
        case 'Expirando': return 'warning'
        case 'Expirado': return 'error'
        default: return 'default'
      }
    }
    
    const getFormatIcon = (format) => {
      switch (format) {
        case 'pdf': return 'file-pdf'
        case 'excel': return 'file-excel'
        case 'csv': return 'file-csv'
        default: return 'file'
      }
    }
    
    return {
      showExportModal,
      exportOptions,
      formats,
      dataTypes,
      previewData,
      openExportModal,
      closeExportModal,
      selectFormat,
      selectDestination,
      applyExportOptions,
      exportData,
      formatDate,
      getStatusVariant,
      getFormatIcon
    }
  }
}
</script>