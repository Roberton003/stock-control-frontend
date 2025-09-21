import apiClient from './apiClient'

export default {
  // Obter dados do dashboard
  getDashboardData() {
    return apiClient.get('/dashboard/')
  },

  // Obter resumo do estoque
  getStockSummary() {
    return apiClient.get('/dashboard/stock-summary/')
  },

  // Obter alertas de validade
  getExpiryAlerts() {
    return apiClient.get('/dashboard/expiry-alerts/')
  },

  // Obter movimentações recentes
  getRecentMovements() {
    return apiClient.get('/dashboard/recent-movements/')
  },

  // Obter dados para gráficos
  getChartData(type, params) {
    return apiClient.get(`/dashboard/charts/${type}/`, { params })
  }
}