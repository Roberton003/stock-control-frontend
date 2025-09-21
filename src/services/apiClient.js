import apiClient from './apiClient'

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

// Adicionar interceptador de resposta
apiClient.interceptors.response.use(
  (response) => {
    // Retornar apenas os dados da resposta
    return response.data
  },
  (error) => {
    // Tratar erros de resposta
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