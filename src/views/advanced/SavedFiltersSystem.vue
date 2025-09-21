<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Sistema de Filtros Salvos</h1>
      <Button variant="primary" @click="toggleSavedFilters">
        <Icon :name="savedFiltersEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ savedFiltersEnabled ? 'Desativar' : 'Ativar' }} Filtros Salvos
      </Button>
    </div>
    
    <!-- Configurações do sistema de filtros salvos -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações do Sistema de Filtros Salvos</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Filtro Padrão</label>
          <Input 
            v-model="filterSettings.defaultFilterName" 
            placeholder="Nome do filtro padrão" 
            @input="updateFilterSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Auto-salvar Filtros</label>
          <Toggle 
            v-model="filterSettings.autoSave" 
            label="Salvar filtros automaticamente" 
            @change="updateFilterSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Notificar ao Salvar</label>
          <Toggle 
            v-model="filterSettings.notifyOnSave" 
            label="Mostrar notificação ao salvar filtro" 
            @change="updateFilterSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de uso do sistema de filtros salvos -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Uso do Sistema de Filtros Salvos</h2>
          <Badge :variant="savedFiltersEnabled ? 'success' : 'default'">
            {{ savedFiltersEnabled ? 'Ativado' : 'Desativado' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Filtros ativos -->
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Filtros Ativos</h3>
            <div v-if="activeFilters.length" class="flex flex-wrap gap-2">
              <Badge 
                v-for="(filter, index) in activeFilters" 
                :key="index" 
                variant="primary" 
                class="mr-2 mb-2"
              >
                {{ filter.label }}: {{ filter.value }}
                <Button variant="outline" size="sm" class="ml-2" @click="removeActiveFilter(index)">
                  <Icon name="times" />
                </Button>
              </Badge>
            </div>
            <div v-else class="text-gray-500">
              Nenhum filtro ativo no momento.
            </div>
          </div>
          
          <!-- Filtros salvos -->
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Filtros Salvos</h3>
            <div v-if="savedFilters.length" class="space-y-2">
              <div 
                v-for="(savedFilter, index) in savedFilters" 
                :key="index" 
                class="flex justify-between items-center p-2 border border-gray-200 rounded hover:bg-gray-50"
              >
                <span class="text-sm font-medium text-gray-900">{{ savedFilter.name }}</span>
                <div class="flex space-x-1">
                  <Button variant="outline" size="sm" @click="applySavedFilter(savedFilter)">
                    <Icon name="play" />
                  </Button>
                  <Button variant="outline" size="sm" @click="editSavedFilter(savedFilter, index)">
                    <Icon name="edit" />
                  </Button>
                  <Button variant="outline" size="sm" @click="deleteSavedFilter(index)">
                    <Icon name="trash" />
                  </Button>
                </div>
              </div>
            </div>
            <div v-else class="text-gray-500">
              Nenhum filtro salvo ainda. Crie seu primeiro filtro!
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button variant="outline" @click="clearAllFilters">
            <Icon name="undo" class="mr-2" />
            Limpar Todos os Filtros
          </Button>
          <Button variant="primary" @click="saveCurrentFilters">
            <Icon name="save" class="mr-2" />
            Salvar Filtros Atuais
          </Button>
        </div>
      </template>
    </Card>
    
    <!-- Componentes de filtro reutilizáveis -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Componentes de Filtro Reutilizáveis</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Filtro de Texto</label>
            <Input 
              v-model="filterComponents.textFilter" 
              placeholder="Digite para filtrar..." 
              type="search"
              @input="applyTextFilter"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Filtro de Categoria</label>
            <Select 
              v-model="filterComponents.categoryFilter" 
              :options="categories" 
              placeholder="Selecione uma categoria"
              @change="applyCategoryFilter"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Filtro de Status</label>
            <Select 
              v-model="filterComponents.statusFilter" 
              :options="statuses" 
              placeholder="Selecione um status"
              @change="applyStatusFilter"
            />
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Lista de itens filtrados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Lista de Itens Filtrados</h2>
          <Badge variant="primary">
            {{ filteredItems.length }} itens encontrados
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
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in filteredItems" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getStatusVariant(item.status)">
                  {{ item.status }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
    
    <!-- Modal para salvar/editar filtros -->
    <Modal :visible="showFilterModal" @close="closeFilterModal">
      <template #header>
        <h3 class="text-lg font-medium">
          {{ editingFilterIndex !== null ? 'Editar Filtro Salvo' : 'Salvar Novo Filtro' }}
        </h3>
      </template>
      
      <form @submit.prevent="saveFilter">
        <div class="grid grid-cols-1 gap-6 p-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Filtro *</label>
            <Input 
              v-model="filterForm.name" 
              placeholder="Digite um nome para o filtro" 
              required
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea 
              v-model="filterForm.description" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Descreva para que serve este filtro"
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Filtros Ativos</label>
            <div v-if="activeFilters.length" class="flex flex-wrap gap-2">
              <Badge 
                v-for="(filter, index) in activeFilters" 
                :key="index" 
                variant="primary" 
                class="mr-2 mb-2"
              >
                {{ filter.label }}: {{ filter.value }}
              </Badge>
            </div>
            <div v-else class="text-gray-500">
              Nenhum filtro ativo para salvar.
            </div>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeFilterModal">Cancelar</Button>
        <Button 
          variant="primary" 
          @click="saveFilter" 
          :disabled="!filterForm.name || !activeFilters.length"
        >
          {{ editingFilterIndex !== null ? 'Atualizar' : 'Salvar' }}
        </Button>
      </template>
    </Modal>
    
    <!-- Informações sobre o sistema de filtros salvos -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre o Sistema de Filtros Salvos</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios do Sistema de Filtros Salvos</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Permite aos usuários salvar combinações de filtros frequentemente usadas</li>
              <li>Reduz o tempo necessário para aplicar filtros complexos repetidamente</li>
              <li>Melhora a produtividade ao eliminar a necessidade de redefinir filtros</li>
              <li>Facilita o compartilhamento de vistas filtradas entre usuários</li>
              <li>Permite criar vistas personalizadas para diferentes perfis de usuário</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Filtros Salvos:</span>
                <span>{{ savedFiltersEnabled ? 'Ativados' : 'Desativados' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Nome do Filtro Padrão:</span>
                <span>{{ filterSettings.defaultFilterName || 'Não definido' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Auto-salvar Filtros:</span>
                <span>{{ filterSettings.autoSave ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Notificar ao Salvar:</span>
                <span>{{ filterSettings.notifyOnSave ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Filtros Ativos:</span>
                <span>{{ activeFilters.length }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Filtros Salvos:</span>
                <span>{{ savedFilters.length }}</span>
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
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'
import Toggle from '@/components/ui/Toggle.vue'

export default {
  name: 'SavedFiltersSystem',
  components: {
    Card,
    Button,
    Input,
    Select,
    Modal,
    Icon,
    Badge,
    Toggle
  },
  setup() {
    // Estados
    const savedFiltersEnabled = ref(true)
    const showFilterModal = ref(false)
    const editingFilterIndex = ref(null)
    
    // Configurações do sistema de filtros salvos
    const filterSettings = ref({
      defaultFilterName: 'Filtro Padrão',
      autoSave: true,
      notifyOnSave: true
    })
    
    // Filtros ativos
    const activeFilters = ref([])
    
    // Filtros salvos
    const savedFilters = ref([
      {
        id: 1,
        name: 'Ácidos em estoque baixo',
        description: 'Lista de ácidos com quantidade abaixo do mínimo',
        filters: [
          { label: 'Categoria', value: 'Ácidos' },
          { label: 'Quantidade Mínima', value: '10' }
        ],
        createdAt: '2023-09-15T14:30:00',
        updatedAt: '2023-09-15T14:30:00'
      },
      {
        id: 2,
        name: 'Reagentes próximos ao vencimento',
        description: 'Lista de reagentes que expiram em menos de 30 dias',
        filters: [
          { label: 'Validade', value: '< 30 dias' }
        ],
        createdAt: '2023-09-10T09:15:00',
        updatedAt: '2023-09-12T11:45:00'
      }
    ])
    
    // Componentes de filtro
    const filterComponents = ref({
      textFilter: '',
      categoryFilter: '',
      statusFilter: ''
    })
    
    // Formulário de filtro
    const filterForm = ref({
      name: '',
      description: ''
    })
    
    // Dados fictícios para demonstração
    const allItems = ref([
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
      },
      {
        id: 5,
        name: 'Hidróxido de Sódio',
        category: 'Bases',
        quantity: 8,
        unit: 'Kilograma',
        status: 'Ativo'
      }
    ])
    
    // Itens filtrados
    const filteredItems = computed(() => {
      return allItems.value.filter(item => {
        // Aplicar filtro de texto
        if (filterComponents.value.textFilter && 
            !item.name.toLowerCase().includes(filterComponents.value.textFilter.toLowerCase())) {
          return false
        }
        
        // Aplicar filtro de categoria
        if (filterComponents.value.categoryFilter && 
            item.category !== filterComponents.value.categoryFilter) {
          return false
        }
        
        // Aplicar filtro de status
        if (filterComponents.value.statusFilter && 
            item.status !== filterComponents.value.statusFilter) {
          return false
        }
        
        return true
      })
    })
    
    // Opções para seletores
    const categories = ref([
      { value: 'Ácidos', label: 'Ácidos' },
      { value: 'Bases', label: 'Bases' },
      { value: 'Sais', label: 'Sais' },
      { value: 'Álcoois', label: 'Álcoois' },
      { value: 'Indicadores', label: 'Indicadores' }
    ])
    
    const statuses = ref([
      { value: 'Ativo', label: 'Ativo' },
      { value: 'Expirando', label: 'Expirando' },
      { value: 'Expirado', label: 'Expirado' },
      { value: 'Inativo', label: 'Inativo' }
    ])
    
    // Métodos
    const toggleSavedFilters = () => {
      savedFiltersEnabled.value = !savedFiltersEnabled.value
    }
    
    const updateFilterSettings = () => {
      // Atualizar configurações do sistema de filtros salvos
      console.log('Atualizando configurações dos filtros salvos:', filterSettings.value)
    }
    
    const applyTextFilter = () => {
      // Aplicar filtro de texto
      console.log('Aplicando filtro de texto:', filterComponents.value.textFilter)
      
      // Adicionar filtro à lista de filtros ativos
      const textFilterIndex = activeFilters.value.findIndex(f => f.label === 'Texto')
      if (filterComponents.value.textFilter) {
        if (textFilterIndex === -1) {
          activeFilters.value.push({ label: 'Texto', value: filterComponents.value.textFilter })
        } else {
          activeFilters.value[textFilterIndex].value = filterComponents.value.textFilter
        }
      } else if (textFilterIndex !== -1) {
        activeFilters.value.splice(textFilterIndex, 1)
      }
    }
    
    const applyCategoryFilter = () => {
      // Aplicar filtro de categoria
      console.log('Aplicando filtro de categoria:', filterComponents.value.categoryFilter)
      
      // Adicionar filtro à lista de filtros ativos
      const categoryFilterIndex = activeFilters.value.findIndex(f => f.label === 'Categoria')
      if (filterComponents.value.categoryFilter) {
        if (categoryFilterIndex === -1) {
          activeFilters.value.push({ label: 'Categoria', value: filterComponents.value.categoryFilter })
        } else {
          activeFilters.value[categoryFilterIndex].value = filterComponents.value.categoryFilter
        }
      } else if (categoryFilterIndex !== -1) {
        activeFilters.value.splice(categoryFilterIndex, 1)
      }
    }
    
    const applyStatusFilter = () => {
      // Aplicar filtro de status
      console.log('Aplicando filtro de status:', filterComponents.value.statusFilter)
      
      // Adicionar filtro à lista de filtros ativos
      const statusFilterIndex = activeFilters.value.findIndex(f => f.label === 'Status')
      if (filterComponents.value.statusFilter) {
        if (statusFilterIndex === -1) {
          activeFilters.value.push({ label: 'Status', value: filterComponents.value.statusFilter })
        } else {
          activeFilters.value[statusFilterIndex].value = filterComponents.value.statusFilter
        }
      } else if (statusFilterIndex !== -1) {
        activeFilters.value.splice(statusFilterIndex, 1)
      }
    }
    
    const removeActiveFilter = (index) => {
      // Remover filtro ativo
      const filter = activeFilters.value[index]
      
      // Limpar o componente de filtro correspondente
      switch (filter.label) {
        case 'Texto':
          filterComponents.value.textFilter = ''
          break
        case 'Categoria':
          filterComponents.value.categoryFilter = ''
          break
        case 'Status':
          filterComponents.value.statusFilter = ''
          break
      }
      
      // Remover da lista de filtros ativos
      activeFilters.value.splice(index, 1)
    }
    
    const clearAllFilters = () => {
      // Limpar todos os filtros
      filterComponents.value = {
        textFilter: '',
        categoryFilter: '',
        statusFilter: ''
      }
      
      activeFilters.value = []
    }
    
    const saveCurrentFilters = () => {
      // Abrir modal para salvar os filtros atuais
      if (!savedFiltersEnabled.value) return
      
      showFilterModal.value = true
      editingFilterIndex.value = null
      filterForm.value = {
        name: filterSettings.value.defaultFilterName,
        description: ''
      }
    }
    
    const applySavedFilter = (savedFilter) => {
      // Aplicar filtro salvo
      if (!savedFiltersEnabled.value) return
      
      console.log('Aplicando filtro salvo:', savedFilter)
      
      // Limpar filtros atuais
      clearAllFilters()
      
      // Aplicar filtros do filtro salvo
      savedFilter.filters.forEach(filter => {
        switch (filter.label) {
          case 'Texto':
            filterComponents.value.textFilter = filter.value
            applyTextFilter()
            break
          case 'Categoria':
            filterComponents.value.categoryFilter = filter.value
            applyCategoryFilter()
            break
          case 'Status':
            filterComponents.value.statusFilter = filter.value
            applyStatusFilter()
            break
        }
      })
    }
    
    const editSavedFilter = (savedFilter, index) => {
      // Editar filtro salvo
      if (!savedFiltersEnabled.value) return
      
      editingFilterIndex.value = index
      filterForm.value = {
        name: savedFilter.name,
        description: savedFilter.description
      }
      showFilterModal.value = true
    }
    
    const deleteSavedFilter = (index) => {
      // Excluir filtro salvo
      if (!savedFiltersEnabled.value) return
      
      console.log('Excluindo filtro salvo:', index)
      savedFilters.value.splice(index, 1)
    }
    
    const showFilterModal = () => {
      // Mostrar modal de filtro
      showFilterModal.value = true
    }
    
    const closeFilterModal = () => {
      // Fechar modal de filtro
      showFilterModal.value = false
      editingFilterIndex.value = null
      filterForm.value = {
        name: '',
        description: ''
      }
    }
    
    const saveFilter = () => {
      // Salvar filtro
      if (!savedFiltersEnabled.value || !filterForm.value.name || !activeFilters.value.length) return
      
      const newFilter = {
        id: Date.now(), // ID único para demonstração
        name: filterForm.value.name,
        description: filterForm.value.description,
        filters: [...activeFilters.value],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
      
      if (editingFilterIndex.value !== null) {
        // Atualizar filtro existente
        savedFilters.value[editingFilterIndex.value] = newFilter
      } else {
        // Adicionar novo filtro
        savedFilters.value.push(newFilter)
      }
      
      // Fechar modal
      closeFilterModal()
      
      // Mostrar notificação se configurado
      if (filterSettings.value.notifyOnSave) {
        console.log('Filtro salvo com sucesso!')
      }
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
    
    return {
      savedFiltersEnabled,
      showFilterModal,
      editingFilterIndex,
      filterSettings,
      activeFilters,
      savedFilters,
      filterComponents,
      filterForm,
      allItems,
      filteredItems,
      categories,
      statuses,
      toggleSavedFilters,
      updateFilterSettings,
      applyTextFilter,
      applyCategoryFilter,
      applyStatusFilter,
      removeActiveFilter,
      clearAllFilters,
      saveCurrentFilters,
      applySavedFilter,
      editSavedFilter,
      deleteSavedFilter,
      showFilterModal,
      closeFilterModal,
      saveFilter,
      getStatusVariant
    }
  }
}
</script>