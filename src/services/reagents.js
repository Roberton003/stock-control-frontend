import apiClient from './apiClient'

export default {
  // Obter todos os reagentes
  getAll() {
    return apiClient.get('/reagents/')
  },

  // Obter um reagente específico pelo ID
  getById(id) {
    return apiClient.get(`/reagents/${id}/`)
  },

  // Criar um novo reagente
  create(reagent) {
    return apiClient.post('/reagents/', reagent)
  },

  // Atualizar um reagente existente
  update(id, reagent) {
    return apiClient.put(`/reagents/${id}/`, reagent)
  },

  // Excluir um reagente
  delete(id) {
    return apiClient.delete(`/reagents/${id}/`)
  }
}