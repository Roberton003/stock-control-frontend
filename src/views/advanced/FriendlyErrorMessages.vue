<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Mensagens de Erro Amigáveis</h1>
      <Button variant="primary" @click="toggleFriendlyErrorMessages">
        <Icon :name="friendlyErrorMessagesEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ friendlyErrorMessagesEnabled ? 'Desativar' : 'Ativar' }} Mensagens Amigáveis
      </Button>
    </div>
    
    <!-- Configurações das mensagens de erro amigáveis -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações das Mensagens de Erro Amigáveis</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Estilo de Exibição</label>
          <Select 
            v-model="errorSettings.displayStyle" 
            :options="displayStyleOptions" 
            placeholder="Selecione o estilo" 
            @change="updateErrorSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tempo de Exibição</label>
          <Select 
            v-model="errorSettings.displayTime" 
            :options="displayTimeOptions" 
            placeholder="Selecione o tempo" 
            @change="updateErrorSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Exibir Detalhes Técnicos</label>
          <Toggle 
            v-model="errorSettings.showTechnicalDetails" 
            label="Mostrar detalhes técnicos aos usuários avançados" 
            @change="updateErrorSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplos de mensagens de erro amigáveis -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <!-- Erro de validação de formulário -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Erro de Validação de Formulário</h2>
        </template>
        <div class="p-4">
          <Alert 
            v-if="showFormError" 
            variant="error" 
            title="Erro de Validação"
            :dismissible="true"
            @dismiss="dismissFormError"
          >
            <p>O formulário contém erros que precisam ser corrigidos antes de continuar:</p>
            <ul class="list-disc pl-5 mt-2 space-y-1">
              <li>O campo "Nome" é obrigatório</li>
              <li>O campo "Email" deve ser um endereço de email válido</li>
              <li>O campo "Senha" deve ter pelo menos 8 caracteres</li>
            </ul>
          </Alert>
          <div v-else class="text-center py-8">
            <Button variant="outline" @click="showFormError = true">
              <Icon name="exclamation-triangle" class="mr-2" />
              Mostrar Erro de Validação
            </Button>
          </div>
        </div>
      </Card>
      
      <!-- Erro de conexão -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Erro de Conexão</h2>
        </template>
        <div class="p-4">
          <Alert 
            v-if="showConnectionError" 
            variant="error" 
            title="Erro de Conexão"
            :dismissible="true"
            @dismiss="dismissConnectionError"
          >
            <p>Não foi possível conectar ao servidor. Por favor, verifique sua conexão com a internet e tente novamente.</p>
            <div class="mt-4 flex space-x-3">
              <Button variant="outline" size="sm" @click="retryConnection">
                <Icon name="sync" class="mr-2" :spin="retryingConnection" />
                {{ retryingConnection ? 'Tentando...' : 'Tentar Novamente' }}
              </Button>
              <Button variant="outline" size="sm" @click="contactSupport">
                <Icon name="envelope" class="mr-2" />
                Contatar Suporte
              </Button>
            </div>
          </Alert>
          <div v-else class="text-center py-8">
            <Button variant="outline" @click="showConnectionError = true">
              <Icon name="wifi-slash" class="mr-2" />
              Mostrar Erro de Conexão
            </Button>
          </div>
        </div>
      </Card>
      
      <!-- Erro de permissão -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Erro de Permissão</h2>
        </template>
        <div class="p-4">
          <Alert 
            v-if="showPermissionError" 
            variant="error" 
            title="Acesso Negado"
            :dismissible="true"
            @dismiss="dismissPermissionError"
          >
            <p>Você não tem permissão para acessar este recurso. Se você acredita que isso é um erro, entre em contato com o administrador do sistema.</p>
            <div class="mt-4 flex space-x-3">
              <Button variant="outline" size="sm" @click="requestAccess">
                <Icon name="key" class="mr-2" />
                Solicitar Acesso
              </Button>
              <Button variant="outline" size="sm" @click="goToDashboard">
                <Icon name="home" class="mr-2" />
                Voltar ao Dashboard
              </Button>
            </div>
          </Alert>
          <div v-else class="text-center py-8">
            <Button variant="outline" @click="showPermissionError = true">
              <Icon name="lock" class="mr-2" />
              Mostrar Erro de Permissão
            </Button>
          </div>
        </div>
      </Card>
      
      <!-- Erro genérico -->
      <Card class="bg-white">
        <template #header>
          <h2 class="text-lg font-semibold">Erro Genérico</h2>
        </template>
        <div class="p-4">
          <Alert 
            v-if="showGenericError" 
            variant="error" 
            title="Ocorreu um Erro"
            :dismissible="true"
            @dismiss="dismissGenericError"
          >
            <p>Desculpe, ocorreu um erro inesperado. Nossa equipe já foi notificada e está trabalhando para resolver o problema.</p>
            <details v-if="errorSettings.showTechnicalDetails" class="mt-4 bg-gray-100 p-3 rounded">
              <summary class="cursor-pointer text-sm font-medium">Detalhes Técnicos</summary>
              <pre class="mt-2 text-xs text-gray-700 overflow-x-auto">
