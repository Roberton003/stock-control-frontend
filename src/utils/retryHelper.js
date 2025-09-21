// src/utils/retryHelper.js
export async function retry(fn, retries = 3, delay = 1000) {
  let lastError;
  
  for (let i = 0; i <= retries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // Se não for o último retry, esperar antes de tentar novamente
      if (i < retries) {
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  // Lançar o último erro se todas as tentativas falharem
  throw lastError;
}