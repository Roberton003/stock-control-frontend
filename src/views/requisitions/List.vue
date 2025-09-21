<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Requisições</h1>
      <Button variant="primary" @click="openCreateModal">
        <Icon name="plus" class="mr-2" />
        Nova Requisição
      </Button>
    </div>
    
    <!-- Filtros -->
    <Card class="mb-6 bg-white">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <Select v-model="filters.status" :options="statusOptions" placeholder="Selecione um status" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Solicitante</label>
          <Input v-model="filters.requester" placeholder="Nome do solicitante" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Período</label>
          <div class="flex space-x-2">
            <Input v-model="filters.startDate" type="date" placeholder="Data inicial" />
            <Input v-model="filters.endDate" type="date" placeholder="Data final" />
          </div>
        </div>
        <div class="flex items-end">
          <Button variant="outline" @click="applyFilters">Aplicar Filtros</Button>
        </div>
      </div>
    </Card>
    
    <!-- Lista de requisições -->
    <Card class="bg-white">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Solicitante</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Itens</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="request in requests" :key="request.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ request.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ request.requester }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(request.date) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ request.items.length }} itens</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getStatusVariant(request.status)">
                  {{ request.status }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="viewDetails(request.id)">
                  <Icon name="eye" />
                </Button>
                <Button v-if="request.status === 'Pendente'" variant="outline" size="sm" class="mr-2" @click="approveRequest(request.id)">
                  <Icon name="check" />
                </Button>
                <Button v-if="request.status === 'Pendente'" variant="outline" size="sm" @click="rejectRequest(request.id)">
                  <Icon name="times" />
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
    
    <!-- Modal de criação -->
    <Modal :visible="showCreateModal" @close="closeCreateModal">
      <template #header>
        <h3 class="text-lg font-medium">Nova Requisição</h3>
      </template>
      
      <form @submit.prevent="createRequest">
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Solicitante *</label>
            <Input v-model="createForm.requester" placeholder="Nome do solicitante" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Itens da Requisição</label>
            <div class="space-y-4">
              <div v-for="(item, index) in createForm.items" :key="index" class="flex space-x-2">
                <Select v-model="item.reagent" :options="reagents" placeholder="Selecione um reagente" />
                <Input v-model="item.quantity" type="number" placeholder="Quantidade" />
                <Button variant="outline" @click="removeItem(index)">
                  <Icon name="trash" />
                </Button>
              </div>
              <Button variant="outline" @click="addItem">
                <Icon name="plus" class="mr-2" />
                Adicionar Item
              </Button>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea 
              v-model="createForm.notes" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Observações sobre a requisição"
            ></textarea>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeCreateModal">Cancelar</Button>
        <Button variant="primary" @click="createRequest">Criar Requisição</Button>
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
  name: 'RequisitionsList',
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
    const showCreateModal = ref(false)
    
    // Filtros
    const filters = ref({
      status: '',
      requester: '',
      startDate: '',
      endDate: ''
    })
    
    // Dados fictícios para demonstração
    const requests = ref([
      {
        id: 1,
        requester: 'João Silva',
        date: '2023-09-15T14:30:00',
        status: 'Aprovada',
        items: [
          { reagent: 'Ácido Clorídrico', quantity: 5 },
          { reagent: 'Etanol 96%', quantity: 10 }
        ]
      },
      {
        id: 2,
        requester: 'Maria Oliveira',
        date: '2023-09-14T09:15:00',
        status: 'Pendente',
        items: [
          { reagent: 'Sulfato de Cobre', quantity: 2 }
        ]
      },
      {
        id: 3,
        requester: 'Pedro Santos',
        date: '2023-09-13T11:45:00',
        status: 'Rejeitada',
        items: [
          { reagent: 'Ácido Nítrico', quantity: 3 },
          { reagent: 'Hidróxido de Sódio', quantity: 1 }
        ]
      }
    ])
    
    const statusOptions = ref([
      { value: 'all', label: 'Todos' },
      { value: 'pending', label: 'Pendente' },
      { value: 'approved', label: 'Aprovada' },
      { value: 'rejected', label: 'Rejeitada' }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' },
      { value: 4, label: 'Ácido Nítrico' },
      { value: 5, label: 'Hidróxido de Sódio' }
    ])
    
    // Formulário de criação
    const createForm = ref({
      requester: '',
      items: [
        { reagent: '', quantity: 0 }
      ],
      notes: ''
    })
    
    // Métodos
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Aprovada': return 'success'
        case 'Pendente': return 'warning'
        case 'Rejeitada': return 'error'
        default: return 'default'
      }
    }
    
    const openCreateModal = () => {
      showCreateModal.value = true
    }
    
    const closeCreateModal = () => {
      showCreateModal.value = false
      resetCreateForm()
    }
    
    const resetCreateForm = () => {
      createForm.value = {
        requester: '',
        items: [
          { reagent: '', quantity: 0 }
        ],
        notes: ''
      }
    }
    
    const addItem = () => {
      createForm.value.items.push({ reagent: '', quantity: 0 })
    }
    
    const removeItem = (index) => {
      if (createForm.value.items.length > 1) {
        createForm.value.items.splice(index, 1)
      }
    }
    
    const createRequest = () => {
      // Lógica para criar a requisição
      console.log('Criando requisição:', createForm.value)
      closeCreateModal()
    }
    
    const viewDetails = (id) => {
      // Lógica para visualizar detalhes
      console.log('Visualizando detalhes da requisição:', id)
    }
    
    const approveRequest = (id) => {
      // Lógica para aprovar requisição
      console.log('Aprovando requisição:', id)
    }
    
    const rejectRequest = (id) => {
      // Lógica para rejeitar requisição
      console.log('Rejeitando requisição:', id)
    }
    
    const applyFilters = () => {
      // Lógica para aplicar filtros
      console.log('Aplicando filtros:', filters.value)
    }
    
    return {
      showCreateModal,
      filters,
      requests,
      statusOptions,
      reagents,
      createForm,
      formatDate,
      getStatusVariant,
      openCreateModal,
      closeCreateModal,
      addItem,
      removeItem,
      createRequest,
      viewDetails,
      approveRequest,
      rejectRequest,
      applyFilters
    }
  }
}
</script>