<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Filtros de Relatórios</h1>
      <Button variant="primary" @click="applyFilters">
        <Icon name="filter" class="mr-2" />
        Aplicar Filtros
      </Button>
    </div>
    
    <!-- Filtros por período -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Filtros por Período</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data Inicial *</label>
          <Input v-model="filters.startDate" type="date" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data Final *</label>
          <Input v-model="filters.endDate" type="date" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Período Pré-definido</label>
          <Select 
            v-model="filters.presetPeriod" 
            :options="presetPeriods" 
            placeholder="Selecione um período"
            @change="applyPresetPeriod"
          />
        </div>
      </div>
    </Card>
    
    <!-- Filtros por usuário -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Filtros por Usuário</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Usuário</label>
          <Select 
            v-model="filters.user" 
            :options="users" 
            placeholder="Selecione um usuário"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Departamento</label>
          <Select 
            v-model="filters.department" 
            :options="departments" 
            placeholder="Selecione um departamento"
          />
        </div>
      </div>
    </Card>
    
    <!-- Filtros por reagente -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Filtros por Reagente</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Reagente</label>
          <Select 
            v-model="filters.reagent" 
            :options="reagents" 
            placeholder="Selecione um reagente"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
          <Select 
            v-model="filters.category" 
            :options="categories" 
            placeholder="Selecione uma categoria"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fornecedor</label>
          <Select 
            v-model="filters.supplier" 
            :options="suppliers" 
            placeholder="Selecione um fornecedor"
          />
        </div>
      </div>
    </Card>
    
    <!-- Filtros avançados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Filtros Avançados</h2>
          <Button variant="outline" size="sm" @click="toggleAdvancedFilters">
            <Icon :name="showAdvancedFilters ? 'chevron-up' : 'chevron-down'" class="mr-2" />
            {{ showAdvancedFilters ? 'Ocultar' : 'Mostrar' }}
          </Button>
        </div>
      </template>
      
      <div v-show="showAdvancedFilters" class="grid grid-cols-1 md:grid-cols-2 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
          <Select 
            v-model="filters.location" 
            :options="locations" 
            placeholder="Selecione uma localização"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status do Lote</label>
          <Select 
            v-model="filters.lotStatus" 
            :options="lotStatuses" 
            placeholder="Selecione um status"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Movimentação</label>
          <Select 
            v-model="filters.movementType" 
            :options="movementTypes" 
            placeholder="Selecione um tipo"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Lote Próximo ao Vencimento</label>
          <Select 
            v-model="filters.nearExpiry" 
            :options="nearExpiryOptions" 
            placeholder="Selecione uma opção"
          />
        </div>
      </div>
    </Card>
    
    <!-- Ações -->
    <div class="flex justify-end space-x-4">
      <Button variant="outline" @click="resetFilters">
        <Icon name="undo" class="mr-2" />
        Limpar Filtros
      </Button>
      <Button variant="primary" @click="applyFilters">
        <Icon name="check" class="mr-2" />
        Aplicar Filtros
      </Button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Icon from '@/components/ui/Icon.vue'

