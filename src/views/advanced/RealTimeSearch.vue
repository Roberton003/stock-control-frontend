<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Busca em Tempo Real</h1>
      <Button variant="primary" @click="toggleRealTimeSearch">
        <Icon :name="realTimeSearchEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ realTimeSearchEnabled ? 'Desativar' : 'Ativar' }} Busca em Tempo Real
      </Button>
    </div>
    
    <!-- Configurações da busca em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações da Busca em Tempo Real</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Atraso (ms)</label>
          <Input 
            v-model="searchSettings.delay" 
            type="number" 
            placeholder="Atraso em milissegundos" 
            @input="updateSearchSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Campos de Busca</label>
          <Select 
            v-model="searchSettings.fields" 
            :options="searchFields" 
            multiple 
            placeholder="Selecione os campos" 
            @change="updateSearchSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Mostrar Sugestões</label>
          <Toggle 
            v-model="searchSettings.showSuggestions" 
            label="Exibir sugestões de busca" 
            @change="updateSearchSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Barra de busca com sugestões -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Barra de Busca com Sugestões</h2>
          <Badge :variant="realTimeSearchEnabled ? 'success' : 'default'">
            {{ realTimeSearchEnabled ? 'Ativada' : 'Desativada' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="relative">
          <Input 
            v-model="searchQuery" 
            placeholder="Digite sua busca..." 
            type="search"
            @input="debouncedSearch"
            @focus="showSuggestions = true"
            @blur="hideSuggestions"
          />
          
          <!-- Sugestões de busca -->
          <div 
            v-if="showSuggestions && searchSuggestions.length && realTimeSearchEnabled" 
            class="absolute z-10 mt-1 w-full rounded-md bg-white shadow-lg"
          >
            <ul class="max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
              <li 
                v-for="(suggestion, index) in searchSuggestions" 
                :key="index"
                class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-gray-100"
                @mousedown="selectSuggestion(suggestion)"
              >
                <div class="flex items-center">
                  <Icon name="search" class="mr-2 text-gray-400" />
                  <span class="font-normal truncate">{{ suggestion }}</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Resultados da busca em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Resultados da Busca em Tempo Real</h2>
          <Badge :variant="searchResults.length ? 'success' : 'default'">
            {{ searchResults.length }} resultados encontrados
          </Badge>
        </div>
      </template>
      
      <div class="overflow-x-auto p-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validade</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="result in searchResults" :key="result.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ result.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result.quantity }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getExpiryVariant(result.expiryDate)">
                  {{ formatDate(result.expiryDate) }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Mensagem de busca vazia -->
      <div v-if="!searchResults.length && searchQuery && !loading" class="p-8 text-center">
        <Icon name="search-off" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-lg font-medium text-gray-900">Nenhum resultado encontrado</h3>
        <p class="mt-1 text-sm text-gray-500">Tente ajustar sua busca ou usar termos diferentes.</p>
      </div>
      
      <!-- Indicador de carregamento -->
      <div v-if="loading" class="p-8 flex justify-center">
        <Spinner size="lg" />
      </div>
    </Card>
    
    <!-- Informações sobre busca em tempo real -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Busca em Tempo Real</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios da Busca em Tempo Real</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Fornece resultados instantâneos enquanto o usuário digita</li>
              <li>Melhora a experiência do usuário ao encontrar informações rapidamente</li>
              <li>Reduz o número de cliques necessários para encontrar itens</li>
              <li>Permite sugestões de busca inteligentes com base no histórico</li>
              <li>Ajuda os usuários a descobrir conteúdo relevante</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Busca em Tempo Real:</span>
                <span>{{ realTimeSearchEnabled ? 'Ativada' : 'Desativada' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Atraso:</span>
                <span>{{ searchSettings.delay }}ms</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Campos de Busca:</span>
                <span>{{ searchSettings.fields.length }} selecionados</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Mostrar Sugestões:</span>
                <span>{{ searchSettings.showSuggestions ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Resultados Encontrados:</span>
                <span>{{ searchResults.length }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Toggle from '@/components/ui/Toggle.vue'
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
    Toggle,
    Icon,
    Badge,
    Spinner
  },
  setup() {
    // Estados
    const realTimeSearchEnabled = ref(true)
    const showSuggestions = ref(false)
    const loading = ref(false)
    const searchQuery = ref('')
    const searchTimeout = ref(null)
    
    // Configurações da busca em tempo real
    const searchSettings = ref({
      delay: 300,
      fields: ['name', 'category'],
      showSuggestions: true
    })
    
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
      }
    ])
    
    // Resultados da busca
    const searchResults = ref([])
    
    // Sugestões de busca
    const searchSuggestions = ref([
      'Ácido Clorídrico',
      'Etanol 96%',
      'Sulfato de Cobre',
      'Ácido Nítrico',
      'Hidróxido de Sódio',
      'Ácidos',
      'Álcoois',
      'Sais',
      'Bases'
    ])
    
    // Opções para seletores
    const searchFields = ref([
      { value: 'name', label: 'Nome' },
      { value: 'category', label: 'Categoria' },
      { value: 'supplier', label: 'Fornecedor' },
      { value: 'location', label: 'Localização' }
    ])
    
    // Métodos
    const toggleRealTimeSearch = () => {
      realTimeSearchEnabled.value = !realTimeSearchEnabled.value
    }
    
    const updateSearchSettings = () => {
      // Atualizar configurações da busca em tempo real
      console.log('Atualizando configurações da busca em tempo real:', searchSettings.value)
    }
    
    const debouncedSearch = () => {
      if (!realTimeSearchEnabled.value) return
      
      // Limpar timeout anterior
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
      }
      
      // Configurar novo timeout
      searchTimeout.value = setTimeout(() => {
        performSearch()
      }, searchSettings.value.delay)
    }
    
    const performSearch = () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = []
        return
      }
      
      loading.value = true
      
      // Simular requisição à API
      setTimeout(() => {
        // Filtrar itens com base na consulta de busca
        searchResults.value = allItems.value.filter(item => {
          return searchSettings.value.fields.some(field => {
            return item[field].toLowerCase().includes(searchQuery.value.toLowerCase())
          })
        })
        
        loading.value = false
      }, 500)
    }
    
    const showSuggestionsList = () => {
      if (!realTimeSearchEnabled.value || !searchSettings.value.showSuggestions) return
      showSuggestions.value = true
    }
    
    const hideSuggestions = () => {
      // Pequeno atraso para permitir a seleção de sugestões
      setTimeout(() => {
        showSuggestions.value = false
      }, 150)
    }
    
    const selectSuggestion = (suggestion) => {
      searchQuery.value = suggestion
      showSuggestions.value = false
      performSearch()
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
    
    return {
      realTimeSearchEnabled,
      showSuggestions,
      loading,
      searchQuery,
      searchTimeout,
      searchSettings,
      allItems,
      searchResults,
      searchSuggestions,
      searchFields,
      toggleRealTimeSearch,
      updateSearchSettings,
      debouncedSearch,
      performSearch,
      showSuggestionsList,
      hideSuggestions,
      selectSuggestion,
      getExpiryVariant,
      formatDate
    }
  }
}
</script>