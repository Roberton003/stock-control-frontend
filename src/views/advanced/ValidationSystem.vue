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
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Validação</label>
          <Select 
            v-model="validationSettings.validationType" 
            :options="validationTypeOptions" 
            placeholder="Selecione o tipo" 
            @change="updateValidationSettings"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tempo de Validação</label>
          <Select 
            v-model="validationSettings.validationTime" 
            :options="validationTimeOptions" 
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
    
    <!-- Exemplo de formulário com validação -->
    <Card class="mb-6 bg-white">
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">Exemplo de Formulário com Validação</h2>
          <Badge :variant="formIsValid ? 'success' : 'error'">
            {{ formIsValid ? 'Válido' : 'Inválido' }}
          </Badge>
        </div>
      </template>
      
      <form @submit.prevent="submitForm" class="p-4">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
            <Input 
              v-model="form.name" 
              :error="errors.name"
              placeholder="Nome do reagente" 
              @blur="validateField('name')"
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
            ></textarea>
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
    
    <!-- Regras de validação -->
    <Card class="mb-6 bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Regras de Validação</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Campos Obrigatórios</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Nome (mínimo 3 caracteres)</li>
              <li>Categoria (seleção obrigatória)</li>
              <li>Unidade (seleção obrigatória)</li>
              <li>Quantidade Mínima (número positivo)</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Validações Especiais</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Nome deve ser único (verificação no banco de dados)</li>
              <li>Quantidade Mínima deve ser menor que Quantidade Máxima</li>
              <li>Descrição opcional mas limitada a 500 caracteres</li>
              <li>Todos os campos devem passar na validação antes do envio</li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
    
    <!-- Informações sobre o sistema de validação -->
    <Card class="bg-white">
      <template #header>
        <h2 class="text-lg font-semibold">Informações sobre o Sistema de Validação</h2>
      </template>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Benefícios do Sistema de Validação</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
              <li>Previne erros de entrada de dados no lado do cliente</li>
              <li>Melhora a experiência do usuário com feedback imediato</li>
              <li>Reduz a carga no servidor ao validar antes do envio</li>
              <li>Padroniza as regras de validação em toda a aplicação</li>
              <li>Permite reutilização de regras em diferentes formulários</li>
            </ul>
          </div>
          <div>
            <h3 class="text-md font-medium text-gray-900 mb-2">Configurações Atuais</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex justify-between">
                <span class="font-medium">Tipo de Validação:</span>
                <span>{{ validationSettings.validationType }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Tempo de Validação:</span>
                <span>{{ validationSettings.validationTime }}ms</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Exibir Mensagens de Erro:</span>
                <span>{{ validationSettings.showErrorMessages ? 'Sim' : 'Não' }}</span>
              </li>
              <li class="flex justify-between">
                <span class="font-medium">Sistema de Validação:</span>
                <span>{{ validationSystemEnabled ? 'Ativado' : 'Desativado' }}</span>
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
import { ref, computed, watch } from 'vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select from '@/components/ui/Select.vue'
import Toggle from '@/components/ui/Toggle.vue'
import Spinner from '@/components/ui/Spinner.vue'
import Icon from '@/components/ui/Icon.vue'
import Badge from '@/components/ui/Badge.vue'

export default {
  name: 'ValidationSystem',
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
    const validationSystemEnabled = ref(true)
    const isSubmitting = ref(false)
    const formIsValid = ref(false)
    
    // Configurações do sistema de validação
    const validationSettings = ref({
      validationType: 'real-time',
      validationTime: 500,
      showErrorMessages: true
    })
    
    // Opções para seletores
    const validationTypeOptions = ref([
      { value: 'real-time', label: 'Tempo Real' },
      { value: 'on-blur', label: 'Ao Sair do Campo' },
      { value: 'on-submit', label: 'Ao Enviar' }
    ])
    
    const validationTimeOptions = ref([
      { value: 300, label: '300ms' },
      { value: 500, label: '500ms' },
      { value: 1000, label: '1000ms' },
      { value: 2000, label: '2000ms' }
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
      min_stock: ''
    })
    
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
    
    // Watch para validar o formulário em tempo real
    watch(form, () => {
      if (validationSettings.value.validationType === 'real-time') {
        validateForm()
      }
    }, { deep: true })
    
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
    const toggleValidationSystem = () => {
      validationSystemEnabled.value = !validationSystemEnabled.value
    }
    
    const updateValidationSettings = () => {
      // Atualizar configurações do sistema de validação
      console.log('Atualizando configurações do sistema de validação:', validationSettings.value)
    }
    
    const validateField = (fieldName) => {
      if (!validationSystemEnabled.value) return
      
      switch (fieldName) {
        case 'name':
          if (form.value.name.length < 3) {
            errors.value.name = 'O nome deve ter pelo menos 3 caracteres'
          } else {
            errors.value.name = ''
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
          } else {
            errors.value.min_stock = ''
          }
          break
      }
      
      // Atualizar o estado de validade do formulário
      formIsValid.value = isFormValid.value
    }
    
    const validateForm = () => {
      if (!validationSystemEnabled.value) return
      
      // Validar todos os campos
      validateField('name')
      validateField('category')
      validateField('unit')
      validateField('min_stock')
      
      // Atualizar o estado de validade do formulário
      formIsValid.value = isFormValid.value
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
        min_stock: ''
      }
      
      formIsValid.value = false
    }
    
    return {
      validationSystemEnabled,
      isSubmitting,
      formIsValid,
      validationSettings,
      validationTypeOptions,
      validationTimeOptions,
      form,
      errors,
      categories,
      units,
      isFormValid,
      toggleValidationSystem,
      updateValidationSettings,
      validateField,
      validateForm,
      submitForm,
      resetForm
    }
  }
}
</script>