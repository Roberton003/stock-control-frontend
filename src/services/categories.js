import apiClient from './apiClient'

export default {
  // Obter todas as categorias
  getAll() {
    return apiClient.get('/categories/')
  },

  // Obter uma categoria específica pelo ID
  getById(id) {
    return apiClient.get(`/categories/${id}/`)
  },

  // Criar uma nova categoria
  create(category) {
    return apiClient.post('/categories/', category)
  },

  // Atualizar uma categoria existente
  update(id, category) {
    return apiClient.put(`/categories/${id}/`, category)
  },

  // Excluir uma categoria
  delete(id) {
    return apiClient.delete(`/categories/${id}/`)
  }
}