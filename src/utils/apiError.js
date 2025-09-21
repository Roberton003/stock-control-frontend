// src/utils/apiError.js
export class ApiError extends Error {
  constructor(message, status, code = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

export function handleApiError(error) {
  if (error.response) {
    // Erro de resposta do servidor
    const { status, data } = error.response;
    
    // Tratamento específico para diferentes status
    switch (status) {
      case 400:
        return new ApiError(
          data.detail || 'Requisição inválida. Verifique os dados enviados.',
          status,
          'BAD_REQUEST'
        );
      case 401:
        return new ApiError(
          'Não autorizado. Faça login novamente.',
          status,
          'UNAUTHORIZED'
        );
      case 403:
        return new ApiError(
          'Acesso proibido. Você não tem permissão para realizar esta ação.',
          status,
          'FORBIDDEN'
        );
      case 404:
        return new ApiError(
          'Recurso não encontrado.',
          status,
          'NOT_FOUND'
        );
      case 500:
        return new ApiError(
          'Erro interno do servidor. Tente novamente mais tarde.',
          status,
          'INTERNAL_SERVER_ERROR'
        );
      default:
        return new ApiError(
          data.detail || `Erro ${status}: ${error.message}`,
          status,
          'UNKNOWN_ERROR'
        );
    }
  } else if (error.request) {
    // Erro de rede (sem resposta do servidor)
    return new ApiError(
      'Erro de conexão. Verifique sua conexão com a internet.',
      null,
      'NETWORK_ERROR'
    );
  } else {
    // Outros erros
    return new ApiError(
      `Erro: ${error.message}`,
      null,
      'GENERAL_ERROR'
    );
  }
}