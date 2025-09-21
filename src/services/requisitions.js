import apiClient from './apiClient'

export default {
  // Obter todas as requisições
  getAll() {
    return apiClient.get('/requisitions/')
  },

  // Obter uma requisição específica pelo ID
  getById(id) {
    return apiClient.get(`/requisitions/${id}/`)
  },

  // Criar uma nova requisição
  create(requisition) {
    return apiClient.post('/requisitions/', requisition)
  },

  // Atualizar uma requisição existente
  update(id, requisition) {
    return apiClient.put(`/requisitions/${id}/`, requisition)
  },

  // Excluir uma requisição
  delete(id) {
    return apiClient.delete(`/requisitions/${id}/`)
  },

  // Aprovar uma requisição
  approve(id) {
    return apiClient.post(`/requisitions/${id}/approve/`)
  },

  // Rejeitar uma requisição
  reject(id) {
    return apiClient.post(`/requisitions/${id}/reject/`)
  }
}