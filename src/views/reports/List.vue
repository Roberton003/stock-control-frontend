<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Relatórios</h1>
      <Button variant="primary" @click="generateReport">
        <Icon name="plus" class="mr-2" />
        Gerar Relatório
      </Button>
    </div>
    
    <!-- Filtros -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Filtros</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Relatório *</label>
          <Select v-model="filters.reportType" :options="reportTypes" placeholder="Selecione um tipo" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Período</label>
          <div class="flex space-x-2">
            <Input v-model="filters.startDate" type="date" placeholder="Data inicial" />
            <Input v-model="filters.endDate" type="date" placeholder="Data final" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Reagente</label>
          <Select v-model="filters.reagent" :options="reagents" placeholder="Selecione um reagente" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Usuário</label>
          <Input v-model="filters.user" placeholder="Nome do usuário" />
        </div>
      </div>
      <div class="px-4 pb-4">
        <Button variant="outline" @click="applyFilters">Aplicar Filtros</Button>
      </div>
    </Card>
    
    <!-- Lista de relatórios gerados -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Relatórios Gerados</h2>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data de Geração</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Período</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gerado Por</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="report in reports" :key="report.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ report.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ report.type }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(report.generationDate) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ report.period }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ report.generatedBy }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getStatusVariant(report.status)">
                  {{ report.status }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="viewReport(report.id)">
                  <Icon name="eye" />
                </Button>
                <Button variant="outline" size="sm" class="mr-2" @click="downloadReport(report.id)">
                  <Icon name="download" />
                </Button>
                <Button variant="outline" size="sm" @click="deleteReport(report.id)">
                  <Icon name="trash" />
                </Button>
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
    
    <!-- Modal de geração de relatório -->
    <Modal :visible="showGenerateModal" @close="closeGenerateModal">
      <template #header>
        <h3 class="text-lg font-medium">Gerar Novo Relatório</h3>
      </template>
      
      <form @submit.prevent="createReport">
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Relatório *</label>
            <Select v-model="generateForm.reportType" :options="reportTypes" placeholder="Selecione um tipo" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Período *</label>
            <div class="flex space-x-2">
              <Input v-model="generateForm.startDate" type="date" placeholder="Data inicial" />
              <Input v-model="generateForm.endDate" type="date" placeholder="Data final" />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Formato *</label>
            <Select v-model="generateForm.format" :options="formats" placeholder="Selecione um formato" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea 
              v-model="generateForm.notes" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Observações sobre o relatório"
            ></textarea>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeGenerateModal">Cancelar</Button>
        <Button variant="primary" @click="createReport">Gerar Relatório</Button>
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
  name: 'ReportsList',
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
    const showGenerateModal = ref(false)
    
    // Filtros
    const filters = ref({
      reportType: '',
      startDate: '',
      endDate: '',
      reagent: '',
      user: ''
    })
    
    // Dados fictícios para demonstração
    const reports = ref([
      {
        id: 1,
        type: 'Consumo de Reagentes',
        generationDate: '2023-09-15T14:30:00',
        period: '01/09/2023 - 15/09/2023',
        generatedBy: 'João Silva',
        status: 'Concluído'
      },
      {
        id: 2,
        type: 'Validade de Lotes',
        generationDate: '2023-09-10T09:15:00',
        period: '01/09/2023 - 10/09/2023',
        generatedBy: 'Maria Oliveira',
        status: 'Em Andamento'
      },
      {
        id: 3,
        type: 'Estoque Atual',
        generationDate: '2023-09-05T11:45:00',
        period: '05/09/2023',
        generatedBy: 'Pedro Santos',
        status: 'Falhou'
      }
    ])
    
    const reportTypes = ref([
      { value: 'consumption', label: 'Consumo de Reagentes' },
      { value: 'expiry', label: 'Validade de Lotes' },
      { value: 'stock', label: 'Estoque Atual' },
      { value: 'movements', label: 'Movimentações' },
      { value: 'requisitions', label: 'Requisições' }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' }
    ])
    
    const formats = ref([
      { value: 'pdf', label: 'PDF' },
      { value: 'excel', label: 'Excel' },
      { value: 'csv', label: 'CSV' }
    ])
    
    // Formulário de geração
    const generateForm = ref({
      reportType: '',
      startDate: '',
      endDate: '',
      format: 'pdf',
      notes: ''
    })
    
    // Métodos
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Concluído': return 'success'
        case 'Em Andamento': return 'warning'
        case 'Falhou': return 'error'
        default: return 'default'
      }
    }
    
    const generateReport = () => {
      showGenerateModal.value = true
    }
    
    const closeGenerateModal = () => {
      showGenerateModal.value = false
      resetGenerateForm()
    }
    
    const resetGenerateForm = () => {
      generateForm.value = {
        reportType: '',
        startDate: '',
        endDate: '',
        format: 'pdf',
        notes: ''
      }
    }
    
    const createReport = () => {
      // Lógica para criar o relatório
      console.log('Gerando relatório:', generateForm.value)
      closeGenerateModal()
    }
    
    const applyFilters = () => {
      // Lógica para aplicar filtros
      console.log('Aplicando filtros:', filters.value)
    }
    
    const viewReport = (id) => {
      // Lógica para visualizar relatório
      console.log('Visualizando relatório:', id)
    }
    
    const downloadReport = (id) => {
      // Lógica para baixar relatório
      console.log('Baixando relatório:', id)
    }
    
    const deleteReport = (id) => {
      // Lógica para excluir relatório
      console.log('Excluindo relatório:', id)
    }
    
    return {
      showGenerateModal,
      filters,
      reports,
      reportTypes,
      reagents,
      formats,
      generateForm,
      formatDate,
      getStatusVariant,
      generateReport,
      closeGenerateModal,
      createReport,
      applyFilters,
      viewReport,
      downloadReport,
      deleteReport
    }
  }
}
</script>