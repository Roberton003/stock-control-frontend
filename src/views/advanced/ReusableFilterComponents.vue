<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Componentes de Filtro Reutilizáveis</h1>
      <Button variant="primary" @click="toggleReusableFilters">
        <Icon :name="reusableFiltersEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ reusableFiltersEnabled ? 'Desativar' : 'Ativar' }} Filtros Reutilizáveis
      </Button>
    </div>
    
    <!-- Configurações dos componentes de filtro -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações dos Componentes de Filtro</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tema</label>
          <Select 
            v-model="filterSettings.theme" 
            :options="themeOptions" 
            placeholder="Selecione um tema" 
            @change="updateFilterSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Posição</label>
          <Select 
            v-model="filterSettings.position" 
            :options="positionOptions" 
            placeholder="Selecione uma posição" 
            @change="updateFilterSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Comportamento</label>
          <Select 
            v-model="filterSettings.behavior" 
            :options="behaviorOptions" 
            placeholder="Selecione um comportamento" 
            @change="updateFilterSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de uso dos componentes de filtro -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Uso dos Componentes de Filtro</h2>
          <Badge :variant="reusableFiltersEnabled ? 'success' : 'default'">
            {{ reusableFiltersEnabled ? 'Ativados' : 'Desativados' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Filtros aplicados -->
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Filtros Aplicados</h3>
            <div v-if="appliedFilters.length" class="flex flex-wrap gap-2">
              <Badge 
                v-for="(filter, index) in appliedFilters" 
                :key="index" 
                variant="primary" 
                class="mr-2 mb-2"
              >
                {{ filter.label }}: {{ filter.value }}
                <Button variant="outline" size="sm" class="ml-2" @click="removeAppliedFilter(index)">
                  <Icon name="times" />
                </Button>
              </Badge>
            </div>
            <div v-else class="text-gray-500">
              Nenhum filtro aplicado no momento.
            </div>
          </div>
          
          <!-- Componentes de filtro reutilizáveis -->
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Componentes de Filtro Reutilizáveis</h3>
            <div class="space-y-4">
              <ReusableFilter 
                v-model="filters.search" 
                type="search" 
                label="Busca" 
                placeholder="Digite sua busca..." 
                @change="applyFilters"
              />
              
              <ReusableFilter 
                v-model="filters.category" 
                type="select" 
                label="Categoria" 
                :options="categories" 
                placeholder="Selecione uma categoria" 
                @change="applyFilters"
              />
              
              <ReusableFilter 
                v-model="filters.status" 
                type="multi-select" 
                label="Status" 
                :options="statuses" 
                placeholder="Selecione os status" 
                @change="applyFilters"
              />
              
              <ReusableFilter 
                v-model="filters.dateRange" 
                type="date-range" 
                label="Período" 
                @change="applyFilters"
              />
              
              <ReusableFilter 
                v-model="filters.quantity" 
                type="number-range" 
                label="Quantidade" 
                :min="0" 
                :max="1000" 
                @change="applyFilters"
              />
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button variant="outline" @click="clearFilters">
            <Icon name="undo" class="mr-2" />
            Limpar Filtros
          </Button>
          <Button variant="primary" @click="applyFilters">
            <Icon name="filter" class="mr-2" />
            Aplicar Filtros
          </Button>
        </div>
      </template>
    </Card>
    
    <!-- Demonstração dos filtros em diferentes contextos -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Demonstração dos Filtros em Diferentes Contextos</h2>
      </template>
      
      <div class="p-4">
        <Tabs v-model="activeTab" :tabs="filterTabs">
          <!-- Aba de reagentes -->
          <TabPanel name="reagents">
            <div class="space-y-4">
              <h3 class="text-md font-medium text-gray-900">Filtros para Reagentes</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <ReusableFilter 
                  v-model="reagentFilters.name" 
                  type="search" 
                  label="Nome" 
                  placeholder="Buscar reagente..." 
                  @change="applyReagentFilters"
                />
                
                <ReusableFilter 
                  v-model="reagentFilters.category" 
                  type="select" 
                  label="Categoria" 
                  :options="categories" 
                  placeholder="Selecione uma categoria" 
                  @change="applyReagentFilters"
                />
                
                <ReusableFilter 
                  v-model="reagentFilters.status" 
                  type="select" 
                  label="Status" 
                  :options="reagentStatuses" 
                  placeholder="Selecione um status" 
                  @change="applyReagentFilters"
                />
              </div>
            </div>
          </TabPanel>
          
          <!-- Aba de lotes -->
          <TabPanel name="stock-lots">
            <div class="space-y-4">
              <h3 class="text-md font-medium text-gray-900">Filtros para Lotes de Estoque</h3>
              <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <ReusableFilter 
                  v-model="stockLotFilters.reagent" 
                  type="select" 
                  label="Reagente" 
                  :options="reagents" 
                  placeholder="Selecione um reagente" 
                  @change="applyStockLotFilters"
                />
                
                <ReusableFilter 
                  v-model="stockLotFilters.expiryStatus" 
                  type="select" 
                  label="Status de Validade" 
                  :options="expiryStatuses" 
                  placeholder="Selecione um status" 
                  @change="applyStockLotFilters"
                />
                
                <ReusableFilter 
                  v-model="stockLotFilters.supplier" 
                  type="select" 
                  label="Fornecedor" 
                  :options="suppliers" 
                  placeholder="Selecione um fornecedor" 
                  @change="applyStockLotFilters"
                />
                
                <ReusableFilter 
                  v-model="stockLotFilters.location" 
                  type="select" 
                  label="Localização" 
                  :options="locations" 
                  placeholder="Selecione uma localização" 
                  @change="applyStockLotFilters"
                />
              </div>
            </div>
          </TabPanel>
          
          <!-- Aba de requisições -->
          <TabPanel name="requisitions">
            <div class="space-y-4">
              <h3 class="text-md font-medium text-gray-900">Filtros para Requisições</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <ReusableFilter 
                  v-model="requisitionFilters.requester" 
                  type="search" 
                  label="Solicitante" 
                  placeholder="Buscar solicitante..." 
                  @change="applyRequisitionFilters"
                />
                
                <ReusableFilter 
                  v-model="requisitionFilters.status" 
                  type="select" 
                  label="Status" 
                  :options="requisitionStatuses" 
                  placeholder="Selecione um status" 
                  @change="applyRequisitionFilters"
                />
                
                <ReusableFilter 
                  v-model="requisitionFilters.dateRange" 
                  type="date-range" 
                  label="Período" 
                  @change="applyRequisitionFilters"
                />
              </div>
            </div>
          </TabPanel>
        </Tabs>
      </div>
    </Card>
    
    <!-- Informações sobre componentes de filtro reutilizáveis -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Componentes de Filtro Reutilizáveis</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios dos Componentes de Filtro Reutilizáveis</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Reduzem a duplicação de código em diferentes partes da aplicação</li>
              <li>Facilitam a manutenção e atualização dos filtros</li>
              <li>Garantem uma experiência de usuário consistente</li>
              <li>Permitem fácil customização através de props</li>
              <li>Aceleram o desenvolvimento de novas funcionalidades</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Filtros Reutilizáveis:</span>
                <span>{{ reusableFiltersEnabled ? 'Ativados' : 'Desativados' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Tema:</span>
                <span>{{ filterSettings.theme }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Posição:</span>
                <span>{{ filterSettings.position }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Comportamento:</span>
                <span>{{ filterSettings.behavior }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Filtros Aplicados:</span>
                <span>{{ appliedFilters.length }}</span>
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
import Tabs from '@/components/ui/Tabs.vue'
import TabPanel from '@/components/ui/TabPanel.vue'
import ReusableFilter from '@/components/filters/ReusableFilter.vue'

export default {
  name: 'ReusableFilterComponents',
  components: {
    Card,
    Button,
    Select,
    Icon,
    Badge,
    Tabs,
    TabPanel,
    ReusableFilter
  },
  setup() {
    // Estados
    const reusableFiltersEnabled = ref(true)
    const activeTab = ref('reagents')
    
    // Configurações dos filtros
    const filterSettings = ref({
      theme: 'light',
      position: 'top',
      behavior: 'auto'
    })
    
    // Filtros gerais
    const filters = ref({
      search: '',
      category: '',
      status: [],
      dateRange: { start: '', end: '' },
      quantity: { min: 0, max: 1000 }
    })
    
    // Filtros específicos por contexto
    const reagentFilters = ref({
      name: '',
      category: '',
      status: ''
    })
    
    const stockLotFilters = ref({
      reagent: '',
      expiryStatus: '',
      supplier: '',
      location: ''
    })
    
    const requisitionFilters = ref({
      requester: '',
      status: '',
      dateRange: { start: '', end: '' }
    })
    
    // Filtros aplicados
    const appliedFilters = ref([])
    
    // Opções para seletores
    const themeOptions = ref([
      { value: 'light', label: 'Claro' },
      { value: 'dark', label: 'Escuro' },
      { value: 'blue', label: 'Azul' },
      { value: 'green', label: 'Verde' }
    ])
    
    const positionOptions = ref([
      { value: 'top', label: 'Superior' },
      { value: 'bottom', label: 'Inferior' },
      { value: 'left', label: 'Esquerda' },
      { value: 'right', label: 'Direita' }
    ])
    
    const behaviorOptions = ref([
      { value: 'auto', label: 'Automático' },
      { value: 'manual', label: 'Manual' },
      { value: 'instant', label: 'Instantâneo' }
    ])
    
    const filterTabs = ref([
      { name: 'reagents', label: 'Reagentes' },
      { name: 'stock-lots', label: 'Lotes de Estoque' },
      { name: 'requisitions', label: 'Requisições' }
    ])
    
    // Dados fictícios para seletores
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
    
    const reagentStatuses = ref([
      { value: 'available', label: 'Disponível' },
      { value: 'low-stock', label: 'Estoque Baixo' },
      { value: 'out-of-stock', label: 'Sem Estoque' }
    ])
    
    const expiryStatuses = ref([
      { value: 'valid', label: 'Válido' },
      { value: 'near-expiry', label: 'Próximo ao Vencimento' },
      { value: 'expired', label: 'Vencido' }
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
    
    const requisitionStatuses = ref([
      { value: 'pending', label: 'Pendente' },
      { value: 'approved', label: 'Aprovada' },
      { value: 'rejected', label: 'Rejeitada' },
      { value: 'completed', label: 'Concluída' }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' },
      { value: 4, label: 'Ácido Nítrico' },
      { value: 5, label: 'Hidróxido de Sódio' }
    ])
    
    // Métodos
    const toggleReusableFilters = () => {
      reusableFiltersEnabled.value = !reusableFiltersEnabled.value
    }
    
    const updateFilterSettings = () => {
      // Atualizar configurações dos componentes de filtro
      console.log('Atualizando configurações dos filtros:', filterSettings.value)
    }
    
    const applyFilters = () => {
      // Aplicar filtros gerais
      console.log('Aplicando filtros:', filters.value)
      
      // Converter filtros em formato de lista para exibição
      appliedFilters.value = []
      
      if (filters.value.search) {
        appliedFilters.value.push({ label: 'Busca', value: filters.value.search })
      }
      
      if (filters.value.category) {
        const category = categories.value.find(c => c.value === filters.value.category)
        if (category) {
          appliedFilters.value.push({ label: 'Categoria', value: category.label })
        }
      }
      
      if (filters.value.status.length) {
        appliedFilters.value.push({ label: 'Status', value: filters.value.status.join(', ') })
      }
      
      if (filters.value.dateRange.start || filters.value.dateRange.end) {
        appliedFilters.value.push({ 
          label: 'Período', 
          value: `${filters.value.dateRange.start || '...'} até ${filters.value.dateRange.end || '...'}`
        })
      }
      
      if (filters.value.quantity.min > 0 || filters.value.quantity.max < 1000) {
        appliedFilters.value.push({ 
          label: 'Quantidade', 
          value: `${filters.value.quantity.min} - ${filters.value.quantity.max}`
        })
      }
    }
    
    const applyReagentFilters = () => {
      // Aplicar filtros específicos para reagentes
      console.log('Aplicando filtros para reagentes:', reagentFilters.value)
    }
    
    const applyStockLotFilters = () => {
      // Aplicar filtros específicos para lotes de estoque
      console.log('Aplicando filtros para lotes de estoque:', stockLotFilters.value)
    }
    
    const applyRequisitionFilters = () => {
      // Aplicar filtros específicos para requisições
      console.log('Aplicando filtros para requisições:', requisitionFilters.value)
    }
    
    const clearFilters = () => {
      // Limpar todos os filtros
      filters.value = {
        search: '',
        category: '',
        status: [],
        dateRange: { start: '', end: '' },
        quantity: { min: 0, max: 1000 }
      }
      
      reagentFilters.value = {
        name: '',
        category: '',
        status: ''
      }
      
      stockLotFilters.value = {
        reagent: '',
        expiryStatus: '',
        supplier: '',
        location: ''
      }
      
      requisitionFilters.value = {
        requester: '',
        status: '',
        dateRange: { start: '', end: '' }
      }
      
      appliedFilters.value = []
    }
    
    const removeAppliedFilter = (index) => {
      // Remover um filtro aplicado específico
      appliedFilters.value.splice(index, 1)
    }
    
    return {
      reusableFiltersEnabled,
      activeTab,
      filterSettings,
      filters,
      reagentFilters,
      stockLotFilters,
      requisitionFilters,
      appliedFilters,
      themeOptions,
      positionOptions,
      behaviorOptions,
      filterTabs,
      categories,
      statuses,
      reagentStatuses,
      expiryStatuses,
      suppliers,
      locations,
      requisitionStatuses,
      reagents,
      toggleReusableFilters,
      updateFilterSettings,
      applyFilters,
      applyReagentFilters,
      applyStockLotFilters,
      applyRequisitionFilters,
      clearFilters,
      removeAppliedFilter
    }
  }
}
</script>