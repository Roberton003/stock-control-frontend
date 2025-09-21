<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Validações em Tempo Real</h1>
      <Button variant="primary" @click="toggleRealTimeValidation">
        <Icon :name="realTimeValidationEnabled ? 'pause' : 'play'" class="mr-2" />
        {{ realTimeValidationEnabled ? 'Desativar' : 'Ativar' }} Validações em Tempo Real
      </Button>
    </div>
    
    <!-- Configurações das validações em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Configurações das Validações em Tempo Real</h2>
      </template>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Atraso de Validação (ms)</label>
          <Input 
            v-model="validationSettings.delay" 
            type="number" 
            placeholder="Atraso em milissegundos" 
            @input="updateValidationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Campos a Validar</label>
          <Select 
            v-model="validationSettings.fieldsToValidate" 
            :options="fieldOptions" 
            multiple
            placeholder="Selecione os campos" 
            @change="updateValidationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Mostrar Erros Imediatamente</label>
          <Toggle 
            v-model="validationSettings.showErrorsImmediately" 
            label="Exibir erros assim que forem detectados" 
            @change="updateValidationSettings"
          />
        </div>
      </div>
    </Card>
    
    <!-- Exemplo de formulário com validações em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Formulário com Validações em Tempo Real</h2>
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
              @input="debouncedValidate('name')"
            />
            <div v-if="errors.name" class="mt-1 text-sm text-red-600">
              {{ errors.name }}
            </div>
            <div v-else-if="validations.name" class="mt-1 text-sm text-green-600">
              {{ validations.name }}
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Categoria *</label>
            <Select 
              v-model="form.category" 
              :error="errors.category"
              :options="categories" 
              placeholder="Selecione uma categoria"
              @change="validateField('category')"
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
              @change="validateField('unit')"
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
              placeholder="Digite a quantidade mínima" 
              @input="debouncedValidate('min_stock')"
            />
            <div v-if="errors.min_stock" class="mt-1 text-sm text-red-600">
              {{ errors.min_stock }}
            </div>
            <div v-else-if="validations.min_stock" class="mt-1 text-sm text-green-600">
              {{ validations.min_stock }}
            </div>
          </div>
          
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea 
              v-model="form.description" 
              rows="3" 
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              placeholder="Descrição detalhada do reagente"
              @input="debouncedValidate('description')"
            ></textarea>
            <div v-if="errors.description" class="mt-1 text-sm text-red-600">
              {{ errors.description }}
            </div>
            <div v-else-if="validations.description" class="mt-1 text-sm text-green-600">
              {{ validations.description }}
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
    
    <!-- Regras de validação em tempo real -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Regras de Validação em Tempo Real</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Validações Automáticas</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Nome: Mínimo de 3 caracteres, máximo de 100 caracteres</li>
              <li>Categoria: Seleção obrigatória de uma opção válida</li>
              <li>Unidade: Seleção obrigatória de uma opção válida</li>
              <li>Quantidade Mínima: Deve ser um número positivo</li>
              <li>Descrição: Opcional, mas limitada a 500 caracteres</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Validações Especiais</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Nome único: Verificação no banco de dados se o nome já existe</li>
              <li>Quantidade Mínima: Deve ser menor que Quantidade Máxima (se definida)</li>
              <li>Descrição: Não deve conter palavras-chave restritas</li>
              <li>Campos dependentes: Validações que dependem de outros campos</li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre validações em tempo real -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre Validações em Tempo Real</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios das Validações em Tempo Real</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Feedback imediato ao usuário sobre erros de entrada</li>
              <li>Redução de erros de formulário antes do envio</li>
              <li>Melhoria da experiência do usuário com correções em tempo real</li>
              <li>Prevenção de envios inválidos ao servidor</li>
              <li>Aumento da eficiência no preenchimento de formulários</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Validações em Tempo Real:</span>
                <span>{{ realTimeValidationEnabled ? 'Ativadas' : 'Desativadas' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Atraso de Validação:</span>
                <span>{{ validationSettings.delay }}ms</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Campos a Validar:</span>
                <span>{{ validationSettings.fieldsToValidate.length }} selecionados</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Mostrar Erros Imediatamente:</span>
                <span>{{ validationSettings.showErrorsImmediately ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Formulário Válido:</span>
                <span>{{ formIsValid ? 'Sim' : 'Não' }}</span>
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
import Toggle from '@/components/ui/Toggle.vue'
import Spinner from '@/components/ui/Spinner.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'RealTimeValidations',
  components: {
    Card,
    Button,
    Input,
    Select,
    Toggle,
    Spinner,
    Icon,
    Badge
  },
  setup() {
    // Estados
    const realTimeValidationEnabled = ref(true)
    const isSubmitting = ref(false)
    const formIsValid = ref(false)
    
    // Configurações das validações em tempo real
    const validationSettings = ref({
      delay: 500,
      fieldsToValidate: ['name', 'category', 'unit', 'min_stock', 'description'],
      showErrorsImmediately: true
    })
    
    // Opções para seletores
    const fieldOptions = ref([
      { value: 'name', label: 'Nome' },
      { value: 'category', label: 'Categoria' },
      { value: 'unit', label: 'Unidade' },
      { value: 'min_stock', label: 'Quantidade Mínima' },
      { value: 'description', label: 'Descrição' }
    ])
    
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
    
    // Formulário
    const form = ref({
      name: '',
      category: '',
      unit: '',
      min_stock: 0,
      description: ''
    })
    
    // Erros de validação
    const errors = ref({
      name: '',
      category: '',
      unit: '',
      min_stock: '',
      description: ''
    })
    
    // Validações bem-sucedidas
    const validations = ref({
      name: '',
      min_stock: '',
      description: ''
    })
    
    // Timeout para debounce
    let validationTimeout
    
    // Computed para verificar se o formulário é válido
    const isFormValid = computed(() => {
      return (
        form.value.name.length >= 3 &&
        form.value.category !== '' &&
        form.value.unit !== '' &&
        form.value.min_stock > 0 &&
        Object.values(errors.value).every(error => error === '')
      )
    })
    
    // Métodos
    const toggleRealTimeValidation = () => {
      realTimeValidationEnabled.value = !realTimeValidationEnabled.value
    }
    
    const updateValidationSettings = () => {
      // Atualizar configurações das validações em tempo real
      console.log('Atualizando configurações das validações em tempo real:', validationSettings.value)
    }
    
    const validateField = (fieldName) => {
      if (!realTimeValidationEnabled.value) return
      
      // Verificar se o campo deve ser validado
      if (!validationSettings.value.fieldsToValidate.includes(fieldName)) return
      
      switch (fieldName) {
        case 'name':
          if (form.value.name.length < 3) {
            errors.value.name = 'O nome deve ter pelo menos 3 caracteres'
            validations.value.name = ''
          } else if (form.value.name.length > 100) {
            errors.value.name = 'O nome não pode ter mais de 100 caracteres'
            validations.value.name = ''
          } else {
            // Verificação de nome único (simulação)
            if (form.value.name.toLowerCase().includes('ácido')) {
              errors.value.name = 'Já existe um reagente com este nome'
              validations.value.name = ''
            } else {
              errors.value.name = ''
              validations.value.name = 'Nome válido'
            }
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
      
      // Atualizar o estado de validade do formulário
      formIsValid.value = isFormValid.value
    }
    
    const debouncedValidate = (fieldName) => {
      if (!realTimeValidationEnabled.value) return
      
      // Limpar timeout anterior
      clearTimeout(validationTimeout)
      
      // Configurar novo timeout
      validationTimeout = setTimeout(() => {
        validateField(fieldName)
      }, validationSettings.value.delay)
    }
    
    const submitForm = () => {
      if (!realTimeValidationEnabled.value || !formIsValid.value) return
      
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
      
      formIsValid.value = false
    }
    
    return {
      realTimeValidationEnabled,
      isSubmitting,
      formIsValid,
      validationSettings,
      fieldOptions,
      categories,
      units,
      form,
      errors,
      validations,
      isFormValid,
      toggleRealTimeValidation,
      updateValidationSettings,
      validateField,
      debouncedValidate,
      submitForm,
      resetForm
    }
  }
}
</script>