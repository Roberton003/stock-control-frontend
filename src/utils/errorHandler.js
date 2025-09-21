// src/utils/errorHandler.js
import { useToast } from '@/composables/useToast'
import { handleApiError } from '@/utils/apiError'

const { addToast } = useToast()

export function handleGlobalError(error) {
  const apiError = handleApiError(error)
  
  // Adicionar notificação amigável
  addToast(apiError.message, 'error', 5000)
  
  // Log do erro para depuração
  console.error('Erro não tratado:', apiError)
  
  return apiError
}

export function handleFormError(errors) {
  // Tratamento de erros de formulário
  if (errors) {
    Object.keys(errors).forEach(field => {
      const messages = errors[field]
      messages.forEach(message => {
        addToast(`${field}: ${message}`, 'warning', 5000)
      })
    })
  }
}