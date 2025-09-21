<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Reagentes</h1>
    
    <!-- Barra de ferramentas -->
    <div class="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div class="flex-1 max-w-md">
        <Input 
          v-model="searchQuery" 
          placeholder="Buscar reagentes..." 
          type="search"
          prepend-icon="search"
        />
      </div>
      <Button variant="primary" @click="openCreateModal">
        <Icon name="plus" class="mr-2" />
        Novo Reagente
      </Button>
    </div>
    
    <!-- Tabela de reagentes -->
    <Card class="bg-white">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estoque Mínimo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade Atual</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="reagent in reagents" :key="reagent.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ reagent.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ reagent.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ reagent.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ reagent.min_stock }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <Badge :variant="getStockLevelVariant(reagent.current_stock, reagent.min_stock)">
                  {{ reagent.current_stock }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="viewDetails(reagent.id)">
                  <Icon name="eye" />
                </Button>
                <Button variant="outline" size="sm" class="mr-2" @click="editReagent(reagent.id)">
                  <Icon name="edit" />
                </Button>
                <Button variant="outline" size="sm" @click="deleteReagent(reagent.id)">
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
          {{ editingReagent ? 'Editar Reagente' : 'Novo Reagente' }}
        </h3>
      </template>
      
      <form @submit.prevent="saveReagent">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
            <Input v-model="form.name" placeholder="Nome do reagente" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Categoria *</label>
            <Select v-model="form.category" :options="categories" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unidade *</label>
            <Select v-model="form.unit" :options="units" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Estoque Mínimo *</label>
            <Input v-model="form.min_stock" type="number" placeholder="Quantidade mínima" />
          </div>
          
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea 
              v-model="form.description" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Descrição detalhada do reagente"
            ></textarea>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeModal">Cancelar</Button>
        <Button variant="primary" @click="saveReagent">Salvar</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'ReagentsList',
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
    const searchQuery = ref('')
    const showModal = ref(false)
    const editingReagent = ref(null)
    
    // Dados fictícios para demonstração
    const reagents = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        unit: 'Litro',
        min_stock: 10,
        current_stock: 25
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        unit: 'Litro',
        min_stock: 20,
        current_stock: 8
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        unit: 'Kilograma',
        min_stock: 5,
        current_stock: 12
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
    
    // Formulário
    const form = ref({
      name: '',
      category: '',
      unit: '',
      min_stock: 0,
      description: ''
    })
    
    // Métodos
    const getStockLevelVariant = (current, minimum) => {
      if (current <= minimum) return 'error'
      if (current <= minimum * 1.5) return 'warning'
      return 'success'
    }
    
    const openCreateModal = () => {
      editingReagent.value = null
      form.value = {
        name: '',
        category: '',
        unit: '',
        min_stock: 0,
        description: ''
      }
      showModal.value = true
    }
    
    const closeModal = () => {
      showModal.value = false
    }
    
    const saveReagent = () => {
      // Lógica para salvar o reagente
      console.log('Salvando reagente:', form.value)
      closeModal()
    }
    
    const viewDetails = (id) => {
      // Lógica para visualizar detalhes
      console.log('Visualizando detalhes do reagente:', id)
    }
    
    const editReagent = (id) => {
      // Lógica para editar reagente
      const reagent = reagents.value.find(r => r.id === id)
      if (reagent) {
        editingReagent.value = reagent
        form.value = { ...reagent }
        showModal.value = true
      }
    }
    
    const deleteReagent = (id) => {
      // Lógica para excluir reagente
      console.log('Excluindo reagente:', id)
    }
    
    // Dados filtrados
    const filteredReagents = computed(() => {
      if (!searchQuery.value) return reagents.value
      const query = searchQuery.value.toLowerCase()
      return reagents.value.filter(reagent => 
        reagent.name.toLowerCase().includes(query) ||
        reagent.category.toLowerCase().includes(query)
      )
    })
    
    return {
      searchQuery,
      showModal,
      editingReagent,
      reagents: filteredReagents,
      categories,
      units,
      form,
      getStockLevelVariant,
      openCreateModal,
      closeModal,
      saveReagent,
      viewDetails,
      editReagent,
      deleteReagent
    }
  }
}
</script>