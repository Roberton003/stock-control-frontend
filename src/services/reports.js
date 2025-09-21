import apiClient from './apiClient'

export default {
  // Obter todos os relatórios
  getAll() {
    return apiClient.get('/reports/')
  },

  // Obter um relatório específico pelo ID
  getById(id) {
    return apiClient.get(`/reports/${id}/`)
  },

  // Criar um novo relatório
  create(report) {
    return apiClient.post('/reports/', report)
  },

  // Atualizar um relatório existente
  update(id, report) {
    return apiClient.put(`/reports/${id}/`, report)
  },

  // Excluir um relatório
  delete(id) {
    return apiClient.delete(`/reports/${id}/`)
  },

  // Gerar relatório de consumo
  generateConsumptionReport(params) {
    return apiClient.get('/reports/consumption/', { params })
  },

  // Gerar relatório de validade
  generateExpiryReport(params) {
    return apiClient.get('/reports/expiry/', { params })
  },

  // Gerar relatório de estoque
  generateStockReport(params) {
    return apiClient.get('/reports/stock/', { params })
  }
}