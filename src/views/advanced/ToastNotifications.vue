<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Sistema de Notificações Toast</h1>
      <Button variant="primary" @click="toggleToastNotifications">
        <Icon :name="toastNotificationsEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ toastNotificationsEnabled ? 'Desativar' : 'Ativar' }} Notificações Toast
      </Button>
    </div>
    
    <!-- Configurações das notificações toast -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações das Notificações Toast</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Posição</label>
          <Select 
            v-model="toastSettings.position" 
            :options="positionOptions" 
            placeholder="Selecione a posição" 
            @change="updateToastSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Duração</label>
          <Select 
            v-model="toastSettings.duration" 
            :options="durationOptions" 
            placeholder="Selecione a duração" 
            @change="updateToastSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Exibir Botão Fechar</label>
          <Toggle 
            v-model="toastSettings.showCloseButton" 
            label="Mostrar botão para fechar manualmente" 
            @change="updateToastSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplos de notificações toast -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <!-- Notificação de sucesso -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Notificação de Sucesso</h2>
        </template>
        <div class="p-4">
          <Button variant="success" @click="showSuccessToast">
            <Icon name="check-circle" class="mr-2" />
            Mostrar Notificação de Sucesso
          </Button>
        </div>
      </Card>
      
      <!-- Notificação de erro -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Notificação de Erro</h2>
        </template>
        <div class="p-4">
          <Button variant="error" @click="showErrorToast">
            <Icon name="exclamation-circle" class="mr-2" />
            Mostrar Notificação de Erro
          </Button>
        </div>
      </Card>
      
      <!-- Notificação de aviso -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Notificação de Aviso</h2>
        </template>
        <div class="p-4">
          <Button variant="warning" @click="showWarningToast">
            <Icon name="exclamation-triangle" class="mr-2" />
            Mostrar Notificação de Aviso
          </Button>
        </div>
      </Card>
      
      <!-- Notificação de informação -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Notificação de Informação</h2>
        </template>
        <div class="p-4">
          <Button variant="info" @click="showInfoToast">
            <Icon name="info-circle" class="mr-2" />
            Mostrar Notificação de Informação
          </Button>
        </div>
      </Card>
    </div>
    
    <!-- Teste de notificações em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Teste de Notificações em Tempo Real</h2>
          <Badge :variant="notificationSimulationEnabled ? 'success' : 'default'">
            {{ notificationSimulationEnabled ? 'Simulação Ativa' : 'Simulação Inativa' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações de Simulação</h3>
            <div class="space-y-4">
              <Toggle 
                v-model="notificationSimulationEnabled" 
                label="Ativar simulação de notificações" 
                @change="toggleNotificationSimulation"
              />
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Frequência de Notificações</label>
                <Slider 
                  v-model="notificationFrequency" 
                  :min="1" 
                  :max="30" 
                  :step="1"
                  @change="updateNotificationSimulation"
                />
                <div class="mt-1 text-sm text-gray-500">
                  Uma notificação a cada {{ notificationFrequency }} segundos
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipos de Notificação</label>
                <div class="space-y-2">
                  <Checkbox 
                    v-for="notificationType in notificationTypes" 
                    :key="notificationType.value"
                    v-model="notificationType.enabled"
                    :label="notificationType.label"
                    @change="updateNotificationSimulation"
                  />
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Controles de Teste</h3>
            <div class="space-y-4">
              <Button 
                variant="outline" 
                @click="startNotificationSimulation" 
                :disabled="!notificationSimulationEnabled || simulationRunning"
              >
                <Icon name="play" class="mr-2" />
                Iniciar Simulação
              </Button>
              
              <Button 
                variant="outline" 
                @click="stopNotificationSimulation" 
                :disabled="!simulationRunning"
              >
                <Icon name="pause" class="mr-2" />
                Parar Simulação
              </Button>
              
              <Button 
                variant="outline" 
                @click="sendCustomNotification"
              >
                <Icon name="bell" class="mr-2" />
                Enviar Notificação Personalizada
              </Button>
              
              <Button 
                variant="outline" 
                @click="clearAllNotifications"
              >
                <Icon name="ban" class="mr-2" />
                Limpar Todas as Notificações
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Componente de notificação toast -->
    <Toast 
      v-for="toast in toasts" 
      :key="toast.id"
      :id="toast.id"
      :message="toast.message"
      :variant="toast.variant"
      :duration="toast.duration"
      :position="toast.position"
      :show-close-button="toast.showCloseButton"
      @close="removeToast"
    />
    
    <!-- Informações sobre notificações toast -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Notificações Toast</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios das Notificações Toast</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Fornecem feedback imediato sobre ações do usuário</li>
              <li>Não interrompem o fluxo de trabalho do usuário</li>
              <li>Podem ser facilmente ignoradas ou fechadas</li>
              <li>Permitem comunicação eficaz de status e erros</li>
              <li>Melhoram a experiência geral do usuário</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Notificações Toast:</span>
                <span>{{ toastNotificationsEnabled ? 'Ativadas' : 'Desativadas' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Posição:</span>
                <span>{{ toastSettings.position }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Duração:</span>
                <span>{{ toastSettings.duration }} segundos</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Exibir Botão Fechar:</span>
                <span>{{ toastSettings.showCloseButton ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Simulação de Notificações:</span>
                <span>{{ notificationSimulationEnabled ? 'Ativada' : 'Desativada' }}</span>
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
import Toggle from '@/components/ui/Toggle.vue'
import Slider from '@/components/ui/Slider.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'
import Toast from '@/components/ui/Toast.vue'

export default {
  name: 'ToastNotifications',
  components: {
    Card,
    Button,
    Select,
    Toggle,
    Slider,
    Checkbox,
    Icon,
    Badge,
    Toast
  },
  setup() {
    // Estados
    const toastNotificationsEnabled = ref(true)
    const notificationSimulationEnabled = ref(false)
    const simulationRunning = ref(false)
    const notificationFrequency = ref(5)
    const notificationInterval = ref(null)
    
    // Configurações das notificações toast
    const toastSettings = ref({
      position: 'top-right',
      duration: 5,
      showCloseButton: true
    })
    
    // Notificações ativas
    const toasts = ref([])
    let toastId = 0
    
    // Opções para seletores
    const positionOptions = ref([
      { value: 'top-left', label: 'Superior Esquerda' },
      { value: 'top-right', label: 'Superior Direita' },
      { value: 'bottom-left', label: 'Inferior Esquerda' },
      { value: 'bottom-right', label: 'Inferior Direita' },
      { value: 'top-center', label: 'Superior Centro' },
      { value: 'bottom-center', label: 'Inferior Centro' }
    ])
    
    const durationOptions = ref([
      { value: 3, label: '3 segundos' },
      { value: 5, label: '5 segundos' },
      { value: 10, label: '10 segundos' },
      { value: 15, label: '15 segundos' },
      { value: 0, label: 'Manual (sem auto-fechamento)' }
    ])
    
    // Tipos de notificação para simulação
    const notificationTypes = ref([
      { value: 'success', label: 'Sucesso', enabled: true },
      { value: 'error', label: 'Erro', enabled: true },
      { value: 'warning', label: 'Aviso', enabled: true },
      { value: 'info', label: 'Informação', enabled: true }
    ])
    
    // Métodos
    const toggleToastNotifications = () => {
      toastNotificationsEnabled.value = !toastNotificationsEnabled.value
    }
    
    const updateToastSettings = () => {
      // Atualizar configurações das notificações toast
      console.log('Atualizando configurações das notificações toast:', toastSettings.value)
    }
    
    const toggleNotificationSimulation = () => {
      notificationSimulationEnabled.value = !notificationSimulationEnabled.value
    }
    
    const updateNotificationSimulation = () => {
      // Atualizar configurações da simulação de notificações
      console.log('Atualizando simulação de notificações:', {
        frequency: notificationFrequency.value,
        types: notificationTypes.value.filter(nt => nt.enabled).map(nt => nt.value)
      })
    }
    
    const showSuccessToast = () => {
      if (!toastNotificationsEnabled.value) return
      
      addToast({
        message: 'Operação realizada com sucesso!',
        variant: 'success',
        duration: toastSettings.value.duration * 1000,
        position: toastSettings.value.position,
        showCloseButton: toastSettings.value.showCloseButton
      })
    }
    
    const showErrorToast = () => {
      if (!toastNotificationsEnabled.value) return
      
      addToast({
        message: 'Ocorreu um erro ao processar a operação.',
        variant: 'error',
        duration: toastSettings.value.duration * 1000,
        position: toastSettings.value.position,
        showCloseButton: toastSettings.value.showCloseButton
      })
    }
    
    const showWarningToast = () => {
      if (!toastNotificationsEnabled.value) return
      
      addToast({
        message: 'Esta ação requer atenção especial.',
        variant: 'warning',
        duration: toastSettings.value.duration * 1000,
        position: toastSettings.value.position,
        showCloseButton: toastSettings.value.showCloseButton
      })
    }
    
    const showInfoToast = () => {
      if (!toastNotificationsEnabled.value) return
      
      addToast({
        message: 'Informações importantes sobre o sistema.',
        variant: 'info',
        duration: toastSettings.value.duration * 1000,
        position: toastSettings.value.position,
        showCloseButton: toastSettings.value.showCloseButton
      })
    }
    
    const addToast = (toast) => {
      toastId++
      toasts.value.push({
        id: toastId,
        ...toast
      })
      
      // Remover toast automaticamente após o tempo especificado (exceto se for 0)
      if (toast.duration > 0) {
        setTimeout(() => {
          removeToast(toastId)
        }, toast.duration)
      }
    }
    
    const removeToast = (id) => {
      const index = toasts.value.findIndex(toast => toast.id === id)
      if (index !== -1) {
        toasts.value.splice(index, 1)
      }
    }
    
    const clearAllNotifications = () => {
      toasts.value = []
    }
    
    const startNotificationSimulation = () => {
      if (simulationRunning.value || !notificationSimulationEnabled.value) return
      
      simulationRunning.value = true
      
      // Iniciar intervalo de simulação
      notificationInterval.value = setInterval(() => {
        // Selecionar aleatoriamente um tipo de notificação habilitado
        const enabledTypes = notificationTypes.value.filter(nt => nt.enabled)
        if (enabledTypes.length > 0) {
          const randomType = enabledTypes[Math.floor(Math.random() * enabledTypes.length)]
          const messages = {
            success: 'Operação concluída com sucesso!',
            error: 'Ocorreu um erro inesperado.',
            warning: 'Atenção: limite mínimo atingido.',
            info: 'Nova atualização disponível.'
          }
          
          addToast({
            message: messages[randomType.value],
            variant: randomType.value,
            duration: toastSettings.value.duration * 1000,
            position: toastSettings.value.position,
            showCloseButton: toastSettings.value.showCloseButton
          })
        }
      }, notificationFrequency.value * 1000)
    }
    
    const stopNotificationSimulation = () => {
      if (!simulationRunning.value) return
      
      simulationRunning.value = false
      clearInterval(notificationInterval.value)
      notificationInterval.value = null
    }
    
    const sendCustomNotification = () => {
      if (!toastNotificationsEnabled.value) return
      
      // Abrir modal para enviar notificação personalizada
      console.log('Abrindo modal para notificação personalizada')
    }
    
    return {
      toastNotificationsEnabled,
      notificationSimulationEnabled,
      simulationRunning,
      notificationFrequency,
      toastSettings,
      toasts,
      positionOptions,
      durationOptions,
      notificationTypes,
      toggleToastNotifications,
      updateToastSettings,
      toggleNotificationSimulation,
      updateNotificationSimulation,
      showSuccessToast,
      showErrorToast,
      showWarningToast,
      showInfoToast,
      addToast,
      removeToast,
      clearAllNotifications,
      startNotificationSimulation,
      stopNotificationSimulation,
      sendCustomNotification
    }
  }
}
</script>