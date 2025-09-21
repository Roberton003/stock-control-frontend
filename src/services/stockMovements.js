import apiClient from './apiClient'

export default {
  // Obter todos os movimentos de estoque
  getAll() {
    return apiClient.get('/stock-movements/')
  },

  // Obter um movimento de estoque específico pelo ID
  getById(id) {
    return apiClient.get(`/stock-movements/${id}/`)
  },

  // Criar um novo movimento de estoque
  create(stockMovement) {
    return apiClient.post('/stock-movements/', stockMovement)
  },

  // Atualizar um movimento de estoque existente
  update(id, stockMovement) {
    return apiClient.put(`/stock-movements/${id}/`, stockMovement)
  },

  // Excluir um movimento de estoque
  delete(id) {
    return apiClient.delete(`/stock-movements/${id}/`)
  }
}