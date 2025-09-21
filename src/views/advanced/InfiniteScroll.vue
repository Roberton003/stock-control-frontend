<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Infinite Scroll</h1>
      <Button variant="primary" @click="toggleInfiniteScroll">
        <Icon :name="infiniteScrollEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ infiniteScrollEnabled ? 'Desativar' : 'Ativar' }} Infinite Scroll
      </Button>
    </div>
    
    <!-- Configurações do infinite scroll -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações do Infinite Scroll</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Itens por Carregamento</label>
          <Select 
            v-model="scrollSettings.itemsPerLoad" 
            :options="itemsPerLoadOptions" 
            placeholder="Selecione a quantidade" 
            @change="updateScrollSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Distância para Carregamento</label>
          <Select 
            v-model="scrollSettings.loadDistance" 
            :options="loadDistanceOptions" 
            placeholder="Selecione a distância" 
            @change="updateScrollSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Animação de Carregamento</label>
          <Toggle 
            v-model="scrollSettings.showLoadingAnimation" 
            label="Mostrar animação de carregamento" 
            @change="updateScrollSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Lista com infinite scroll -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Lista de Itens com Infinite Scroll</h2>
          <Badge :variant="infiniteScrollEnabled ? 'success' : 'default'">
            {{ infiniteScrollEnabled ? 'Ativado' : 'Desativado' }}
          </Badge>
        </div>
      </template>
      
      <div 
        ref="scrollContainer" 
        class="overflow-y-auto max-h-[500px]"
        @scroll="handleScroll"
      >
        <div class="divide-y divide-gray-200">
          <div 
            v-for="item in displayedItems" 
            :key="item.id" 
            class="p-4 hover:bg-gray-50 transition-colors duration-150"
          >
            <div class="flex justify-between items-center">
              <div>
                <h3 class="text-sm font-medium text-gray-900">{{ item.name }}</h3>
                <p class="text-sm text-gray-500">{{ item.category }}</p>
              </div>
              <div class="flex items-center">
                <Badge :variant="getStatusVariant(item.status)">
                  {{ item.status }}
                </Badge>
                <span class="ml-2 text-sm text-gray-500">{{ item.quantity }} {{ item.unit }}</span>
              </div>
            </div>
            <div class="mt-2 flex justify-between items-center">
              <span class="text-sm text-gray-500">Lote: {{ item.lot_number }}</span>
              <Badge :variant="getExpiryVariant(item.expiry_date)">
                {{ formatDate(item.expiry_date) }}
              </Badge>
            </div>
          </div>
          
          <!-- Indicador de carregamento -->
          <div 
            v-if="loading && scrollSettings.showLoadingAnimation" 
            class="p-4 flex justify-center items-center"
          >
            <Spinner size="lg" />
          </div>
          
          <!-- Mensagem de fim da lista -->
          <div 
            v-if="!hasMoreItems && !loading" 
            class="p-4 text-center text-sm text-gray-500"
          >
            Não há mais itens para carregar.
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre infinite scroll -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Infinite Scroll</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios do Infinite Scroll</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Melhora a experiência do usuário ao navegar por grandes conjuntos de dados</li>
              <li>Reduz o número de cliques necessários para acessar mais conteúdo</li>
              <li>Permite uma navegação contínua sem interrupções</li>
              <li>Aumenta o tempo de permanência na página</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Itens por Carregamento:</span>
                <span>{{ scrollSettings.itemsPerLoad }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Distância para Carregamento:</span>
                <span>{{ scrollSettings.loadDistance }} pixels</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Animação de Carregamento:</span>
                <span>{{ scrollSettings.showLoadingAnimation ? 'Ativada' : 'Desativada' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Infinite Scroll:</span>
                <span>{{ infiniteScrollEnabled ? 'Ativado' : 'Desativado' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Itens Carregados:</span>
                <span>{{ displayedItems.length }} de {{ allItems.length }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'
import Toggle from '@/components/ui/Toggle.vue'
import Spinner from '@/components/ui/Spinner.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'InfiniteScroll',
  components: {
    Card,
    Button,
    Select,
    Toggle,
    Spinner,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const infiniteScrollEnabled = ref(true)
    const loading = ref(false)
    const hasMoreItems = ref(true)
    const scrollContainer = ref(null)
    
    // Configurações do infinite scroll
    const scrollSettings = ref({
      itemsPerLoad: 10,
      loadDistance: 100,
      showLoadingAnimation: true
    })
    
    // Opções para seletores
    const itemsPerLoadOptions = ref([
      { value: 5, label: '5 itens' },
      { value: 10, label: '10 itens' },
      { value: 20, label: '20 itens' },
      { value: 50, label: '50 itens' }
    ])
    
    const loadDistanceOptions = ref([
      { value: 50, label: '50 pixels' },
      { value: 100, label: '100 pixels' },
      { value: 200, label: '200 pixels' },
      { value: 500, label: '500 pixels' }
    ])
    
    // Dados fictícios para demonstração
    const allItems = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro',
        lot_number: 'AC12345',
        expiry_date: '2024-12-31',
        status: 'Ativo'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro',
        lot_number: 'ET67890',
        expiry_date: '2024-06-30',
        status: 'Expirando'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma',
        lot_number: 'SC54321',
        expiry_date: '2025-03-15',
        status: 'Ativo'
      },
      {
        id: 4,
        name: 'Ácido Nítrico',
        category: 'Ácidos',
        quantity: 15,
        unit: 'Litro',
        lot_number: 'AN98765',
        expiry_date: '2024-09-30',
        status: 'Ativo'
      },
      {
        id: 5,
        name: 'Hidróxido de Sódio',
        category: 'Bases',
        quantity: 8,
        unit: 'Kilograma',
        lot_number: 'HS45678',
        expiry_date: '2025-01-20',
        status: 'Ativo'
      },
      {
        id: 6,
        name: 'Ácido Sulfúrico',
        category: 'Ácidos',
        quantity: 20,
        unit: 'Litro',
        lot_number: 'AS24680',
        expiry_date: '2024-11-15',
        status: 'Ativo'
      },
      {
        id: 7,
        name: 'Etanol 70%',
        category: 'Álcoois',
        quantity: 30,
        unit: 'Litro',
        lot_number: 'E73570',
        expiry_date: '2024-08-10',
        status: 'Ativo'
      },
      {
        id: 8,
        name: 'Cloreto de Sódio',
        category: 'Sais',
        quantity: 12,
        unit: 'Kilograma',
        lot_number: 'CS13579',
        expiry_date: '2025-05-30',
        status: 'Ativo'
      },
      {
        id: 9,
        name: 'Ácido Acético',
        category: 'Ácidos',
        quantity: 18,
        unit: 'Litro',
        lot_number: 'AA97531',
        expiry_date: '2024-10-25',
        status: 'Ativo'
      },
      {
        id: 10,
        name: 'Metanol',
        category: 'Álcoois',
        quantity: 7,
        unit: 'Litro',
        lot_number: 'ME86420',
        expiry_date: '2024-07-12',
        status: 'Ativo'
      },
      {
        id: 11,
        name: 'Carbonato de Cálcio',
        category: 'Sais',
        quantity: 15,
        unit: 'Kilograma',
        lot_number: 'CC75319',
        expiry_date: '2025-02-28',
        status: 'Ativo'
      },
      {
        id: 12,
        name: 'Ácido Fosfórico',
        category: 'Ácidos',
        quantity: 12,
        unit: 'Litro',
        lot_number: 'AF64208',
        expiry_date: '2024-12-15',
        status: 'Ativo'
      },
      {
        id: 13,
        name: 'Propanol',
        category: 'Álcoois',
        quantity: 9,
        unit: 'Litro',
        lot_number: 'PR53197',
        expiry_date: '2024-09-20',
        status: 'Ativo'
      },
      {
        id: 14,
        name: 'Nitrato de Prata',
        category: 'Sais',
        quantity: 3,
        unit: 'Kilograma',
        lot_number: 'NP42086',
        expiry_date: '2025-04-10',
        status: 'Ativo'
      },
      {
        id: 15,
        name: 'Ácido Perclórico',
        category: 'Ácidos',
        quantity: 6,
        unit: 'Litro',
        lot_number: 'AP31975',
        expiry_date: '2024-08-30',
        status: 'Ativo'
      }
    ])
    
    // Itens exibidos (inicialmente vazio, carregados conforme o scroll)
    const displayedItems = ref([])
    
    // Métodos
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Ativo': return 'success'
        case 'Expirando': return 'warning'
        case 'Expirado': return 'error'
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
    
    const toggleInfiniteScroll = () => {
      infiniteScrollEnabled.value = !infiniteScrollEnabled.value
    }
    
    const updateScrollSettings = () => {
      // Atualizar configurações do infinite scroll
      console.log('Atualizando configurações do infinite scroll:', scrollSettings.value)
    }
    
    const handleScroll = () => {
      if (!infiniteScrollEnabled.value || loading.value || !hasMoreItems.value) return
      
      const container = scrollContainer.value
      if (!container) return
      
      const { scrollTop, scrollHeight, clientHeight } = container
      const distanceFromBottom = scrollHeight - scrollTop - clientHeight
      
      // Verificar se o usuário chegou perto do final da lista
      if (distanceFromBottom <= scrollSettings.value.loadDistance) {
        loadMoreItems()
      }
    }
    
    const loadMoreItems = () => {
      if (loading.value || !hasMoreItems.value) return
      
      loading.value = true
      
      // Simular carregamento de mais itens
      setTimeout(() => {
        const currentLength = displayedItems.value.length
        const newItems = allItems.value.slice(
          currentLength, 
          currentLength + scrollSettings.value.itemsPerLoad
        )
        
        displayedItems.value.push(...newItems)
        
        // Verificar se todos os itens foram carregados
        if (displayedItems.value.length >= allItems.value.length) {
          hasMoreItems.value = false
        }
        
        loading.value = false
      }, 1000)
    }
    
    const initializeItems = () => {
      // Carregar os primeiros itens
      const initialItems = allItems.value.slice(0, scrollSettings.value.itemsPerLoad)
      displayedItems.value = initialItems
      
      // Verificar se todos os itens foram carregados inicialmente
      if (initialItems.length >= allItems.value.length) {
        hasMoreItems.value = false
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      initializeItems()
    })
    
    onUnmounted(() => {
      // Limpar event listeners se necessário
    })
    
    return {
      infiniteScrollEnabled,
      loading,
      hasMoreItems,
      scrollContainer,
      scrollSettings,
      itemsPerLoadOptions,
      loadDistanceOptions,
      allItems,
      displayedItems,
      getStatusVariant,
      getExpiryVariant,
      formatDate,
      toggleInfiniteScroll,
      updateScrollSettings,
      handleScroll,
      loadMoreItems,
      initializeItems
    }
  }
}
</script>