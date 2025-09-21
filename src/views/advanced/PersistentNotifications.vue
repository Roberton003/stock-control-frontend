<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Sistema de Notificações Persistentes</h1>
      <Button variant="primary" @click="togglePersistentNotifications">
        <Icon :name="persistentNotificationsEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ persistentNotificationsEnabled ? 'Desativar' : 'Ativar' }} Notificações Persistentes
      </Button>
    </div>
    
    <!-- Configurações das notificações persistentes -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações das Notificações Persistentes</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tempo de Exibição</label>
          <Select 
            v-model="notificationSettings.displayTime" 
            :options="displayTimeOptions" 
            placeholder="Selecione o tempo" 
            @change="updateNotificationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Posição</label>
          <Select 
            v-model="notificationSettings.position" 
            :options="positionOptions" 
            placeholder="Selecione a posição" 
            @change="updateNotificationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Exibir Notificações Não Lidas</label>
          <Toggle 
            v-model="notificationSettings.showUnread" 
            label="Mostrar apenas notificações não lidas" 
            @change="updateNotificationSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Painel de notificações -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Painel de Notificações</h2>
          <div class="flex space-x-2">
            <Button variant="outline" size="sm" @click="markAllAsRead">
              <Icon name="check-double" class="mr-2" />
              Marcar Todas como Lidas
            </Button>
            <Button variant="outline" size="sm" @click="clearAllNotifications">
              <Icon name="trash" class="mr-2" />
              Limpar Todas
            </Button>
          </div>
        </div>
      </template>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Notificação</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="notification in notifications" 
              :key="notification.id" 
              :class="notification.read ? 'bg-white' : 'bg-blue-50'"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div v-if="!notification.read" class="w-2 h-2 rounded-full bg-primary mr-3"></div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ notification.title }}</div>
                    <div class="text-sm text-gray-500">{{ notification.message }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(notification.timestamp) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="getTypeVariant(notification.type)">
                  {{ notification.type }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <Badge :variant="notification.read ? 'success' : 'warning'">
                  {{ notification.read ? 'Lida' : 'Não Lida' }}
                </Badge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <Button 
                  v-if="!notification.read" 
                  variant="secondary" 
                  size="sm" 
                  class="mr-2" 
                  @click="markAsRead(notification.id)"
                >
                  <Icon name="check" />
                </Button>
                <Button variant="outline" size="sm" @click="deleteNotification(notification.id)">
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
          Mostrando <span class="font-medium">1</span> a <span class="font-medium">{{ notifications.length }}</span> de <span class="font-medium">{{ notifications.length }}</span> notificações
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm" disabled>Anterior</Button>
          <Button variant="outline" size="sm" disabled>Próximo</Button>
        </div>
      </div>
    </Card>
    
    <!-- Centro de notificações -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Centro de Notificações</h2>
          <Badge variant="primary">
            {{ unreadNotificationsCount }} não lidas
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div v-if="unreadNotificationsCount > 0" class="space-y-4">
          <div 
            v-for="notification in unreadNotifications" 
            :key="notification.id" 
            class="p-4 rounded-lg border border-gray-200 bg-white shadow-sm"
          >
            <div class="flex justify-between">
              <div class="flex items-start">
                <div class="w-2 h-2 rounded-full bg-primary mt-2 mr-3"></div>
                <div>
                  <h3 class="text-sm font-medium text-gray-900">{{ notification.title }}</h3>
                  <p class="text-sm text-gray-500 mt-1">{{ notification.message }}</p>
                  <p class="text-xs text-gray-400 mt-2">{{ formatDate(notification.timestamp) }}</p>
                </div>
              </div>
              <div class="flex space-x-2">
                <Button variant="secondary" size="sm" @click="markAsRead(notification.id)">
                  <Icon name="check" class="mr-1" />
                  Marcar como Lida
                </Button>
                <Button variant="outline" size="sm" @click="deleteNotification(notification.id)">
                  <Icon name="trash" />
                </Button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <Icon name="bell-slash" class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-lg font-medium text-gray-900">Nenhuma notificação não lida</h3>
          <p class="mt-1 text-sm text-gray-500">Todas as suas notificações foram lidas.</p>
        </div>
      </div>
    </Card>
    
    <!-- Simulação de notificações -->
    <Card class="bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Simulação de Notificações</h2>
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
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'
import Toggle from '@/components/ui/Toggle.vue'
import Slider from '@/components/ui/Slider.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'PersistentNotifications',
  components: {
    Card,
    Button,
    Select,
    Toggle,
    Slider,
    Checkbox,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const persistentNotificationsEnabled = ref(true)
    const notificationSimulationEnabled = ref(false)
    const simulationRunning = ref(false)
    const notificationFrequency = ref(10)
    const notificationInterval = ref(null)
    
    // Configurações das notificações
    const notificationSettings = ref({
      displayTime: 5000,
      position: 'top-right',
      showUnread: true
    })
    
    // Notificações
    const notifications = ref([
      {
        id: 1,
        title: 'Lote próximo ao vencimento',
        message: 'O lote AC12345 de Ácido Clorídrico vence em 15 dias',
        timestamp: '2023-09-15T14:30:00',
        type: 'warning',
        read: false
      },
      {
        id: 2,
        title: 'Estoque baixo',
        message: 'O estoque de Etanol 96% está abaixo do mínimo definido',
        timestamp: '2023-09-14T09:15:00',
        type: 'error',
        read: false
      },
      {
        id: 3,
        title: 'Nova requisição aprovada',
        message: 'A requisição #REQ-2023-001 foi aprovada',
        timestamp: '2023-09-13T16:45:00',
        type: 'success',
        read: true
      },
      {
        id: 4,
        title: 'Atualização disponível',
        message: 'Uma nova versão do sistema está disponível',
        timestamp: '2023-09-12T11:20:00',
        type: 'info',
        read: true
      }
    ])
    
    // Opções para seletores
    const displayTimeOptions = ref([
      { value: 3000, label: '3 segundos' },
      { value: 5000, label: '5 segundos' },
      { value: 10000, label: '10 segundos' },
      { value: 15000, label: '15 segundos' },
      { value: 0, label: 'Manual (sem auto-fechamento)' }
    ])
    
    const positionOptions = ref([
      { value: 'top-left', label: 'Superior Esquerda' },
      { value: 'top-right', label: 'Superior Direita' },
      { value: 'bottom-left', label: 'Inferior Esquerda' },
      { value: 'bottom-right', label: 'Inferior Direita' },
      { value: 'top-center', label: 'Superior Centro' },
      { value: 'bottom-center', label: 'Inferior Centro' }
    ])
    
    // Tipos de notificação para simulação
    const notificationTypes = ref([
      { value: 'success', label: 'Sucesso', enabled: true },
      { value: 'error', label: 'Erro', enabled: true },
      { value: 'warning', label: 'Aviso', enabled: true },
      { value: 'info', label: 'Informação', enabled: true }
    ])
    
    // Computed properties
    const unreadNotificationsCount = computed(() => {
      return notifications.value.filter(n => !n.read).length
    })
    
    const unreadNotifications = computed(() => {
      return notifications.value.filter(n => !n.read)
    })
    
    // Métodos
    const togglePersistentNotifications = () => {
      persistentNotificationsEnabled.value = !persistentNotificationsEnabled.value
    }
    
    const updateNotificationSettings = () => {
      // Atualizar configurações das notificações
      console.log('Atualizando configurações das notificações:', notificationSettings.value)
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
    
    const getTypeVariant = (type) => {
      switch (type) {
        case 'success': return 'success'
        case 'error': return 'error'
        case 'warning': return 'warning'
        case 'info': return 'info'
        default: return 'default'
      }
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const markAsRead = (id) => {
      const notification = notifications.value.find(n => n.id === id)
      if (notification) {
        notification.read = true
      }
    }
    
    const markAllAsRead = () => {
      notifications.value.forEach(n => {
        n.read = true
      })
    }
    
    const deleteNotification = (id) => {
      const index = notifications.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notifications.value.splice(index, 1)
      }
    }
    
    const clearAllNotifications = () => {
      notifications.value = []
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
          
          // Adicionar nova notificação
          const newNotification = {
            id: Date.now(),
            title: 'Notificação de Simulação',
            message: messages[randomType.value],
            timestamp: new Date().toISOString(),
            type: randomType.value,
            read: false
          }
          
          notifications.value.unshift(newNotification)
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
      // Abrir modal para enviar notificação personalizada
      console.log('Abrindo modal para notificação personalizada')
    }
    
    // Lifecycle hooks
    onMounted(() => {
      // Inicializar sistema de notificações persistentes
      console.log('Inicializando sistema de notificações persistentes')
    })
    
    onUnmounted(() => {
      // Limpar intervalos e listeners
      if (notificationInterval.value) {
        clearInterval(notificationInterval.value)
      }
    })
    
    return {
      persistentNotificationsEnabled,
      notificationSimulationEnabled,
      simulationRunning,
      notificationFrequency,
      notificationInterval,
      notificationSettings,
      notifications,
      displayTimeOptions,
      positionOptions,
      notificationTypes,
      unreadNotificationsCount,
      unreadNotifications,
      getTypeVariant,
      formatDate,
      togglePersistentNotifications,
      updateNotificationSettings,
      toggleNotificationSimulation,
      updateNotificationSimulation,
      markAsRead,
      markAllAsRead,
      deleteNotification,
      clearAllNotifications,
      startNotificationSimulation,
      stopNotificationSimulation,
      sendCustomNotification
    }
  }
}
</script>