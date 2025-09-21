<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Skeleton Loaders</h1>
      <Button variant="primary" @click="toggleSkeletonLoaders">
        <Icon :name="skeletonLoadersEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ skeletonLoadersEnabled ? 'Desativar' : 'Ativar' }} Skeleton Loaders
      </Button>
    </div>
    
    <!-- Configurações dos skeleton loaders -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações dos Skeleton Loaders</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Duração da Animação</label>
          <Select 
            v-model="skeletonSettings.animationDuration" 
            :options="animationDurationOptions" 
            placeholder="Selecione a duração" 
            @change="updateSkeletonSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Cor Base</label>
          <Select 
            v-model="skeletonSettings.baseColor" 
            :options="baseColorOptions" 
            placeholder="Selecione a cor" 
            @change="updateSkeletonSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Cor de Destaque</label>
          <Select 
            v-model="skeletonSettings.highlightColor" 
            :options="highlightColorOptions" 
            placeholder="Selecione a cor" 
            @change="updateSkeletonSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplos de skeleton loaders -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <!-- Card com skeleton loader -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Card com Skeleton Loader</h2>
        </template>
        <div v-if="loading" class="p-4">
          <SkeletonLoader 
            :count="3" 
            :duration="skeletonSettings.animationDuration" 
            :base-color="skeletonSettings.baseColor" 
            :highlight-color="skeletonSettings.highlightColor"
          />
        </div>
        <div v-else class="p-4">
          <p class="text-gray-700">
            Este é um exemplo de card com skeleton loader. Quando os dados estão sendo carregados,
            são exibidos placeholders animados que indicam ao usuário que o conteúdo está sendo
            carregado.
          </p>
        </div>
      </Card>
      
      <!-- Tabela com skeleton loader -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Tabela com Skeleton Loader</h2>
        </template>
        <div v-if="loading" class="p-4">
          <SkeletonLoader 
            :count="5" 
            :duration="skeletonSettings.animationDuration" 
            :base-color="skeletonSettings.baseColor" 
            :highlight-color="skeletonSettings.highlightColor"
            type="table"
          />
        </div>
        <div v-else class="overflow-x-auto p-4">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in tableItems" :key="item.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }} {{ item.unit }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
    
    <!-- Lista com skeleton loader -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Lista com Skeleton Loader</h2>
      </template>
      <div v-if="loading" class="p-4">
        <SkeletonLoader 
          :count="4" 
          :duration="skeletonSettings.animationDuration" 
          :base-color="skeletonSettings.baseColor" 
          :highlight-color="skeletonSettings.highlightColor"
          type="list"
        />
      </div>
      <div v-else class="divide-y divide-gray-200">
        <div 
          v-for="item in listItems" 
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
        </div>
      </div>
    </Card>
    
    <!-- Controles de carregamento -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Controles de Carregamento</h2>
      </template>
      <div class="p-4 flex flex-wrap gap-4">
        <Button 
          variant="primary" 
          @click="simulateLoading"
          :disabled="loading"
        >
          <Icon name="sync" class="mr-2" :spin="loading" />
          {{ loading ? 'Carregando...' : 'Simular Carregamento' }}
        </Button>
        <Button 
          variant="outline" 
          @click="stopLoading"
          :disabled="!loading"
        >
          <Icon name="stop" class="mr-2" />
          Parar Carregamento
        </Button>
        <div class="flex items-center ml-auto">
          <label class="mr-2 text-sm text-gray-700">Tempo de Carregamento:</label>
          <Select 
            v-model="loadingTime" 
            :options="loadingTimeOptions" 
            class="w-32"
          />
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre skeleton loaders -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Skeleton Loaders</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios dos Skeleton Loaders</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Melhoram a percepção de velocidade do aplicativo</li>
              <li>Reduzem a ansiedade do usuário durante o carregamento</li>
              <li>Fornecem feedback visual imediato sobre o estado da aplicação</li>
              <li>Criam uma experiência mais fluida e profissional</li>
              <li>Evitam o efeito de flickering (piscar) da interface</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Duração da Animação:</span>
                <span>{{ skeletonSettings.animationDuration }}ms</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Cor Base:</span>
                <span>{{ skeletonSettings.baseColor }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Cor de Destaque:</span>
                <span>{{ skeletonSettings.highlightColor }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Skeleton Loaders:</span>
                <span>{{ skeletonLoadersEnabled ? 'Ativados' : 'Desativados' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Estado de Carregamento:</span>
                <span>{{ loading ? 'Carregando' : 'Pronto' }}</span>
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
import Select from '@/components/ui/Select.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'

export default {
  name: 'SkeletonLoaders',
  components: {
    Card,
    Button,
    Select,
    Icon,
    Badge,
    SkeletonLoader
  },
  setup() {
    // Estados
    const skeletonLoadersEnabled = ref(true)
    const loading = ref(false)
    const loadingTime = ref(2000)
    
    // Configurações dos skeleton loaders
    const skeletonSettings = ref({
      animationDuration: 1500,
      baseColor: '#f0f0f0',
      highlightColor: '#e0e0e0'
    })
    
    // Opções para seletores
    const animationDurationOptions = ref([
      { value: 500, label: '500ms' },
      { value: 1000, label: '1000ms' },
      { value: 1500, label: '1500ms' },
      { value: 2000, label: '2000ms' }
    ])
    
    const baseColorOptions = ref([
      { value: '#f0f0f0', label: 'Cinza Claro' },
      { value: '#e0e0e0', label: 'Cinza Médio' },
      { value: '#d0d0d0', label: 'Cinza Escuro' }
    ])
    
    const highlightColorOptions = ref([
      { value: '#e0e0e0', label: 'Cinza Médio' },
      { value: '#d0d0d0', label: 'Cinza Escuro' },
      { value: '#c0c0c0', label: 'Cinza Mais Escuro' }
    ])
    
    const loadingTimeOptions = ref([
      { value: 1000, label: '1 segundo' },
      { value: 2000, label: '2 segundos' },
      { value: 3000, label: '3 segundos' },
      { value: 5000, label: '5 segundos' }
    ])
    
    // Dados fictícios para demonstração
    const tableItems = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma'
      }
    ])
    
    const listItems = ref([
      {
        id: 1,
        name: 'Ácido Clorídrico',
        category: 'Ácidos',
        quantity: 25,
        unit: 'Litro',
        status: 'Ativo'
      },
      {
        id: 2,
        name: 'Etanol 96%',
        category: 'Álcoois',
        quantity: 10,
        unit: 'Litro',
        status: 'Expirando'
      },
      {
        id: 3,
        name: 'Sulfato de Cobre',
        category: 'Sais',
        quantity: 5,
        unit: 'Kilograma',
        status: 'Ativo'
      },
      {
        id: 4,
        name: 'Ácido Nítrico',
        category: 'Ácidos',
        quantity: 15,
        unit: 'Litro',
        status: 'Ativo'
      }
    ])
    
    // Métodos
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Ativo': return 'success'
        case 'Expirando': return 'warning'
        case 'Expirado': return 'error'
        default: return 'default'
      }
    }
    
    const toggleSkeletonLoaders = () => {
      skeletonLoadersEnabled.value = !skeletonLoadersEnabled.value
    }
    
    const updateSkeletonSettings = () => {
      // Atualizar configurações dos skeleton loaders
      console.log('Atualizando configurações dos skeleton loaders:', skeletonSettings.value)
    }
    
    const simulateLoading = () => {
      if (loading.value) return
      
      loading.value = true
      
      // Simular carregamento por um tempo determinado
      setTimeout(() => {
        loading.value = false
      }, loadingTime.value)
    }
    
    const stopLoading = () => {
      loading.value = false
    }
    
    return {
      skeletonLoadersEnabled,
      loading,
      loadingTime,
      skeletonSettings,
      animationDurationOptions,
      baseColorOptions,
      highlightColorOptions,
      loadingTimeOptions,
      tableItems,
      listItems,
      getStatusVariant,
      toggleSkeletonLoaders,
      updateSkeletonSettings,
      simulateLoading,
      stopLoading
    }
  }
}
</script>