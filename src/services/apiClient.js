import axios from 'axios'

// Criar instância do axios com configurações padrão
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // URL base do backend
  timeout: 10000, // Timeout de 10 segundos
  headers: {
    'Content-Type': 'application/json'
  }
})

export default apiClient