<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Busca em Tempo Real</h1>
      <Button variant="primary" @click="openSearchModal">
        <Icon name="search" class="mr-2" />
        Buscar
      </Button>
    </div>
    
    <!-- Barra de busca -->
    <Card class="mb-6 bg-white">
      <div class="p-4">
        <div class="relative">
          <Input 
            v-model="searchQuery" 
            placeholder="Digite sua busca..." 
            type="search"
            @input="debouncedSearch"
          />
          <div v-if="isLoading" class="absolute inset-y-0 right-0 flex items-center pr-3">
            <Spinner size="sm" />
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Resultados da busca -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Resultados da Busca</h2>
      </template>
      
      <!-- Mensagem de busca vazia -->
      <div v-if="!searchQuery && !searchResults.length" class="p-8 text-center">
        <Icon name="search" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-lg font-medium text-gray-900">Nenhuma busca realizada</h3>
        <p class="mt-1 text-sm text-gray-500">Digite algo na barra de busca para ver os resultados.</p>
      </div>
      
      <!-- Mensagem de nenhum resultado -->
      <div v-else-if="searchQuery && !searchResults.length && !isLoading" class="p-8 text-center">
        <Icon name="search-off" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-lg font-medium text-gray-900">Nenhum resultado encontrado</h3>
        <p class="mt-1 text-sm text-gray-500">Tente ajustar sua busca ou usar termos diferentes.</p>
      </div>
      
      <!-- Resultados -->
      <div v-else-if="searchResults.length" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="result in searchResults" :key="result.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getTypeVariant(result.type)">
                  {{ result.type }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ result.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result.quantity }} {{ result.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getExpiryVariant(result.expiryDate)">
                  {{ formatDate(result.expiryDate) }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="viewDetails(result.id, result.type)">
                  <Icon name="eye" />
                </Button>
                <Button variant="outline" size="sm" @click="addToCart(result.id, result.type)">
                  <Icon name="cart-plus" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Indicador de carregamento -->
      <div v-else-if="isLoading" class="p-8 flex justify-center">
        <Spinner size="lg" />
      </div>
    </Card>
    
    <!-- Sugestões de busca -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Sugestões de Busca</h2>
      </template>
      <div class="p-4">
        <div class="flex flex-wrap gap-2">
          <Button 
            v-for="suggestion in suggestions" 
            :key="suggestion" 
            variant="outline" 
            size="sm" 
            @click="applySuggestion(suggestion)"
            class="mr-2 mb-2"
          >
            {{ suggestion }}
          </Button>
        </div>
      </div>
    </Card>
    
    <!-- Histórico de buscas -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Histórico de Buscas</h2>
      </template>
      <div class="p-4">
        <div v-if="searchHistory.length">
          <div 
            v-for="(query, index) in searchHistory" 
            :key="index" 
            class="flex justify-between items-center py-2 border-b border-gray-200 last:border-b-0"
          >
            <span class="text-sm text-gray-700 cursor-pointer hover:text-primary" @click="repeatSearch(query)">
              {{ query }}
            </span>
            <Button variant="outline" size="sm" @click="removeFromHistory(index)">
              <Icon name="times" />
            </Button>
          </div>
        </div>
        <div v-else class="text-center py-4">
          <p class="text-sm text-gray-500">Nenhuma busca realizada ainda.</p>
        </div>
      </div>
    </Card>
    
    <!-- Modal de busca avançada -->
    <Modal :visible="showSearchModal" @close="closeSearchModal">
      <template #header>
        <h3 class="text-lg font-medium">Busca Avançada</h3>
      </template>
      
      <form @submit.prevent="performAdvancedSearch">
        <div class="grid grid-cols-1 gap-6 p-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Termo de Busca</label>
            <Input v-model="advancedSearchForm.query" placeholder="Digite o termo de busca" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Item</label>
            <Select 
              v-model="advancedSearchForm.itemType" 
              :options="itemTypes" 
              placeholder="Selecione o tipo de item"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
            <Select 
              v-model="advancedSearchForm.category" 
              :options="categories" 
              placeholder="Selecione uma categoria"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Validade</label>
            <div class="flex space-x-2">
              <Input 
                v-model="advancedSearchForm.startDate" 
                type="date" 
                placeholder="Data inicial"
              />
              <Input 
                v-model="advancedSearchForm.endDate" 
                type="date" 
                placeholder="Data final"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade Mínima</label>
            <Input 
              v-model="advancedSearchForm.minQuantity" 
              type="number" 
              placeholder="Quantidade mínima"
            />
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeSearchModal">Cancelar</Button>
        <Button variant="primary" @click="performAdvancedSearch">Buscar</Button>
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
import Spinner from '@/components/ui/Spinner.vue'

export default {
  name: 'RealTimeSearch',
  components: {
    Card,
    Button,
    Input,
    Select,
    Modal,
    Icon,
    Badge,
    Spinner
  },
  setup() {
    // Estados
    const searchQuery = ref('')
    const isLoading = ref(false)
    const showSearchModal = ref(false)
    const searchResults = ref([])
    const searchHistory = ref([])
    
    // Formulário de busca avançada
    const advancedSearchForm = ref({
      query: '',
      itemType: '',
      category: '',
      startDate: '',
      endDate: '',
      minQuantity: 0
    })
    
    // Dados fictícios para demonstração
    const suggestions = ref([
      'Ácido Clorídrico',
      'Etanol 96%',
      'Sulfato de Cobre',
      'Reagente Expirando',
      'Estoque Baixo'
    ])
    
    const itemTypes = ref([
      { value: 'reagent', label: 'Reagente' },
      { value: 'stock-lot', label: 'Lote de Estoque' },
      { value: 'requisition', label: 'Requisição' }
    ])
    
    const categories = ref([
      { value: 'acids', label: 'Ácidos' },
      { value: 'bases', label: 'Bases' },
      { value: 'salts', label: 'Sais' },
      { value: 'solvents', label: 'Solventes' },
      { value: 'indicators', label: 'Indicadores' }
    ])
    
    // Debounce para pesquisa em tempo real
    let searchTimeout
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        performSearch()
      }, 300)
    }
    
    // Métodos
    const performSearch = () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = []
        return
      }
      
      isLoading.value = true
      
      // Simular requisição à API
      setTimeout(() => {
        // Dados fictícios para demonstração
        searchResults.value = [
          {
            id: 1,
            type: 'Reagente',
            name: 'Ácido Clorídrico',
            category: 'Ácidos',
            quantity: 25,
            unit: 'Litro',
            expiryDate: '2024-12-31'
          },
          {
            id: 2,
            type: 'Lote de Estoque',
            name: 'Etanol 96%',
            category: 'Álcoois',
            quantity: 10,
            unit: 'Litro',
            expiryDate: '2024-06-30'
          },
          {
            id: 3,
            type: 'Reagente',
            name: 'Sulfato de Cobre',
            category: 'Sais',
            quantity: 5,
            unit: 'Kilograma',
            expiryDate: '2025-03-15'
          }
        ]
        
        isLoading.value = false
        
        // Adicionar à história de buscas
        addToHistory(searchQuery.value)
      }, 500)
    }
    
    const performAdvancedSearch = () => {
      // Lógica para realizar busca avançada
      console.log('Realizando busca avançada:', advancedSearchForm.value)
      closeSearchModal()
    }
    
    const getTypeVariant = (type) => {
      switch (type) {
        case 'Reagente': return 'primary'
        case 'Lote de Estoque': return 'secondary'
        case 'Requisição': return 'accent'
        default: return 'default'
      }
    }
    
    const getExpiryVariant = (expiryDate) => {
      const today = new Date()
      const expiry = new Date(expiryDate)
      const diffTime = expiry - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) return 'error'
      if (diffDays <= 30) return 'warning'
      return 'success'
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const openSearchModal = () => {
      showSearchModal.value = true
    }
    
    const closeSearchModal = () => {
      showSearchModal.value = false
    }
    
    const viewDetails = (id, type) => {
      // Lógica para visualizar detalhes
      console.log(`Visualizando detalhes do ${type} #${id}`)
    }
    
    const addToCart = (id, type) => {
      // Lógica para adicionar ao carrinho
      console.log(`Adicionando ${type} #${id} ao carrinho`)
    }
    
    const applySuggestion = (suggestion) => {
      searchQuery.value = suggestion
      performSearch()
    }
    
    const addToHistory = (query) => {
      // Verificar se a consulta já existe no histórico
      const index = searchHistory.value.indexOf(query)
      if (index !== -1) {
        // Remover a consulta existente
        searchHistory.value.splice(index, 1)
      }
      
      // Adicionar a consulta no início do histórico
      searchHistory.value.unshift(query)
      
      // Limitar o histórico a 10 itens
      if (searchHistory.value.length > 10) {
        searchHistory.value.pop()
      }
    }
    
    const removeFromHistory = (index) => {
      searchHistory.value.splice(index, 1)
    }
    
    const repeatSearch = (query) => {
      searchQuery.value = query
      performSearch()
    }
    
    return {
      searchQuery,
      isLoading,
      showSearchModal,
      searchResults,
      searchHistory,
      advancedSearchForm,
      suggestions,
      itemTypes,
      categories,
      debouncedSearch,
      performSearch,
      performAdvancedSearch,
      getTypeVariant,
      getExpiryVariant,
      formatDate,
      openSearchModal,
      closeSearchModal,
      viewDetails,
      addToCart,
      applySuggestion,
      removeFromHistory,
      repeatSearch
    }
  }
}
</script>