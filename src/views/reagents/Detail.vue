<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Detalhes do Reagente</h1>
      <Button variant="primary" @click="editReagent">
        <Icon name="edit" class="mr-2" />
        Editar Reagente
      </Button>
    </div>
    
    <!-- Informações gerais -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações Gerais</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="text-sm font-medium text-gray-500">Nome</h3>
          <p class="mt-1 text-sm text-gray-900">Ácido Clorídrico</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Categoria</h3>
          <p class="mt-1 text-sm text-gray-900">Ácidos</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Unidade</h3>
          <p class="mt-1 text-sm text-gray-900">Litro</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Estoque Mínimo</h3>
          <p class="mt-1 text-sm text-gray-900">10 Litros</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Quantidade Atual</h3>
          <p class="mt-1 text-sm text-gray-900">
            <Badge variant="success">25 Litros</Badge>
          </p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Status</h3>
          <p class="mt-1 text-sm text-gray-900">
            <Badge variant="success">Ativo</Badge>
          </p>
        </div>
      </div>
    </Card>
    
    <!-- Descrição -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Descrição</h2>
      </template>
      <p class="text-gray-700">
        O ácido clorídrico é um composto químico constituído por um átomo de hidrogênio e um de cloro. 
        É altamente corrosivo e deve ser manipulado com extremo cuidado, utilizando equipamentos de 
        proteção individual adequados.
      </p>
    </Card>
    
    <!-- Lotes associados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Lotes Associados</h2>
          <Button variant="outline" @click="addLot">
            <Icon name="plus" class="mr-2" />
            Adicionar Lote
          </Button>
        </div>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lote</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="lot in lots" :key="lot.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ lot.number }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ lot.quantity }} {{ lot.unit }}</td>
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
                <Button variant="secondary" size="sm" class="mr-2" @click="viewLotDetails(lot.id)">
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
    </Card>
    
    <!-- Histórico de movimentações -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Histórico de Movimentações</h2>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuário</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Observações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="movement in movements" :key="movement.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(movement.date) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="movement.type === 'entry' ? 'success' : 'error'">
                  {{ movement.type === 'entry' ? 'Entrada' : 'Saída' }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ movement.quantity }} {{ movement.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ movement.user }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ movement.notes }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
    
    <!-- Modal de edição -->
    <Modal :visible="showEditModal" @close="closeEditModal">
      <template #header>
        <h3 class="text-lg font-medium">Editar Reagente</h3>
      </template>
      
      <form @submit.prevent="saveReagent">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
            <Input v-model="editForm.name" placeholder="Nome do reagente" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Categoria *</label>
            <Select v-model="editForm.category" :options="categories" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unidade *</label>
            <Select v-model="editForm.unit" :options="units" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Estoque Mínimo *</label>
            <Input v-model="editForm.min_stock" type="number" placeholder="Quantidade mínima" />
          </div>
          
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea 
              v-model="editForm.description" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Descrição detalhada do reagente"
            ></textarea>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeEditModal">Cancelar</Button>
        <Button variant="primary" @click="saveReagent">Salvar</Button>
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
  name: 'ReagentDetail',
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
    const showEditModal = ref(false)
    
    // Dados fictícios para demonstração
    const lots = ref([
      {
        id: 1,
        number: 'AC12345',
        quantity: 15,
        unit: 'Litro',
        expiry_date: '2024-12-31',
        status: 'Ativo'
      },
      {
        id: 2,
        number: 'AC67890',
        quantity: 10,
        unit: 'Litro',
        expiry_date: '2025-06-30',
        status: 'Ativo'
      }
    ])
    
    const movements = ref([
      {
        id: 1,
        date: '2023-09-15T14:30:00',
        type: 'entry',
        quantity: 20,
        unit: 'Litro',
        user: 'João Silva',
        notes: 'Compra de estoque'
      },
      {
        id: 2,
        date: '2023-09-10T09:15:00',
        type: 'exit',
        quantity: 5,
        unit: 'Litro',
        user: 'Maria Oliveira',
        notes: 'Utilização em experimento'
      },
      {
        id: 3,
        date: '2023-09-01T11:45:00',
        type: 'entry',
        quantity: 10,
        unit: 'Litro',
        user: 'Pedro Santos',
        notes: 'Recebimento de fornecedor'
      }
    ])
    
    const categories = ref([
      { value: 'acids', label: 'Ácidos' },
      { value: 'bases', label: 'Bases' },
      { value: 'salts', label: 'Sais' },
      { value: 'solvents', label: 'Solventes' },
      { value: 'indicators', label: 'Indicadores' }
    ])
    
    const units = ref([
      { value: 'liter', label: 'Litro' },
      { value: 'kilogram', label: 'Kilograma' },
      { value: 'gram', label: 'Grama' },
      { value: 'milliliter', label: 'Mililitro' },
      { value: 'piece', label: 'Peça' }
    ])
    
    // Formulário de edição
    const editForm = ref({
      name: 'Ácido Clorídrico',
      category: 'acids',
      unit: 'liter',
      min_stock: 10,
      description: 'O ácido clorídrico é um composto químico constituído por um átomo de hidrogênio e um de cloro. É altamente corrosivo e deve ser manipulado com extremo cuidado, utilizando equipamentos de proteção individual adequados.'
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
    
    const editReagent = () => {
      showEditModal.value = true
    }
    
    const closeEditModal = () => {
      showEditModal.value = false
    }
    
    const saveReagent = () => {
      // Lógica para salvar o reagente
      console.log('Salvando reagente:', editForm.value)
      closeEditModal()
    }
    
    const addLot = () => {
      // Lógica para adicionar lote
      console.log('Adicionando novo lote')
    }
    
    const viewLotDetails = (id) => {
      // Lógica para visualizar detalhes do lote
      console.log('Visualizando detalhes do lote:', id)
    }
    
    const editLot = (id) => {
      // Lógica para editar lote
      console.log('Editando lote:', id)
    }
    
    const deleteLot = (id) => {
      // Lógica para excluir lote
      console.log('Excluindo lote:', id)
    }
    
    return {
      showEditModal,
      lots,
      movements,
      categories,
      units,
      editForm,
      getExpiryVariant,
      getStatusVariant,
      formatDate,
      editReagent,
      closeEditModal,
      saveReagent,
      addLot,
      viewLotDetails,
      editLot,
      deleteLot
    }
  }
}
</script>