export default {
  name: 'ReportFilters',
  components: {
    Card,
    Button,
    Input,
    Select,
    Icon
  },
  setup() {
    // Estados
    const showAdvancedFilters = ref(false)
    
    // Filtros
    const filters = ref({
      startDate: '',
      endDate: '',
      presetPeriod: '',
      user: '',
      department: '',
      reagent: '',
      category: '',
      supplier: '',
      location: '',
      lotStatus: '',
      movementType: '',
      nearExpiry: ''
    })
    
    // Opções para seletores
    const presetPeriods = ref([
      { value: 'today', label: 'Hoje' },
      { value: 'yesterday', label: 'Ontem' },
      { value: 'lastWeek', label: 'Última Semana' },
      { value: 'lastMonth', label: 'Último Mês' },
      { value: 'lastQuarter', label: 'Último Trimestre' },
      { value: 'lastYear', label: 'Último Ano' },
      { value: 'custom', label: 'Personalizado' }
    ])
    
    const users = ref([
      { value: 1, label: 'João Silva' },
      { value: 2, label: 'Maria Oliveira' },
      { value: 3, label: 'Pedro Santos' },
      { value: 4, label: 'Ana Costa' },
      { value: 5, label: 'Carlos Mendes' }
    ])
    
    const departments = ref([
      { value: 1, label: 'Química' },
      { value: 2, label: 'Biologia' },
      { value: 3, label: 'Física' },
      { value: 4, label: 'Matemática' },
      { value: 5, label: 'Computação' }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' },
      { value: 4, label: 'Ácido Nítrico' },
      { value: 5, label: 'Hidróxido de Sódio' }
    ])
    
    const categories = ref([
      { value: 1, label: 'Ácidos' },
      { value: 2, label: 'Bases' },
      { value: 3, label: 'Sais' },
      { value: 4, label: 'Álcoois' },
      { value: 5, label: 'Indicadores' }
    ])
    
    const suppliers = ref([
      { value: 1, label: 'LabQuímica Ltda' },
      { value: 2, label: 'Química Brasil' },
      { value: 3, label: 'Laboratórios ABC' },
      { value: 4, label: 'Reagentes SA' },
      { value: 5, label: 'Produtos Químicos Ltda' }
    ])
    
    const locations = ref([
      { value: 1, label: 'Armário A1' },
      { value: 2, label: 'Armário B2' },
      { value: 3, label: 'Prateleira C3' },
      { value: 4, label: 'Sala D4' },
      { value: 5, label: 'Laboratório E5' }
    ])
    
    const lotStatuses = ref([
      { value: 'active', label: 'Ativo' },
      { value: 'expiring', label: 'Expirando' },
      { value: 'expired', label: 'Expirado' },
      { value: 'inactive', label: 'Inativo' }
    ])
    
    const movementTypes = ref([
      { value: 'entry', label: 'Entrada' },
      { value: 'exit', label: 'Saída' },
      { value: 'transfer', label: 'Transferência' },
      { value: 'adjustment', label: 'Ajuste' }
    ])
    
    const nearExpiryOptions = ref([
      { value: 'all', label: 'Todos' },
      { value: 'yes', label: 'Sim' },
      { value: 'no', label: 'Não' }
    ])
    
    // Métodos
    const toggleAdvancedFilters = () => {
      showAdvancedFilters.value = !showAdvancedFilters.value
    }
    
    const applyPresetPeriod = (period) => {
      const today = new Date()
      
      switch (period) {
        case 'today':
          filters.value.startDate = formatDate(today)
          filters.value.endDate = formatDate(today)
          break
        case 'yesterday':
          const yesterday = new Date(today)
          yesterday.setDate(yesterday.getDate() - 1)
          filters.value.startDate = formatDate(yesterday)
          filters.value.endDate = formatDate(yesterday)
          break
        case 'lastWeek':
          const lastWeek = new Date(today)
          lastWeek.setDate(lastWeek.getDate() - 7)
          filters.value.startDate = formatDate(lastWeek)
          filters.value.endDate = formatDate(today)
          break
        case 'lastMonth':
          const lastMonth = new Date(today)
          lastMonth.setMonth(lastMonth.getMonth() - 1)
          filters.value.startDate = formatDate(lastMonth)
          filters.value.endDate = formatDate(today)
          break
        case 'lastQuarter':
          const lastQuarter = new Date(today)
          lastQuarter.setMonth(lastQuarter.getMonth() - 3)
          filters.value.startDate = formatDate(lastQuarter)
          filters.value.endDate = formatDate(today)
          break
        case 'lastYear':
          const lastYear = new Date(today)
          lastYear.setFullYear(lastYear.getFullYear() - 1)
          filters.value.startDate = formatDate(lastYear)
          filters.value.endDate = formatDate(today)
          break
        case 'custom':
          // Manter datas personalizadas
          break
      }
    }
    
    const formatDate = (date) => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }
    
    const resetFilters = () => {
      filters.value = {
        startDate: '',
        endDate: '',
        presetPeriod: '',
        user: '',
        department: '',
        reagent: '',
        category: '',
        supplier: '',
        location: '',
        lotStatus: '',
        movementType: '',
        nearExpiry: ''
      }
    }
    
    const applyFilters = () => {
      // Lógica para aplicar os filtros
      console.log('Aplicando filtros:', filters.value)
    }
    
    return {
      showAdvancedFilters,
      filters,
      presetPeriods,
      users,
      departments,
      reagents,
      categories,
      suppliers,
      locations,
      lotStatuses,
      movementTypes,
      nearExpiryOptions,
      toggleAdvancedFilters,
      applyPresetPeriod,
      resetFilters,
      applyFilters
    }
  }
}
</script>