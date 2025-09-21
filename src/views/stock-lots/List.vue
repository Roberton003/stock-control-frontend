<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Lotes de Estoque</h1>
      <Button variant="primary" @click="openCreateModal">
        <Icon name="plus" class="mr-2" />
        Novo Lote
      </Button>
    </div>
    
    <!-- Filtros -->
    <Card class="mb-6 bg-white">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Reagente</label>
          <Select v-model="filters.reagent" :options="reagents" placeholder="Selecione um reagente" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fornecedor</label>
          <Select v-model="filters.supplier" :options="suppliers" placeholder="Selecione um fornecedor" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
          <Select v-model="filters.location" :options="locations" placeholder="Selecione uma localização" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Validade</label>
          <Select v-model="filters.expiry" :options="expiryOptions" placeholder="Período de validade" />
        </div>
      </div>
      <div class="px-4 pb-4">
        <Button variant="outline" @click="clearFilters">Limpar Filtros</Button>
      </div>
    </Card>
    
    <!-- Lista de lotes -->
    <Card class="bg-white">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reagente</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lote</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="lot in lots" :key="lot.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ lot.reagent.name }}</div>
                <div class="text-sm text-gray-500">{{ lot.reagent.category }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ lot.lot_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ lot.quantity }} {{ lot.reagent.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getExpiryVariant(lot.expiry_date)">
                  {{ formatDate(lot.expiry_date) }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getStatusVariant(lot.status)">
                  {{ lot.status }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="viewDetails(lot.id)">
                  <Icon name="eye" />
                </Button>
                <Button variant="outline" size="sm" class="mr-2" @click="editLot(lot.id)">
                  <Icon name="edit" />
                </Button>
                <Button variant="outline" size="sm" @click="deleteLot(lot.id)">
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
    
    <!-- Modal de criação/edição -->
    <Modal :visible="showModal" @close="closeModal">
      <template #header>
        <h3 class="text-lg font-medium">
          {{ editingLot ? 'Editar Lote' : 'Novo Lote' }}
        </h3>
      </template>
      
      <form @submit.prevent="saveLot">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Reagente *</label>
            <Select v-model="form.reagent" :options="reagents" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Número do Lote *</label>
            <Input v-model="form.lot_number" placeholder="Número do lote" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade *</label>
            <Input v-model="form.quantity" type="number" placeholder="Quantidade" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unidade *</label>
            <Input v-model="form.unit" placeholder="Unidade" disabled />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Validade *</label>
            <Input v-model="form.expiry_date" type="date" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fornecedor</label>
            <Select v-model="form.supplier" :options="suppliers" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
            <Select v-model="form.location" :options="locations" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Preço de Compra</label>
            <Input v-model="form.purchase_price" type="number" step="0.01" placeholder="Preço de compra" />
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeModal">Cancelar</Button>
        <Button variant="primary" @click="saveLot">Salvar</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'StockLotsList',
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
    const showModal = ref(false)
    const editingLot = ref(null)
    
    // Filtros
    const filters = ref({
      reagent: '',
      supplier: '',
      location: '',
      expiry: ''
    })
    
    // Dados fictícios para demonstração
    const lots = ref([
      {
        id: 1,
        reagent: {
          id: 1,
          name: 'Ácido Clorídrico',
          category: 'Ácidos',
          unit: 'Litro'
        },
        lot_number: 'AC12345',
        quantity: 25,
        expiry_date: '2024-12-31',
        status: 'Ativo',
        supplier: 'LabQuímica Ltda',
        location: 'Armário A1'
      },
      {
        id: 2,
        reagent: {
          id: 2,
          name: 'Etanol 96%',
          category: 'Álcoois',
          unit: 'Litro'
        },
        lot_number: 'ET67890',
        quantity: 8,
        expiry_date: '2024-06-30',
        status: 'Expirando',
        supplier: 'Química Brasil',
        location: 'Armário B2'
      },
      {
        id: 3,
        reagent: {
          id: 3,
          name: 'Sulfato de Cobre',
          category: 'Sais',
          unit: 'Kilograma'
        },
        lot_number: 'SC54321',
        quantity: 12,
        expiry_date: '2025-03-15',
        status: 'Ativo',
        supplier: 'Laboratórios ABC',
        location: 'Prateleira C3'
      }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' }
    ])
    
    const suppliers = ref([
      { value: 1, label: 'LabQuímica Ltda' },
      { value: 2, label: 'Química Brasil' },
      { value: 3, label: 'Laboratórios ABC' }
    ])
    
    const locations = ref([
      { value: 1, label: 'Armário A1' },
      { value: 2, label: 'Armário B2' },
      { value: 3, label: 'Prateleira C3' }
    ])
    
    const expiryOptions = ref([
      { value: 'all', label: 'Todos' },
      { value: 'active', label: 'Ativos' },
      { value: 'expiring', label: 'Expirando (< 30 dias)' },
      { value: 'expired', label: 'Expirados' }
    ])
    
    // Formulário
    const form = ref({
      reagent: '',
      lot_number: '',
      quantity: 0,
      unit: '',
      expiry_date: '',
      supplier: '',
      location: '',
      purchase_price: 0
    })
    
    // Watch para atualizar unidade quando reagente mudar
    watch(() => form.value.reagent, (newReagentId) => {
      if (newReagentId) {
        const reagent = reagents.value.find(r => r.value === newReagentId)
        if (reagent) {
          // Na prática, isso viria da API
          form.value.unit = 'Litro' // Valor padrão para exemplo
        }
      }
    })
    
    // Métodos
    const getExpiryVariant = (expiryDate) => {
      const today = new Date()
      const expiry = new Date(expiryDate)
      const diffTime = expiry - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) return 'error'
      if (diffDays <= 30) return 'warning'
      return 'success'
    }
    
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Ativo': return 'success'
        case 'Expirando': return 'warning'
        case 'Expirado': return 'error'
        default: return 'default'
      }
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const openCreateModal = () => {
      editingLot.value = null
      form.value = {
        reagent: '',
        lot_number: '',
        quantity: 0,
        unit: '',
        expiry_date: '',
        supplier: '',
        location: '',
        purchase_price: 0
      }
      showModal.value = true
    }
    
    const closeModal = () => {
      showModal.value = false
    }
    
    const saveLot = () => {
      // Lógica para salvar o lote
      console.log('Salvando lote:', form.value)
      closeModal()
    }
    
    const viewDetails = (id) => {
      // Lógica para visualizar detalhes
      console.log('Visualizando detalhes do lote:', id)
    }
    
    const editLot = (id) => {
      // Lógica para editar lote
      const lot = lots.value.find(l => l.id === id)
      if (lot) {
        editingLot.value = lot
        form.value = { ...lot }
        showModal.value = true
      }
    }
    
    const deleteLot = (id) => {
      // Lógica para excluir lote
      console.log('Excluindo lote:', id)
    }
    
    const clearFilters = () => {
      filters.value = {
        reagent: '',
        supplier: '',
        location: '',
        expiry: ''
      }
    }
    
    return {
      showModal,
      editingLot,
      filters,
      lots,
      reagents,
      suppliers,
      locations,
      expiryOptions,
      form,
      getExpiryVariant,
      getStatusVariant,
      formatDate,
      openCreateModal,
      closeModal,
      saveLot,
      viewDetails,
      editLot,
      deleteLot,
      clearFilters
    }
  }
}
</script>