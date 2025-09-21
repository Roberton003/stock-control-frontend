import apiClient from './apiClient'

export default {
  // Obter todos os fornecedores
  getAll() {
    return apiClient.get('/suppliers/')
  },

  // Obter um fornecedor específico pelo ID
  getById(id) {
    return apiClient.get(`/suppliers/${id}/`)
  },

  // Criar um novo fornecedor
  create(supplier) {
    return apiClient.post('/suppliers/', supplier)
  },

  // Atualizar um fornecedor existente
  update(id, supplier) {
    return apiClient.put(`/suppliers/${id}/`, supplier)
  },

  // Excluir um fornecedor
  delete(id) {
    return apiClient.delete(`/suppliers/${id}/`)
  }
}