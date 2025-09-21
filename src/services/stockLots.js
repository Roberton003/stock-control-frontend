import apiClient from './apiClient'

export default {
  // Obter todos os lotes de estoque
  getAll() {
    return apiClient.get('/stock-lots/')
  },

  // Obter um lote de estoque específico pelo ID
  getById(id) {
    return apiClient.get(`/stock-lots/${id}/`)
  },

  // Criar um novo lote de estoque
  create(stockLot) {
    return apiClient.post('/stock-lots/', stockLot)
  },

  // Atualizar um lote de estoque existente
  update(id, stockLot) {
    return apiClient.put(`/stock-lots/${id}/`, stockLot)
  },

  // Excluir um lote de estoque
  delete(id) {
    return apiClient.delete(`/stock-lots/${id}/`)
  }
}