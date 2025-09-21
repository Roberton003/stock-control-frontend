<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Detalhes do Lote</h1>
      <Button variant="primary" @click="editLot">
        <Icon name="edit" class="mr-2" />
        Editar Lote
      </Button>
    </div>
    
    <!-- Informações gerais -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações Gerais</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="text-sm font-medium text-gray-500">Número do Lote</h3>
          <p class="mt-1 text-sm text-gray-900">AC12345</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Reagente</h3>
          <p class="mt-1 text-sm text-gray-900">Ácido Clorídrico</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Quantidade</h3>
          <p class="mt-1 text-sm text-gray-900">25 Litros</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Data de Validade</h3>
          <p class="mt-1 text-sm text-gray-900">
            <Badge variant="success">31/12/2024</Badge>
          </p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Fornecedor</h3>
          <p class="mt-1 text-sm text-gray-900">LabQuímica Ltda</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Localização</h3>
          <p class="mt-1 text-sm text-gray-900">Armário A1</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Preço de Compra</h3>
          <p class="mt-1 text-sm text-gray-900">R$ 45,00 por litro</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Data de Compra</h3>
          <p class="mt-1 text-sm text-gray-900">15/03/2023</p>
        </div>
      </div>
    </Card>
    
    <!-- Status -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Status</h2>
      </template>
      <div class="flex items-center">
        <Badge variant="success" class="mr-4">Ativo</Badge>
        <div class="text-sm text-gray-500">
          <p>Restam 135 dias até o vencimento</p>
          <p class="mt-1">Quantidade suficiente em estoque</p>
        </div>
      </div>
    </Card>
    
    <!-- Histórico de movimentações -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Histórico de Movimentações</h2>
          <Button variant="outline" @click="addMovement">
            <Icon name="plus" class="mr-2" />
            Nova Movimentação
          </Button>
        </div>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuário</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Observações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="movement in movements" :key="movement.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(movement.date) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="movement.type === 'entry' ? 'success' : 'error'">
                  {{ movement.type === 'entry' ? 'Entrada' : 'Saída' }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ movement.quantity }} {{ movement.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ movement.user }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ movement.notes }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Paginação -->
      <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Mostrando <span class="font-medium">1</span> a <span class="font-medium">5</span> de <span class="font-medium">24</span> resultados
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm" disabled>Anterior</Button>
          <Button variant="outline" size="sm">Próximo</Button>
        </div>
      </div>
    </Card>
    
    <!-- Documentos associados -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Documentos Associados</h2>
      </template>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <Card class="border border-gray-200">
          <div class="p-4">
            <div class="flex items-center">
              <Icon name="file-pdf" class="text-red-500 text-xl mr-3" />
              <div>
                <h3 class="font-medium text-gray-900">Nota Fiscal #NF12345</h3>
                <p class="text-sm text-gray-500">PDF, 2.4 MB</p>
              </div>
            </div>
            <div class="mt-4 flex space-x-2">
              <Button variant="outline" size="sm">Visualizar</Button>
              <Button variant="outline" size="sm">Download</Button>
            </div>
          </div>
        </Card>
        
        <Card class="border border-gray-200">
          <div class="p-4">
            <div class="flex items-center">
              <Icon name="file-certificate" class="text-blue-500 text-xl mr-3" />
              <div>
                <h3 class="font-medium text-gray-900">Certificado de Qualidade</h3>
                <p class="text-sm text-gray-500">PDF, 1.8 MB</p>
              </div>
            </div>
            <div class="mt-4 flex space-x-2">
              <Button variant="outline" size="sm">Visualizar</Button>
              <Button variant="outline" size="sm">Download</Button>
            </div>
          </div>
        </Card>
      </div>
    </Card>
    
    <!-- Modal de edição -->
    <Modal :visible="showEditModal" @close="closeEditModal">
      <template #header>
        <h3 class="text-lg font-medium">Editar Lote</h3>
      </template>
      
      <form @submit.prevent="saveLot">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Número do Lote *</label>
            <Input v-model="editForm.lot_number" placeholder="Número do lote" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Reagente *</label>
            <Select v-model="editForm.reagent" :options="reagents" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade *</label>
            <Input v-model="editForm.quantity" type="number" placeholder="Quantidade" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unidade *</label>
            <Input v-model="editForm.unit" placeholder="Unidade" disabled />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Validade *</label>
            <Input v-model="editForm.expiry_date" type="date" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fornecedor</label>
            <Select v-model="editForm.supplier" :options="suppliers" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
            <Select v-model="editForm.location" :options="locations" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Preço de Compra</label>
            <Input v-model="editForm.purchase_price" type="number" step="0.01" placeholder="Preço de compra" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Compra</label>
            <Input v-model="editForm.purchase_date" type="date" />
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeEditModal">Cancelar</Button>
        <Button variant="primary" @click="saveLot">Salvar</Button>
      </template>
    </Modal>
    
    <!-- Modal de nova movimentação -->
    <Modal :visible="showMovementModal" @close="closeMovementModal">
      <template #header>
        <h3 class="text-lg font-medium">Nova Movimentação</h3>
      </template>
      
      <form @submit.prevent="saveMovement">
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
            <Select v-model="movementForm.type" :options="movementTypes" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade *</label>
            <Input v-model="movementForm.quantity" type="number" placeholder="Quantidade" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unidade</label>
            <Input v-model="movementForm.unit" placeholder="Unidade" disabled />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Usuário *</label>
            <Input v-model="movementForm.user" placeholder="Nome do usuário" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea 
              v-model="movementForm.notes" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Observações sobre a movimentação"
            ></textarea>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeMovementModal">Cancelar</Button>
        <Button variant="primary" @click="saveMovement">Registrar</Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'StockLotDetail',
  components: {
    Card,
    Button,
    Input,
    Select,
    Modal,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const showEditModal = ref(false)
    const showMovementModal = ref(false)
    
    // Dados fictícios para demonstração
    const movements = ref([
      {
        id: 1,
        date: '2023-09-15T14:30:00',
        type: 'entry',
        quantity: 20,
        unit: 'Litro',
        user: 'João Silva',
        notes: 'Compra de estoque'
      },
      {
        id: 2,
        date: '2023-09-10T09:15:00',
        type: 'exit',
        quantity: 5,
        unit: 'Litro',
        user: 'Maria Oliveira',
        notes: 'Utilização em experimento'
      },
      {
        id: 3,
        date: '2023-09-01T11:45:00',
        type: 'entry',
        quantity: 10,
        unit: 'Litro',
        user: 'Pedro Santos',
        notes: 'Recebimento de fornecedor'
      },
      {
        id: 4,
        date: '2023-08-20T16:20:00',
        type: 'exit',
        quantity: 3,
        unit: 'Litro',
        user: 'Ana Costa',
        notes: 'Transferência para outro laboratório'
      },
      {
        id: 5,
        date: '2023-08-15T10:30:00',
        type: 'entry',
        quantity: 15,
        unit: 'Litro',
        user: 'Carlos Mendes',
        notes: 'Ajuste de estoque'
      }
    ])
    
    const reagents = ref([
      { value: 1, label: 'Ácido Clorídrico' },
      { value: 2, label: 'Etanol 96%' },
      { value: 3, label: 'Sulfato de Cobre' }
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
    
    const movementTypes = ref([
      { value: 'entry', label: 'Entrada' },
      { value: 'exit', label: 'Saída' }
    ])
    
    // Formulário de edição
    const editForm = ref({
      lot_number: 'AC12345',
      reagent: 1,
      quantity: 25,
      unit: 'Litro',
      expiry_date: '2024-12-31',
      supplier: 1,
      location: 1,
      purchase_price: 45.00,
      purchase_date: '2023-03-15'
    })
    
    // Formulário de movimentação
    const movementForm = ref({
      type: 'entry',
      quantity: 0,
      unit: 'Litro',
      user: '',
      notes: ''
    })
    
    // Métodos
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const editLot = () => {
      showEditModal.value = true
    }
    
    const closeEditModal = () => {
      showEditModal.value = false
    }
    
    const saveLot = () => {
      // Lógica para salvar o lote
      console.log('Salvando lote:', editForm.value)
      closeEditModal()
    }
    
    const addMovement = () => {
      showMovementModal.value = true
    }
    
    const closeMovementModal = () => {
      showMovementModal.value = false
    }
    
    const saveMovement = () => {
      // Lógica para registrar a movimentação
      console.log('Registrando movimentação:', movementForm.value)
      closeMovementModal()
    }
    
    return {
      showEditModal,
      showMovementModal,
      movements,
      reagents,
      suppliers,
      locations,
      movementTypes,
      editForm,
      movementForm,
      formatDate,
      editLot,
      closeEditModal,
      saveLot,
      addMovement,
      closeMovementModal,
      saveMovement
    }
  }
}
</script>