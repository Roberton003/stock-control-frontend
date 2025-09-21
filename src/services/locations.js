import apiClient from './apiClient'

export default {
  // Obter todas as localizações
  getAll() {
    return apiClient.get('/locations/')
  },

  // Obter uma localização específica pelo ID
  getById(id) {
    return apiClient.get(`/locations/${id}/`)
  },

  // Criar uma nova localização
  create(location) {
    return apiClient.post('/locations/', location)
  },

  // Atualizar uma localização existente
  update(id, location) {
    return apiClient.put(`/locations/${id}/`, location)
  },

  // Excluir uma localização
  delete(id) {
    return apiClient.delete(`/locations/${id}/`)
  }
}