Error: TypeError: Cannot read property 'name' of undefined
    at ReagentService.getReagentById (src/services/reagents.js:45:23)
    at ReagentDetail.setup (src/views/reagents/Detail.vue:120:15)
              </pre>
            </details>
            <div class="mt-4 flex space-x-3">
              <Button variant="outline" size="sm" @click="reloadPage">
                <Icon name="sync" class="mr-2" />
                Recarregar Página
              </Button>
              <Button variant="outline" size="sm" @click="goToDashboard">
                <Icon name="home" class="mr-2" />
                Voltar ao Dashboard
              </Button>
            </div>
          </Alert>
          <div v-else class="text-center py-8">
            <Button variant="outline" @click="showGenericError = true">
              <Icon name="exclamation-circle" class="mr-2" />
              Mostrar Erro Genérico
            </Button>
          </div>
        </div>
      </Card>
    </div>
    
    <!-- Teste de mensagens de erro em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Teste de Mensagens de Erro em Tempo Real</h2>
          <Badge :variant="errorSimulationEnabled ? 'success' : 'default'">
            {{ errorSimulationEnabled ? 'Simulação Ativa' : 'Simulação Inativa' }}
          </Badge>
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações de Simulação</h3>
            <div class="space-y-4">
              <Toggle 
                v-model="errorSimulationEnabled" 
                label="Ativar simulação de erros" 
                @change="toggleErrorSimulation"
              />
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Taxa de Erro</label>
                <Slider 
                  v-model="errorRate" 
                  :min="0" 
                  :max="100" 
                  :step="5"
                  @change="updateErrorSimulation"
                />
                <div class="mt-1 text-sm text-gray-500">
                  {{ errorRate }}% de chance de erro em cada requisição
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipos de Erro</label>
                <div class="space-y-2">
                  <Checkbox 
                    v-for="errorType in errorTypes" 
                    :key="errorType.value"
                    v-model="errorType.enabled"
                    :label="errorType.label"
                    @change="updateErrorSimulation"
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
                @click="simulateApiCall" 
                :disabled="!errorSimulationEnabled"
              >
                <Icon name="bolt" class="mr-2" />
                Simular Chamada API
              </Button>
              
              <Button 
                variant="outline" 
                @click="simulateFormSubmission" 
                :disabled="!errorSimulationEnabled"
              >
                <Icon name="paper-plane" class="mr-2" />
                Simular Envio de Formulário
              </Button>
              
              <Button 
                variant="outline" 
                @click="simulatePermissionCheck" 
                :disabled="!errorSimulationEnabled"
              >
                <Icon name="shield-alt" class="mr-2" />
                Simular Verificação de Permissão
              </Button>
              
              <Button 
                variant="outline" 
                @click="clearAllErrors"
              >
                <Icon name="ban" class="mr-2" />
                Limpar Todos os Erros
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre mensagens de erro amigáveis -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Mensagens de Erro Amigáveis</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Princípios das Mensagens Amigáveis</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Claras e concisas, evitando jargões técnicos</li>
              <li>Educadas e empáticas, reconhecendo a frustração do usuário</li>
              <li>Informativas, explicando o que aconteceu e por que</li>
              <li>Úteis, oferecendo soluções ou próximos passos</li>
              <li>Consistentes em tom e estilo em toda a aplicação</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Mensagens Amigáveis:</span>
                <span>{{ friendlyErrorMessagesEnabled ? 'Ativadas' : 'Desativadas' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Estilo de Exibição:</span>
                <span>{{ errorSettings.displayStyle }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Tempo de Exibição:</span>
                <span>{{ errorSettings.displayTime }} segundos</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Exibir Detalhes Técnicos:</span>
                <span>{{ errorSettings.showTechnicalDetails ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Simulação de Erros:</span>
                <span>{{ errorSimulationEnabled ? 'Ativada' : 'Desativada' }}</span>
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
import Alert from '@/components/ui/Alert.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'FriendlyErrorMessages',
  components: {
    Card,
    Button,
    Select,
    Toggle,
    Slider,
    Checkbox,
    Alert,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const friendlyErrorMessagesEnabled = ref(true)
    const errorSimulationEnabled = ref(false)
    const errorRate = ref(20)
    const retryingConnection = ref(false)
    
    // Configurações das mensagens de erro
    const errorSettings = ref({
      displayStyle: 'toast',
      displayTime: 5,
      showTechnicalDetails: false
    })
    
    // Estados dos erros de exemplo
    const showFormError = ref(false)
    const showConnectionError = ref(false)
    const showPermissionError = ref(false)
    const showGenericError = ref(false)
    
    // Opções para seletores
    const displayStyleOptions = ref([
      { value: 'toast', label: 'Toast' },
      { value: 'modal', label: 'Modal' },
      { value: 'inline', label: 'Inline' }
    ])
    
    const displayTimeOptions = ref([
      { value: 3, label: '3 segundos' },
      { value: 5, label: '5 segundos' },
      { value: 10, label: '10 segundos' },
      { value: 0, label: 'Manual (sem auto-fechamento)' }
    ])
    
    // Tipos de erro para simulação
    const errorTypes = ref([
      { value: 'validation', label: 'Erros de Validação', enabled: true },
      { value: 'network', label: 'Erros de Rede', enabled: true },
      { value: 'permission', label: 'Erros de Permissão', enabled: true },
      { value: 'server', label: 'Erros do Servidor', enabled: true },
      { value: 'generic', label: 'Erros Genéricos', enabled: true }
    ])
    
    // Métodos
    const toggleFriendlyErrorMessages = () => {
      friendlyErrorMessagesEnabled.value = !friendlyErrorMessagesEnabled.value
    }
    
    const updateErrorSettings = () => {
      // Atualizar configurações das mensagens de erro
      console.log('Atualizando configurações das mensagens de erro:', errorSettings.value)
    }
    
    const toggleErrorSimulation = () => {
      errorSimulationEnabled.value = !errorSimulationEnabled.value
    }
    
    const updateErrorSimulation = () => {
      // Atualizar configurações da simulação de erros
      console.log('Atualizando simulação de erros:', {
        errorRate: errorRate.value,
        errorTypes: errorTypes.value.filter(et => et.enabled).map(et => et.value)
      })
    }
    
    const dismissFormError = () => {
      showFormError.value = false
    }
    
    const dismissConnectionError = () => {
      showConnectionError.value = false
    }
    
    const dismissPermissionError = () => {
      showPermissionError.value = false
    }
    
    const dismissGenericError = () => {
      showGenericError.value = false
    }
    
    const retryConnection = () => {
      retryingConnection.value = true
      
      // Simular tentativa de reconexão
      setTimeout(() => {
        retryingConnection.value = false
        showConnectionError.value = false
      }, 2000)
    }
    
    const contactSupport = () => {
      // Abrir formulário de contato com suporte
      console.log('Abrindo formulário de contato com suporte')
    }
    
    const requestAccess = () => {
      // Solicitar acesso ao recurso
      console.log('Solicitando acesso ao recurso')
    }
    
    const goToDashboard = () => {
      // Navegar para o dashboard
      console.log('Navegando para o dashboard')
    }
    
    const reloadPage = () => {
      // Recarregar a página
      window.location.reload()
    }
    
    const simulateApiCall = () => {
      // Simular chamada à API
      console.log('Simulando chamada à API')
      
      // Determinar aleatoriamente se ocorrerá um erro
      const shouldError = Math.random() * 100 < errorRate.value
      
      if (shouldError) {
        // Selecionar aleatoriamente um tipo de erro habilitado
        const enabledErrors = errorTypes.value.filter(et => et.enabled)
        if (enabledErrors.length > 0) {
          const randomError = enabledErrors[Math.floor(Math.random() * enabledErrors.length)]
          showRandomError(randomError.value)
        }
      } else {
        console.log('Chamada API bem-sucedida')
      }
    }
    
    const simulateFormSubmission = () => {
      // Simular envio de formulário
      console.log('Simulando envio de formulário')
      
      // Determinar aleatoriamente se ocorrerá um erro
      const shouldError = Math.random() * 100 < errorRate.value
      
      if (shouldError) {
        showFormError.value = true
      } else {
        console.log('Formulário enviado com sucesso')
      }
    }
    
    const simulatePermissionCheck = () => {
      // Simular verificação de permissão
      console.log('Simulando verificação de permissão')
      
      // Determinar aleatoriamente se ocorrerá um erro
      const shouldError = Math.random() * 100 < errorRate.value
      
      if (shouldError) {
        showPermissionError.value = true
      } else {
        console.log('Permissão concedida')
      }
    }
    
    const showRandomError = (errorType) => {
      switch (errorType) {
        case 'validation':
          showFormError.value = true
          break
        case 'network':
          showConnectionError.value = true
          break
        case 'permission':
          showPermissionError.value = true
          break
        case 'server':
        case 'generic':
        default:
          showGenericError.value = true
          break
      }
    }
    
    const clearAllErrors = () => {
      showFormError.value = false
      showConnectionError.value = false
      showPermissionError.value = false
      showGenericError.value = false
    }
    
    return {
      friendlyErrorMessagesEnabled,
      errorSimulationEnabled,
      errorRate,
      retryingConnection,
      errorSettings,
      showFormError,
      showConnectionError,
      showPermissionError,
      showGenericError,
      displayStyleOptions,
      displayTimeOptions,
      errorTypes,
      toggleFriendlyErrorMessages,
      updateErrorSettings,
      toggleErrorSimulation,
      updateErrorSimulation,
      dismissFormError,
      dismissConnectionError,
      dismissPermissionError,
      dismissGenericError,
      retryConnection,
      contactSupport,
      requestAccess,
      goToDashboard,
      reloadPage,
      simulateApiCall,
      simulateFormSubmission,
      simulatePermissionCheck,
      showRandomError,
      clearAllErrors
    }
  }
}
</script>