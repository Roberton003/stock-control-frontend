<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Componentes de Filtro Reutilizáveis</h1>
      <Button variant="primary" @click="openFilterModal">
        <Icon name="filter" class="mr-2" />
        Aplicar Filtros
      </Button>
    </div>
    
    <!-- Exemplo de uso dos componentes de filtro -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Exemplo de Filtros</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <!-- Filtro de texto -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Pesquisa por Nome</label>
          <Input 
            v-model="filters.name" 
            placeholder="Digite o nome do reagente" 
            type="search"
            @input="debouncedSearch"
          />
        </div>
        
        <!-- Filtro de seleção única -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
          <Select 
            v-model="filters.category" 
            :options="categories" 
            placeholder="Selecione uma categoria"
            @change="applyFilters"
          />
        </div>
        
        <!-- Filtro de seleção múltipla -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <MultiSelect 
            v-model="filters.status" 
            :options="statuses" 
            placeholder="Selecione os status"
            @change="applyFilters"
          />
        </div>
        
        <!-- Filtro de data -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data de Validade</label>
          <div class="flex space-x-2">
            <Input 
              v-model="filters.startDate" 
              type="date" 
              placeholder="Data inicial"
              @change="applyFilters"
            />
            <Input 
              v-model="filters.endDate" 
              type="date" 
              placeholder="Data final"
              @change="applyFilters"
            />
          </div>
        </div>
        
        <!-- Filtro de número -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade Mínima</label>
          <Input 
            v-model="filters.minQuantity" 
            type="number" 
            placeholder="Quantidade mínima"
            @input="debouncedSearch"
          />
        </div>
        
        <!-- Filtro booleano -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Próximo ao Vencimento</label>
          <Toggle 
            v-model="filters.nearExpiry" 
            label="Mostrar apenas próximos ao vencimento"
            @change="applyFilters"
          />
        </div>
      </div>
      
      <!-- Botões de ação -->
      <div class="px-4 pb-4">
        <Button variant="outline" @click="resetFilters">
          <Icon name="undo" class="mr-2" />
          Limpar Filtros
        </Button>
      </div>
    </Card>
    
    <!-- Resultados filtrados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Resultados Filtrados</h2>
      </template>
      <div class="overflow-x-auto p-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in filteredItems" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }} {{ item.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getExpiryVariant(item.expiryDate)">
                  {{ formatDate(item.expiryDate) }}
                </Badge>
              </td>
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
    
    <!-- Modal de filtros avançados -->
    <Modal :visible="showFilterModal" @close="closeFilterModal">
      <template #header>
        <h3 class="text-lg font-medium">Filtros Avançados</h3>
      </template>
      
      <div class="grid grid-cols-1 gap-6 p-4">
        <!-- Filtros adicionais podem ser adicionados aqui -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fornecedor</label>
          <Select 
            v-model="filters.supplier" 
            :options="suppliers" 
            placeholder="Selecione um fornecedor"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
          <Select 
            v-model="filters.location" 
            :options="locations" 
            placeholder="Selecione uma localização"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ordenação</label>
          <Select 
            v-model="filters.sortBy" 
            :options="sortOptions" 
            placeholder="Ordene por"
          />
        </div>
      </div>
      
      <template #footer>
        <Button variant="outline" @click="closeFilterModal">Cancelar</Button>
        <Button variant="primary" @click="applyAdvancedFilters">Aplicar Filtros</Button>
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
import MultiSelect from '@/components/ui/MultiSelect.vue'
import Toggle from '@/components/ui/Toggle.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'ReusableFilterComponents',
  components: {
    Card,
    Button,
    Input,
    Select,
    MultiSelect,
    Toggle,
    Modal,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const showFilterModal = ref(false)
    
    // Filtros
    const filters = ref({
      name: '',
      category: '',
      status: [],
      startDate: '',
      endDate: '',
      minQuantity: 0,
      nearExpiry: false,
      supplier: '',
      location: '',
      sortBy: ''
    })
    
    // Dados fictícios para demonstração
    const items = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro',
        expiryDate: '2024-12-31',
        status: 'Ativo',
        supplier: 'LabQuímica Ltda',
        location: 'Armário A1'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro',
        expiryDate: '2024-06-30',
        status: 'Expirando',
        supplier: 'Química Brasil',
        location: 'Armário B2'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma',
        expiryDate: '2025-03-15',
        status: 'Ativo',
        supplier: 'Laboratórios ABC',
        location: 'Prateleira C3'
      }
    ])
    
    // Opções para seletores
    const categories = ref([
      { value: 'acids', label: 'Ácidos' },
      { value: 'bases', label: 'Bases' },
      { value: 'salts', label: 'Sais' },
      { value: 'solvents', label: 'Solventes' },
      { value: 'indicators', label: 'Indicadores' }
    ])
    
    const statuses = ref([
      { value: 'active', label: 'Ativo' },
      { value: 'expiring', label: 'Expirando' },
      { value: 'expired', label: 'Expirado' },
      { value: 'inactive', label: 'Inativo' }
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
    
    const sortOptions = ref([
      { value: 'name', label: 'Nome' },
      { value: 'category', label: 'Categoria' },
      { value: 'quantity', label: 'Quantidade' },
      { value: 'expiryDate', label: 'Data de Validade' },
      { value: 'status', label: 'Status' }
    ])
    
    // Dados filtrados
    const filteredItems = computed(() => {
      return items.value.filter(item => {
        // Filtro por nome
        if (filters.value.name && !item.name.toLowerCase().includes(filters.value.name.toLowerCase())) {
          return false
        }
        
        // Filtro por categoria
        if (filters.value.category && item.category !== filters.value.category) {
          return false
        }
        
        // Filtro por status
        if (filters.value.status.length > 0 && !filters.value.status.includes(item.status)) {
          return false
        }
        
        // Filtro por data de validade
        if (filters.value.startDate || filters.value.endDate) {
          const itemDate = new Date(item.expiryDate)
          
          if (filters.value.startDate && itemDate < new Date(filters.value.startDate)) {
            return false
          }
          
          if (filters.value.endDate && itemDate > new Date(filters.value.endDate)) {
            return false
          }
        }
        
        // Filtro por quantidade mínima
        if (filters.value.minQuantity > 0 && item.quantity < filters.value.minQuantity) {
          return false
        }
        
        // Filtro por próximo ao vencimento
        if (filters.value.nearExpiry) {
          const today = new Date()
          const expiryDate = new Date(item.expiryDate)
          const diffTime = expiryDate - today
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
          
          if (diffDays > 30) {
            return false
          }
        }
        
        return true
      })
    })
    
    // Debounce para pesquisa em tempo real
    let searchTimeout
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        applyFilters()
      }, 300)
    }
    
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
        case 'Inativo': return 'default'
        default: return 'default'
      }
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const openFilterModal = () => {
      showFilterModal.value = true
    }
    
    const closeFilterModal = () => {
      showFilterModal.value = false
    }
    
    const applyFilters = () => {
      // Lógica para aplicar os filtros
      console.log('Aplicando filtros:', filters.value)
    }
    
    const applyAdvancedFilters = () => {
      // Lógica para aplicar os filtros avançados
      console.log('Aplicando filtros avançados:', filters.value)
      closeFilterModal()
    }
    
    const resetFilters = () => {
      filters.value = {
        name: '',
        category: '',
        status: [],
        startDate: '',
        endDate: '',
        minQuantity: 0,
        nearExpiry: false,
        supplier: '',
        location: '',
        sortBy: ''
      }
      applyFilters()
    }
    
    return {
      showFilterModal,
      filters,
      items,
      filteredItems,
      categories,
      statuses,
      suppliers,
      locations,
      sortOptions,
      getExpiryVariant,
      getStatusVariant,
      formatDate,
      openFilterModal,
      closeFilterModal,
      applyFilters,
      applyAdvancedFilters,
      resetFilters,
      debouncedSearch
    }
  }
}
</script>