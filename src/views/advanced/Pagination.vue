<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Paginação em Todas as Listagens</h1>
      <Button variant="primary" @click="configurePagination">
        <Icon name="cog" class="mr-2" />
        Configurar Paginação
      </Button>
    </div>
    
    <!-- Configurações de paginação -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações de Paginação</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Itens por Página</label>
          <Select 
            v-model="paginationSettings.itemsPerPage" 
            :options="itemsPerPageOptions" 
            placeholder="Selecione a quantidade" 
            @change="updatePaginationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Posição da Paginação</label>
          <Select 
            v-model="paginationSettings.position" 
            :options="paginationPositions" 
            placeholder="Selecione a posição" 
            @change="updatePaginationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Estilo da Paginação</label>
          <Select 
            v-model="paginationSettings.style" 
            :options="paginationStyles" 
            placeholder="Selecione o estilo" 
            @change="updatePaginationSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de paginação em uma listagem -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Exemplo de Listagem com Paginação</h2>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validade</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in paginatedItems" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ item.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getExpiryVariant(item.expiryDate)">
                  {{ formatDate(item.expiryDate) }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Paginação -->
      <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Mostrando <span class="font-medium">{{ pagination.currentPage * pagination.itemsPerPage - pagination.itemsPerPage + 1 }}</span> a 
          <span class="font-medium">{{ Math.min(pagination.currentPage * pagination.itemsPerPage, pagination.totalItems) }}</span> de 
          <span class="font-medium">{{ pagination.totalItems }}</span> resultados
        </div>
        <div class="flex space-x-2">
          <Button 
            variant="outline" 
            size="sm" 
            :disabled="pagination.currentPage === 1"
            @click="previousPage"
          >
            Anterior
          </Button>
          <Button 
            v-for="page in paginationButtons" 
            :key="page" 
            :variant="page === pagination.currentPage ? 'primary' : 'outline'" 
            size="sm" 
            @click="goToPage(page)"
          >
            {{ page }}
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            :disabled="pagination.currentPage === pagination.totalPages"
            @click="nextPage"
          >
            Próximo
          </Button>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre paginação -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Paginação</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios da Paginação</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Melhora o desempenho da aplicação ao carregar menos dados por vez</li>
              <li>Facilita a navegação em conjuntos grandes de dados</li>
              <li>Reduz o tempo de carregamento inicial das páginas</li>
              <li>Melhora a experiência do usuário ao organizar informações</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Itens por Página:</span>
                <span>{{ paginationSettings.itemsPerPage }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Posição:</span>
                <span>{{ paginationSettings.position }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Estilo:</span>
                <span>{{ paginationSettings.style }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Página Atual:</span>
                <span>{{ pagination.currentPage }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Total de Páginas:</span>
                <span>{{ pagination.totalPages }}</span>
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
import Select from '@/components/ui/Select.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'PaginationSystem',
  components: {
    Card,
    Button,
    Select,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const paginationSettings = ref({
      itemsPerPage: 10,
      position: 'bottom',
      style: 'numbers'
    })
    
    const pagination = ref({
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 97,
      totalPages: 10
    })
    
    // Opções para seletores
    const itemsPerPageOptions = ref([
      { value: 5, label: '5 itens por página' },
      { value: 10, label: '10 itens por página' },
      { value: 20, label: '20 itens por página' },
      { value: 50, label: '50 itens por página' },
      { value: 100, label: '100 itens por página' }
    ])
    
    const paginationPositions = ref([
      { value: 'top', label: 'Topo' },
      { value: 'bottom', label: 'Rodapé' },
      { value: 'both', label: 'Ambos' }
    ])
    
    const paginationStyles = ref([
      { value: 'numbers', label: 'Números' },
      { value: 'arrows', label: 'Setas' },
      { value: 'dots', label: 'Pontos' }
    ])
    
    // Dados fictícios para demonstração
    const allItems = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro',
        expiryDate: '2024-12-31'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro',
        expiryDate: '2024-06-30'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma',
        expiryDate: '2025-03-15'
      },
      {
        id: 4,
        name: 'Ácido Nítrico',
        category: 'Ácidos',
        quantity: 15,
        unit: 'Litro',
        expiryDate: '2024-09-30'
      },
      {
        id: 5,
        name: 'Hidróxido de Sódio',
        category: 'Bases',
        quantity: 8,
        unit: 'Kilograma',
        expiryDate: '2025-01-20'
      },
      {
        id: 6,
        name: 'Ácido Sulfúrico',
        category: 'Ácidos',
        quantity: 20,
        unit: 'Litro',
        expiryDate: '2024-11-15'
      },
      {
        id: 7,
        name: 'Etanol 70%',
        category: 'Álcoois',
        quantity: 30,
        unit: 'Litro',
        expiryDate: '2024-08-10'
      },
      {
        id: 8,
        name: 'Cloreto de Sódio',
        category: 'Sais',
        quantity: 12,
        unit: 'Kilograma',
        expiryDate: '2025-05-30'
      },
      {
        id: 9,
        name: 'Ácido Acético',
        category: 'Ácidos',
        quantity: 18,
        unit: 'Litro',
        expiryDate: '2024-10-25'
      },
      {
        id: 10,
        name: 'Metanol',
        category: 'Álcoois',
        quantity: 7,
        unit: 'Litro',
        expiryDate: '2024-07-12'
      }
    ])
    
    // Dados paginados
    const paginatedItems = computed(() => {
      const start = (pagination.value.currentPage - 1) * pagination.value.itemsPerPage
      const end = start + pagination.value.itemsPerPage
      return allItems.value.slice(start, end)
    })
    
    // Botões de paginação
    const paginationButtons = computed(() => {
      const buttons = []
      const totalPages = pagination.value.totalPages
      const currentPage = pagination.value.currentPage
      
      // Sempre mostrar a primeira página
      buttons.push(1)
      
      // Mostrar páginas próximas à página atual
      for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
        buttons.push(i)
      }
      
      // Sempre mostrar a última página
      if (totalPages > 1) {
        buttons.push(totalPages)
      }
      
      return buttons
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
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const configurePagination = () => {
      // Lógica para configurar a paginação
      console.log('Configurando paginação:', paginationSettings.value)
    }
    
    const updatePaginationSettings = () => {
      // Atualizar configurações de paginação
      pagination.value.itemsPerPage = paginationSettings.value.itemsPerPage
      console.log('Atualizando configurações de paginação:', paginationSettings.value)
    }
    
    const goToPage = (page) => {
      pagination.value.currentPage = page
    }
    
    const previousPage = () => {
      if (pagination.value.currentPage > 1) {
        pagination.value.currentPage--
      }
    }
    
    const nextPage = () => {
      if (pagination.value.currentPage < pagination.value.totalPages) {
        pagination.value.currentPage++
      }
    }
    
    return {
      paginationSettings,
      pagination,
      itemsPerPageOptions,
      paginationPositions,
      paginationStyles,
      allItems,
      paginatedItems,
      paginationButtons,
      getExpiryVariant,
      formatDate,
      configurePagination,
      updatePaginationSettings,
      goToPage,
      previousPage,
      nextPage
    }
  }
}
</script>