# playwright.config.js - Configuração do Playwright para testes E2E

/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  // Diretório onde os testes estão localizados
  testDir: './e2e_tests',
  
  // Diretório para resultados dos testes
  outputDir: './test_results/playwright',
  
  // Timeout global para cada teste
  timeout: 30000,
  
  // Configurações de expectativa
  expect: {
    // Timeout para expectativas
    timeout: 5000
  },
  
  // Em ambiente CI, falhar imediatamente
  forbidOnly: !!process.env.CI,
  
  // Número de tentativas em caso de falha
  retries: process.env.CI ? 2 : 0,
  
  // Número de workers para execução paralela
  workers: process.env.CI ? 1 : undefined,
  
  // Configurações do reporter
  reporter: [
    // Reporter padrão
    ['list'],
    
    // Reporter HTML para visualização dos resultados
    ['html', { 
      outputFolder: 'playwright-report', 
      open: 'never' 
    }],
    
    // Reporter JSON para integração com outras ferramentas
    ['json', { 
      outputFile: 'test_results/playwright/results.json' 
    }],
    
    // Reporter JUnit para integração com CI/CD
    ['junit', { 
      outputFile: 'test_results/playwright/results.xml' 
    }]
  ],
  
  // Configurações padrão para todos os projetos
  use: {
    // URL base para testes
    baseURL: 'http://localhost:8000',
    
    // Configurações de tracing
    trace: 'on-first-retry',
    
    // Configurações de screenshot
    screenshot: 'only-on-failure',
    
    // Configurações de vídeo
    video: 'retain-on-failure',
    
    // Executar em modo headless (sem interface gráfica) em CI
    headless: !!process.env.CI,
    
    // Viewport padrão
    viewport: { width: 1280, height: 720 },
    
    // Ignorar erros de HTTPS
    ignoreHTTPSErrors: true,
    
    // Permitir downloads
    acceptDownloads: true,
  },
  
  // Projetos para diferentes browsers
  projects: [
    {
      name: 'chromium',
      use: { 
        browserName: 'chromium',
        // Emulando dispositivos móveis
        ...devices['Desktop Chrome']
      },
    },
    
    {
      name: 'firefox',
      use: { 
        browserName: 'firefox',
        ...devices['Desktop Firefox']
      },
    },
    
    {
      name: 'webkit',
      use: { 
        browserName: 'webkit',
        ...devices['Desktop Safari']
      },
    },
    
    // Testes em dispositivos móveis
    {
      name: 'Mobile Chrome',
      use: { 
        browserName: 'chromium',
        ...devices['Pixel 5']
      },
    },
    
    {
      name: 'Mobile Safari',
      use: { 
        browserName: 'webkit',
        ...devices['iPhone 12']
      },
    },
  ],
};

// Exportar configuração
module.exports = config;

// Dispositivos para emulação
const devices = {
  'Desktop Chrome': {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    viewport: { width: 1280, height: 720 }
  },
  'Desktop Firefox': {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    viewport: { width: 1280, height: 720 }
  },
  'Desktop Safari': {
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    viewport: { width: 1280, height: 720 }
  },
  'Pixel 5': {
    userAgent: 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
    viewport: { width: 393, height: 851 },
    deviceScaleFactor: 2.75,
    isMobile: true,
    hasTouch: true
  },
  'iPhone 12': {
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true
  }
};

module.exports.devices = devices;