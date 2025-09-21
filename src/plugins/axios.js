// src/plugins/axios.js
import axios from 'axios'
import { retry } from '@/utils/retryHelper'

// Criar instância do axios com configurações padrão
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // URL base do backend
  timeout: 10000, // Timeout de 10 segundos
  headers: {
    'Content-Type': 'application/json'
  }
})

// Adicionar interceptador de requisição
apiClient.interceptors.request.use(
  (config) => {
    // Adicionar token de autenticação se existir
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Adicionar interceptador de resposta com retry automático
apiClient.interceptors.response.use(
  (response) => {
    // Retornar apenas os dados da resposta
    return response.data
  },
  async (error) => {
    const originalRequest = error.config
    
    // Verificar se é um erro de rede ou servidor (5xx)
    if ((error.code === 'ECONNABORTED' || error.message === 'Network Error' ||
         (error.response && error.response.status >= 500)) &&
        !originalRequest._retry) {
      
      originalRequest._retry = true
      
      // Tentar novamente a requisição
      return retry(() => axios(originalRequest), 3, 1000)
    }
    
    // Tratar erros de resposta do servidor (4xx)
    if (error.response) {
      // Erros de resposta do servidor
      console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
      // Erros de rede
      console.error('Network Error:', error.request)
    } else {
      // Outros erros
      console.error('Error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default apiClient