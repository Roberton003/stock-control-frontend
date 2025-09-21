<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Sistema de Filtros Salvos</h1>
      <Button variant="primary" @click="openSaveFilterModal">
        <Icon name="save" class="mr-2" />
        Salvar Filtro
      </Button>
    </div>
    
    <!-- Filtros ativos -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Filtros Ativos</h2>
      </template>
      <div class="p-4">
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
    </Card>
    
    <!-- Lista de filtros salvos -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Filtros Salvos</h2>
      </template>
      
      <div class="overflow-x-auto p-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Filtros</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data de Criação</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(savedFilter, index) in savedFilters" :key="index" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ savedFilter.name }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <div class="flex flex-wrap gap-1">
                  <Badge 
                    v-for="(filter, filterIndex) in savedFilter.filters" 
                    :key="filterIndex" 
                    variant="secondary" 
                    class="mr-1 mb-1"
                  >
                    {{ filter.label }}: {{ filter.value }}
                  </Badge>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(savedFilter.createdAt) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button variant="secondary" size="sm" class="mr-2" @click="applySavedFilter(savedFilter)">
                  <Icon name="play" class="mr-1" />
                  Aplicar
                </Button>
                <Button variant="outline" size="sm" class="mr-2" @click="editSavedFilter(savedFilter, index)">
                  <Icon name="edit" />
                </Button>
                <Button variant="outline" size="sm" @click="deleteSavedFilter(index)">
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
          Mostrando <span class="font-medium">1</span> a <span class="font-medium">{{ savedFilters.length }}</span> de <span class="font-medium">{{ savedFilters.length }}</span> filtros salvos
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm" disabled>Anterior</Button>
          <Button variant="outline" size="sm" disabled>Próximo</Button>
        </div>
      </div>
    </Card>
    
    <!-- Modal de salvamento de filtros -->
    <Modal :visible="showSaveFilterModal" @close="closeSaveFilterModal">
      <template #header>
        <h3 class="text-lg font-medium">
          {{ editingFilterIndex !== null ? 'Editar Filtro Salvo' : 'Salvar Novo Filtro' }}
        </h3>
      </template>
      
      <form @submit.prevent="saveFilter">
        <div class="grid grid-cols-1 gap-6 p-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Filtro *</label>
            <Input v-model="saveFilterForm.name" placeholder="Digite um nome para o filtro" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea 
              v-model="saveFilterForm.description" 
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
        <Button variant="outline" @click="closeSaveFilterModal">Cancelar</Button>
        <Button variant="primary" @click="saveFilter" :disabled="!saveFilterForm.name || !activeFilters.length">
          {{ editingFilterIndex !== null ? 'Atualizar' : 'Salvar' }}
        </Button>
      </template>
    </Modal>
    
    <!-- Modal de confirmação de exclusão -->
    <Modal :visible="showDeleteConfirmModal" @close="closeDeleteConfirmModal">
      <template #header>
        <h3 class="text-lg font-medium">Confirmar Exclusão</h3>
      </template>
      
      <div class="p-4">
        <p class="text-gray-700">
          Tem certeza que deseja excluir o filtro salvo "<strong>{{ filterToDelete?.name }}</strong>"? 
          Esta ação não pode ser desfeita.
        </p>
      </div>
      
      <template #footer>
        <Button variant="outline" @click="closeDeleteConfirmModal">Cancelar</Button>
        <Button variant="error" @click="confirmDeleteFilter">Excluir</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'SavedFiltersSystem',
  components: {
    Card,
    Button,
    Input,
    Modal,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const showSaveFilterModal = ref(false)
    const showDeleteConfirmModal = ref(false)
    const editingFilterIndex = ref(null)
    const filterToDelete = ref(null)
    const deleteFilterIndex = ref(null)
    
    // Filtros ativos (simulando filtros aplicados na interface)
    const activeFilters = ref([
      { label: 'Nome', value: 'Ácido Clorídrico' },
      { label: 'Categoria', value: 'Ácidos' },
      { label: 'Quantidade Mínima', value: '10' }
    ])
    
    // Filtros salvos (simulando dados armazenados)
    const savedFilters = ref([
      {
        id: 1,
        name: 'Ácidos em estoque baixo',
        description: 'Lista de ácidos com quantidade abaixo do mínimo',
        filters: [
          { label: 'Categoria', value: 'Ácidos' },
          { label: 'Quantidade Mínima', value: '10' }
        ],
        createdAt: '2023-09-15T14:30:00'
      },
      {
        id: 2,
        name: 'Reagentes próximos ao vencimento',
        description: 'Lista de reagentes que expiram em menos de 30 dias',
        filters: [
          { label: 'Validade', value: '< 30 dias' }
        ],
        createdAt: '2023-09-10T09:15:00'
      },
      {
        id: 3,
        name: 'Reagentes de limpeza',
        description: 'Lista de reagentes usados para limpeza',
        filters: [
          { label: 'Categoria', value: 'Limpeza' }
        ],
        createdAt: '2023-09-05T11:45:00'
      }
    ])
    
    // Formulário de salvamento de filtros
    const saveFilterForm = ref({
      name: '',
      description: ''
    })
    
    // Métodos
    const openSaveFilterModal = () => {
      showSaveFilterModal.value = true
    }
    
    const closeSaveFilterModal = () => {
      showSaveFilterModal.value = false
      editingFilterIndex.value = null
      saveFilterForm.value = {
        name: '',
        description: ''
      }
    }
    
    const saveFilter = () => {
      if (!saveFilterForm.value.name || !activeFilters.value.length) return
      
      const newFilter = {
        id: Date.now(), // ID único para demonstração
        name: saveFilterForm.value.name,
        description: saveFilterForm.value.description,
        filters: [...activeFilters.value],
        createdAt: new Date().toISOString()
      }
      
      if (editingFilterIndex.value !== null) {
        // Atualizar filtro existente
        savedFilters.value[editingFilterIndex.value] = newFilter
      } else {
        // Adicionar novo filtro
        savedFilters.value.push(newFilter)
      }
      
      closeSaveFilterModal()
    }
    
    const applySavedFilter = (savedFilter) => {
      // Lógica para aplicar o filtro salvo
      console.log('Aplicando filtro salvo:', savedFilter)
      
      // Atualizar os filtros ativos com os filtros salvos
      activeFilters.value = [...savedFilter.filters]
    }
    
    const editSavedFilter = (savedFilter, index) => {
      editingFilterIndex.value = index
      saveFilterForm.value = {
        name: savedFilter.name,
        description: savedFilter.description
      }
      showSaveFilterModal.value = true
    }
    
    const deleteSavedFilter = (index) => {
      filterToDelete.value = savedFilters.value[index]
      deleteFilterIndex.value = index
      showDeleteConfirmModal.value = true
    }
    
    const closeDeleteConfirmModal = () => {
      showDeleteConfirmModal.value = false
      filterToDelete.value = null
      deleteFilterIndex.value = null
    }
    
    const confirmDeleteFilter = () => {
      if (deleteFilterIndex.value !== null) {
        savedFilters.value.splice(deleteFilterIndex.value, 1)
        closeDeleteConfirmModal()
      }
    }
    
    const removeActiveFilter = (index) => {
      activeFilters.value.splice(index, 1)
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    return {
      showSaveFilterModal,
      showDeleteConfirmModal,
      editingFilterIndex,
      filterToDelete,
      deleteFilterIndex,
      activeFilters,
      savedFilters,
      saveFilterForm,
      openSaveFilterModal,
      closeSaveFilterModal,
      saveFilter,
      applySavedFilter,
      editSavedFilter,
      deleteSavedFilter,
      closeDeleteConfirmModal,
      confirmDeleteFilter,
      removeActiveFilter,
      formatDate
    }
  }
}
</script>