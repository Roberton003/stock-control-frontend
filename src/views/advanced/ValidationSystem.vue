<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Sistema de Validação Reutilizável</h1>
      <Button variant="primary" @click="toggleValidationSystem">
        <Icon :name="validationSystemEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ validationSystemEnabled ? 'Desativar' : 'Ativar' }} Sistema de Validação
      </Button>
    </div>
    
    <!-- Configurações do sistema de validação -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações do Sistema de Validação</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Modo de Validação</label>
          <Select 
            v-model="validationSettings.mode" 
            :options="validationModeOptions" 
            placeholder="Selecione o modo" 
            @change="updateValidationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tempo de Validação</label>
          <Select 
            v-model="validationSettings.timing" 
            :options="validationTimingOptions" 
            placeholder="Selecione o tempo" 
            @change="updateValidationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Exibir Mensagens de Erro</label>
          <Toggle 
            v-model="validationSettings.showErrorMessages" 
            label="Mostrar mensagens de erro amigáveis" 
            @change="updateValidationSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de formulário com validação reutilizável -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Formulário com Validação Reutilizável</h2>
          <Badge :variant="formIsValid ? 'success' : 'error'">
            {{ formIsValid ? 'Válido' : 'Inválido' }}
          </Badge>
        </div>
      </template>
      
      <form @submit.prevent="submitForm" class="p-4">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Reagente *</label>
            <Input 
              v-model="form.name" 
              :error="errors.name"
              placeholder="Digite o nome do reagente" 
              @blur="validateField('name')"
              @input="clearError('name')"
            />
            <div v-if="errors.name" class="mt-1 text-sm text-red-600">
              {{ errors.name }}
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Categoria *</label>
            <Select 
              v-model="form.category" 
              :error="errors.category"
              :options="categories" 
              placeholder="Selecione uma categoria"
              @blur="validateField('category')"
              @change="clearError('category')"
            />
            <div v-if="errors.category" class="mt-1 text-sm text-red-600">
              {{ errors.category }}
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unidade *</label>
            <Select 
              v-model="form.unit" 
              :error="errors.unit"
              :options="units" 
              placeholder="Selecione uma unidade"
              @blur="validateField('unit')"
              @change="clearError('unit')"
            />
            <div v-if="errors.unit" class="mt-1 text-sm text-red-600">
              {{ errors.unit }}
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade Mínima *</label>
            <Input 
              v-model="form.min_stock" 
              :error="errors.min_stock"
              type="number" 
              placeholder="Quantidade mínima" 
              @blur="validateField('min_stock')"
              @input="clearError('min_stock')"
            />
            <div v-if="errors.min_stock" class="mt-1 text-sm text-red-600">
              {{ errors.min_stock }}
            </div>
          </div>
          
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea 
              v-model="form.description" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Descrição detalhada do reagente"
              @blur="validateField('description')"
              @input="clearError('description')"
            ></textarea>
            <div v-if="errors.description" class="mt-1 text-sm text-red-600">
              {{ errors.description }}
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-end space-x-3">
          <Button variant="outline" @click="resetForm">Limpar</Button>
          <Button 
            variant="primary" 
            type="submit" 
            :disabled="!formIsValid || isSubmitting"
          >
            <Spinner v-if="isSubmitting" size="sm" class="mr-2" />
            {{ isSubmitting ? 'Enviando...' : 'Enviar' }}
          </Button>
        </div>
      </form>
    </Card>
    
    <!-- Regras de validação reutilizáveis -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Regras de Validação Reutilizáveis</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Regras Disponíveis</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Obrigatório (required) - Campo deve ser preenchido</li>
              <li>Comprimento Mínimo (minLength) - Campo deve ter pelo menos N caracteres</li>
              <li>Comprimento Máximo (maxLength) - Campo não deve ultrapassar N caracteres</li>
              <li>Número Positivo (positiveNumber) - Valor deve ser maior que zero</li>
              <li>Email Válido (email) - Campo deve conter um email válido</li>
              <li>Data Futura (futureDate) - Data deve ser posterior à data atual</li>
              <li>Data Passada (pastDate) - Data deve ser anterior à data atual</li>
              <li>Personalizado (custom) - Regras específicas definidas pelo usuário</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Sistema de Validação:</span>
                <span>{{ validationSystemEnabled ? 'Ativado' : 'Desativado' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Modo de Validação:</span>
                <span>{{ validationSettings.mode }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Tempo de Validação:</span>
                <span>{{ validationSettings.timing }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Exibir Mensagens de Erro:</span>
                <span>{{ validationSettings.showErrorMessages ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Formulário Válido:</span>
                <span>{{ formIsValid ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Erros Encontrados:</span>
                <span>{{ Object.keys(errors).length }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Demonstração de validação em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Demonstração de Validação em Tempo Real</h2>
          <Toggle 
            v-model="realTimeValidationEnabled" 
            label="Ativar validação em tempo real" 
            @change="toggleRealTimeValidation"
          />
        </div>
      </template>
      
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Campo com Validação em Tempo Real</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome de Usuário *</label>
                <Input 
                  v-model="realTimeForm.username" 
                  :error="realTimeErrors.username"
                  placeholder="Digite seu nome de usuário" 
                  @input="validateUsername"
                />
                <div v-if="realTimeErrors.username" class="mt-1 text-sm text-red-600">
                  {{ realTimeErrors.username }}
                </div>
                <div v-else-if="realTimeValidations.username" class="mt-1 text-sm text-green-600">
                  {{ realTimeValidations.username }}
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                <Input 
                  v-model="realTimeForm.email" 
                  :error="realTimeErrors.email"
                  type="email" 
                  placeholder="Digite seu email" 
                  @input="validateEmail"
                />
                <div v-if="realTimeErrors.email" class="mt-1 text-sm text-red-600">
                  {{ realTimeErrors.email }}
                </div>
                <div v-else-if="realTimeValidations.email" class="mt-1 text-sm text-green-600">
                  {{ realTimeValidations.email }}
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Senha *</label>
                <Input 
                  v-model="realTimeForm.password" 
                  :error="realTimeErrors.password"
                  type="password" 
                  placeholder="Digite sua senha" 
                  @input="validatePassword"
                />
                <div v-if="realTimeErrors.password" class="mt-1 text-sm text-red-600">
                  {{ realTimeErrors.password }}
                </div>
                <div v-else-if="realTimeValidations.password" class="mt-1 text-sm text-green-600">
                  {{ realTimeValidations.password }}
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Status da Validação</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <span class="text-sm font-medium text-gray-700">Nome de Usuário</span>
                <Badge :variant="getValidationStatus(realTimeForm.username, realTimeErrors.username)">
                  {{ getValidationStatusLabel(realTimeForm.username, realTimeErrors.username) }}
                </Badge>
              </div>
              
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <span class="text-sm font-medium text-gray-700">Email</span>
                <Badge :variant="getValidationStatus(realTimeForm.email, realTimeErrors.email)">
                  {{ getValidationStatusLabel(realTimeForm.email, realTimeErrors.email) }}
                </Badge>
              </div>
              
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <span class="text-sm font-medium text-gray-700">Senha</span>
                <Badge :variant="getValidationStatus(realTimeForm.password, realTimeErrors.password)">
                  {{ getValidationStatusLabel(realTimeForm.password, realTimeErrors.password) }}
                </Badge>
              </div>
              
              <div class="mt-4 p-4 bg-blue-50 rounded-md">
                <h4 class="text-md font-medium text-blue-800 mb-2">Benefícios da Validação em Tempo Real</h4>
                <ul class="list-disc pl-5 space-y-1 text-sm text-blue-700">
                  <li>Feedback imediato sobre erros de entrada</li>
                  <li>Redução de erros de formulário antes do envio</li>
                  <li>Melhoria da experiência do usuário</li>
                  <li>Prevenção de envios inválidos ao servidor</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Mensagens de erro amigáveis -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Mensagens de Erro Amigáveis</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Exemplos de Mensagens</h3>
            <div class="space-y-4">
              <Alert variant="error" title="Erro de Validação">
                <p>O campo "Nome" é obrigatório e deve ter pelo menos 3 caracteres.</p>
              </Alert>
              
              <Alert variant="warning" title="Aviso de Validação">
                <p>A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números.</p>
              </Alert>
              
              <Alert variant="info" title="Informação de Validação">
                <p>O email digitado já está cadastrado no sistema. Deseja recuperar sua senha?</p>
              </Alert>
            </div>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações de Erros</h3>
            <div class="space-y-4">
              <Toggle 
                v-model="friendlyErrorMessagesEnabled" 
                label="Ativar mensagens de erro amigáveis" 
                @change="toggleFriendlyErrorMessages"
              />
              
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
import Toggle from '@/components/ui/Toggle.vue'
import Spinner from '@/components/ui/Spinner.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'
import Alert from '@/components/ui/Alert.vue'

export default {
  name: 'ReusableValidationSystem',
  components: {
    Card,
    Button,
    Input,
    Select,
    Toggle,
    Spinner,
    Icon,
    Badge,
    Alert
  },
  setup() {
    // Estados
    const validationSystemEnabled = ref(true)
    const realTimeValidationEnabled = ref(true)
    const friendlyErrorMessagesEnabled = ref(true)
    const isSubmitting = ref(false)
    
    // Configurações do sistema de validação
    const validationSettings = ref({
      mode: 'onChange',
      timing: 'realTime',
      showErrorMessages: true
    })
    
    // Configurações das mensagens de erro
    const errorSettings = ref({
      displayStyle: 'toast',
      displayTime: 5000,
      showTechnicalDetails: false
    })
    
    // Formulário principal
    const form = ref({
      name: '',
      category: '',
      unit: '',
      min_stock: 0,
      description: ''
    })
    
    // Erros de validação do formulário principal
    const errors = ref({
      name: '',
      category: '',
      unit: '',
      min_stock: '',
      description: ''
    })
    
    // Validações bem-sucedidas do formulário principal
    const validations = ref({
      name: '',
      min_stock: '',
      description: ''
    })
    
    // Formulário para validação em tempo real
    const realTimeForm = ref({
      username: '',
      email: '',
      password: ''
    })
    
    // Erros de validação em tempo real
    const realTimeErrors = ref({
      username: '',
      email: '',
      password: ''
    })
    
    // Validações bem-sucedidas em tempo real
    const realTimeValidations = ref({
      username: '',
      email: '',
      password: ''
    })
    
    // Opções para seletores
    const validationModeOptions = ref([
      { value: 'onChange', label: 'Ao Alterar' },
      { value: 'onBlur', label: 'Ao Sair do Campo' },
      { value: 'onSubmit', label: 'Ao Enviar' },
      { value: 'realTime', label: 'Em Tempo Real' }
    ])
    
    const validationTimingOptions = ref([
      { value: 'realTime', label: 'Tempo Real' },
      { value: 'delayed', label: 'Com Atraso' },
      { value: 'instant', label: 'Instantâneo' }
    ])
    
    const displayStyleOptions = ref([
      { value: 'toast', label: 'Toast' },
      { value: 'modal', label: 'Modal' },
      { value: 'inline', label: 'Inline' }
    ])
    
    const displayTimeOptions = ref([
      { value: 3000, label: '3 segundos' },
      { value: 5000, label: '5 segundos' },
      { value: 10000, label: '10 segundos' },
      { value: 0, label: 'Manual (sem auto-fechamento)' }
    ])
    
    // Dados fictícios para seletores
    const categories = ref([
      { value: 'acids', label: 'Ácidos' },
      { value: 'bases', label: 'Bases' },
      { value: 'salts', label: 'Sais' },
      { value: 'solvents', label: 'Solventes' },
      { value: 'indicators', label: 'Indicadores' }
    ])
    
    const units = ref([
      { value: 'liter', label: 'Litro' },
      { value: 'kilogram', label: 'Kilograma' },
      { value: 'gram', label: 'Grama' },
      { value: 'milliliter', label: 'Mililitro' },
      { value: 'piece', label: 'Peça' }
    ])
    
    // Computed properties
    const formIsValid = computed(() => {
      return (
        form.value.name.length >= 3 &&
        form.value.category !== '' &&
        form.value.unit !== '' &&
        form.value.min_stock > 0 &&
        Object.values(errors.value).every(error => error === '')
      )
    })
    
    // Métodos
    const toggleValidationSystem = () => {
      validationSystemEnabled.value = !validationSystemEnabled.value
    }
    
    const updateValidationSettings = () => {
      // Atualizar configurações do sistema de validação
      console.log('Atualizando configurações do sistema de validação:', validationSettings.value)
    }
    
    const toggleRealTimeValidation = () => {
      realTimeValidationEnabled.value = !realTimeValidationEnabled.value
    }
    
    const toggleFriendlyErrorMessages = () => {
      friendlyErrorMessagesEnabled.value = !friendlyErrorMessagesEnabled.value
    }
    
    const updateErrorSettings = () => {
      // Atualizar configurações das mensagens de erro
      console.log('Atualizando configurações das mensagens de erro:', errorSettings.value)
    }
    
    const validateField = (fieldName) => {
      if (!validationSystemEnabled.value) return
      
      switch (fieldName) {
        case 'name':
          if (form.value.name.length < 3) {
            errors.value.name = 'O nome deve ter pelo menos 3 caracteres'
            validations.value.name = ''
          } else if (form.value.name.length > 100) {
            errors.value.name = 'O nome não pode ter mais de 100 caracteres'
            validations.value.name = ''
          } else {
            errors.value.name = ''
            validations.value.name = 'Nome válido'
          }
          break
        case 'category':
          if (form.value.category === '') {
            errors.value.category = 'Por favor, selecione uma categoria'
          } else {
            errors.value.category = ''
          }
          break
        case 'unit':
          if (form.value.unit === '') {
            errors.value.unit = 'Por favor, selecione uma unidade'
          } else {
            errors.value.unit = ''
          }
          break
        case 'min_stock':
          if (form.value.min_stock <= 0) {
            errors.value.min_stock = 'A quantidade mínima deve ser maior que zero'
            validations.value.min_stock = ''
          } else {
            errors.value.min_stock = ''
            validations.value.min_stock = 'Quantidade mínima válida'
          }
          break
        case 'description':
          if (form.value.description.length > 500) {
            errors.value.description = 'A descrição não pode ter mais de 500 caracteres'
            validations.value.description = ''
          } else {
            errors.value.description = ''
            if (form.value.description.length > 0) {
              validations.value.description = 'Descrição válida'
            } else {
              validations.value.description = ''
            }
          }
          break
      }
    }
    
    const clearError = (fieldName) => {
      errors.value[fieldName] = ''
    }
    
    const validateUsername = () => {
      if (!realTimeValidationEnabled.value) return
      
      if (realTimeForm.value.username.length < 3) {
        realTimeErrors.value.username = 'O nome de usuário deve ter pelo menos 3 caracteres'
        realTimeValidations.value.username = ''
      } else if (realTimeForm.value.username.length > 20) {
        realTimeErrors.value.username = 'O nome de usuário não pode ter mais de 20 caracteres'
        realTimeValidations.value.username = ''
      } else {
        realTimeErrors.value.username = ''
        realTimeValidations.value.username = 'Nome de usuário válido'
      }
    }
    
    const validateEmail = () => {
      if (!realTimeValidationEnabled.value) return
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!realTimeForm.value.email) {
        realTimeErrors.value.email = 'O email é obrigatório'
        realTimeValidations.value.email = ''
      } else if (!emailRegex.test(realTimeForm.value.email)) {
        realTimeErrors.value.email = 'Por favor, insira um email válido'
        realTimeValidations.value.email = ''
      } else {
        realTimeErrors.value.email = ''
        realTimeValidations.value.email = 'Email válido'
      }
    }
    
    const validatePassword = () => {
      if (!realTimeValidationEnabled.value) return
      
      if (realTimeForm.value.password.length < 8) {
        realTimeErrors.value.password = 'A senha deve ter pelo menos 8 caracteres'
        realTimeValidations.value.password = ''
      } else if (!/[A-Z]/.test(realTimeForm.value.password)) {
        realTimeErrors.value.password = 'A senha deve conter pelo menos uma letra maiúscula'
        realTimeValidations.value.password = ''
      } else if (!/[a-z]/.test(realTimeForm.value.password)) {
        realTimeErrors.value.password = 'A senha deve conter pelo menos uma letra minúscula'
        realTimeValidations.value.password = ''
      } else if (!/\d/.test(realTimeForm.value.password)) {
        realTimeErrors.value.password = 'A senha deve conter pelo menos um número'
        realTimeValidations.value.password = ''
      } else {
        realTimeErrors.value.password = ''
        realTimeValidations.value.password = 'Senha válida'
      }
    }
    
    const getValidationStatus = (value, error) => {
      if (error) return 'error'
      if (value && !error) return 'success'
      return 'default'
    }
    
    const getValidationStatusLabel = (value, error) => {
      if (error) return 'Inválido'
      if (value && !error) return 'Válido'
      return 'Não preenchido'
    }
    
    const submitForm = () => {
      if (!validationSystemEnabled.value || !formIsValid.value) return
      
      isSubmitting.value = true
      
      // Simular envio do formulário
      setTimeout(() => {
        console.log('Enviando formulário:', form.value)
        isSubmitting.value = false
        resetForm()
      }, 2000)
    }
    
    const resetForm = () => {
      form.value = {
        name: '',
        category: '',
        unit: '',
        min_stock: 0,
        description: ''
      }
      
      errors.value = {
        name: '',
        category: '',
        unit: '',
        min_stock: '',
        description: ''
      }
      
      validations.value = {
        name: '',
        min_stock: '',
        description: ''
      }
    }
    
    return {
      validationSystemEnabled,
      realTimeValidationEnabled,
      friendlyErrorMessagesEnabled,
      isSubmitting,
      validationSettings,
      errorSettings,
      form,
      errors,
      validations,
      realTimeForm,
      realTimeErrors,
      realTimeValidations,
      validationModeOptions,
      validationTimingOptions,
      displayStyleOptions,
      displayTimeOptions,
      categories,
      units,
      formIsValid,
      toggleValidationSystem,
      updateValidationSettings,
      toggleRealTimeValidation,
      toggleFriendlyErrorMessages,
      updateErrorSettings,
      validateField,
      clearError,
      validateUsername,
      validateEmail,
      validatePassword,
      getValidationStatus,
      getValidationStatusLabel,
      submitForm,
      resetForm
    }
  }
}
</script>