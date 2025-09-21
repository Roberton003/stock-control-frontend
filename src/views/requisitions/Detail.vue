<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Detalhes da Requisição</h1>
      <div v-if="request.status === 'Pendente'">
        <Button variant="success" class="mr-2" @click="approveRequest">
          <Icon name="check" class="mr-2" />
          Aprovar
        </Button>
        <Button variant="error" @click="rejectRequest">
          <Icon name="times" class="mr-2" />
          Rejeitar
        </Button>
      </div>
    </div>
    
    <!-- Informações gerais -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações Gerais</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="text-sm font-medium text-gray-500">ID</h3>
          <p class="mt-1 text-sm text-gray-900">#{{ request.id }}</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Solicitante</h3>
          <p class="mt-1 text-sm text-gray-900">{{ request.requester }}</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Data</h3>
          <p class="mt-1 text-sm text-gray-900">{{ formatDate(request.date) }}</p>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-500">Status</h3>
          <p class="mt-1 text-sm text-gray-900">
            <Badge :variant="getStatusVariant(request.status)">
              {{ request.status }}
            </Badge>
          </p>
        </div>
      </div>
    </Card>
    
    <!-- Itens da requisição -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Itens da Requisição</h2>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reagente</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade Solicitada</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(item, index) in request.items" :key="index" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.reagent }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.quantity }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ item.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getItemStatusVariant(item.status)">
                  {{ item.status }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
    
    <!-- Observações -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Observações</h2>
      </template>
      <p class="text-gray-700">{{ request.notes || 'Nenhuma observação registrada.' }}</p>
    </Card>
    
    <!-- Histórico de aprovações -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Histórico de Aprovações</h2>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ação</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Responsável</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Comentários</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(approval, index) in request.approvalHistory" :key="index" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(approval.date) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="approval.action === 'Aprovada' ? 'success' : 'error'">
                  {{ approval.action }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ approval.responsible }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ approval.comments || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
    
    <!-- Modal de aprovação/rejeição -->
    <Modal :visible="showApprovalModal" @close="closeApprovalModal">
      <template #header>
        <h3 class="text-lg font-medium">
          {{ approvalAction === 'approve' ? 'Aprovar Requisição' : 'Rejeitar Requisição' }}
        </h3>
      </template>
      
      <form @submit.prevent="submitApproval">
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Comentários</label>
            <textarea 
              v-model="approvalForm.comments" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              :placeholder="`Comentários sobre a ${approvalAction === 'approve' ? 'aprovação' : 'rejeição'} da requisição`"
            ></textarea>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button variant="outline" @click="closeApprovalModal">Cancelar</Button>
        <Button :variant="approvalAction === 'approve' ? 'success' : 'error'" @click="submitApproval">
          {{ approvalAction === 'approve' ? 'Aprovar' : 'Rejeitar' }}
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Modal from '@/components/ui/Modal.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'RequisitionDetail',
  components: {
    Card,
    Button,
    Modal,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const showApprovalModal = ref(false)
    const approvalAction = ref('') // 'approve' ou 'reject'
    
    // Dados fictícios para demonstração
    const request = ref({
      id: 1,
      requester: 'João Silva',
      date: '2023-09-15T14:30:00',
      status: 'Pendente',
      notes: 'Necessário para o experimento XYZ agendado para amanhã.',
      items: [
        {
          reagent: 'Ácido Clorídrico',
          quantity: 5,
          unit: 'Litro',
          status: 'Disponível'
        },
        {
          reagent: 'Etanol 96%',
          quantity: 10,
          unit: 'Litro',
          status: 'Parcialmente Disponível'
        }
      ],
      approvalHistory: [
        {
          date: '2023-09-15T14:30:00',
          action: 'Criada',
          responsible: 'João Silva',
          comments: 'Requisição criada para experimento XYZ'
        }
      ]
    })
    
    // Formulário de aprovação
    const approvalForm = ref({
      comments: ''
    })
    
    // Métodos
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const getStatusVariant = (status) => {
      switch (status) {
        case 'Aprovada': return 'success'
        case 'Pendente': return 'warning'
        case 'Rejeitada': return 'error'
        default: return 'default'
      }
    }
    
    const getItemStatusVariant = (status) => {
      switch (status) {
        case 'Disponível': return 'success'
        case 'Parcialmente Disponível': return 'warning'
        case 'Indisponível': return 'error'
        default: return 'default'
      }
    }
    
    const approveRequest = () => {
      approvalAction.value = 'approve'
      showApprovalModal.value = true
    }
    
    const rejectRequest = () => {
      approvalAction.value = 'reject'
      showApprovalModal.value = true
    }
    
    const closeApprovalModal = () => {
      showApprovalModal.value = false
      approvalForm.value.comments = ''
    }
    
    const submitApproval = () => {
      // Lógica para submeter aprovação/rejeição
      console.log(`${approvalAction.value === 'approve' ? 'Aprovando' : 'Rejeitando'} requisição:`, approvalForm.value)
      closeApprovalModal()
    }
    
    return {
      showApprovalModal,
      approvalAction,
      request,
      approvalForm,
      formatDate,
      getStatusVariant,
      getItemStatusVariant,
      approveRequest,
      rejectRequest,
      closeApprovalModal,
      submitApproval
    }
  }
}
</script>