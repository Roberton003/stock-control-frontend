// vite.config.js - Configuração do Vite para o projeto

import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  // Raiz do projeto
  root: './',
  
  // Diretório de build
  build: {
    outDir: 'static/dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        // Entradas principais
        main: resolve(__dirname, 'static/src/js/main.js'),
        dashboard: resolve(__dirname, 'static/src/js/dashboard.js'),
        products: resolve(__dirname, 'static/src/js/products.js'),
        lots: resolve(__dirname, 'static/src/js/lots.js'),
        movements: resolve(__dirname, 'static/src/js/movements.js'),
        requisitions: resolve(__dirname, 'static/src/js/requisitions.js'),
        reports: resolve(__dirname, 'static/src/js/reports.js'),
        // Estilos principais
        styles: resolve(__dirname, 'static/src/css/main.css'),
      },
      output: {
        // Nomes dos arquivos de saída
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
    // Minificar em produção
    minify: 'esbuild',
    // Gerar sourcemaps em desenvolvimento
    sourcemap: true,
  },
  
  // Configurações do servidor de desenvolvimento
  server: {
    // Porta do servidor
    port: 3000,
    // Host do servidor
    host: '0.0.0.0',
    // Proxy para APIs do Django
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
    // Abrir navegador automaticamente
    open: true,
  },
  
  // Configurações de resolução de módulos
  resolve: {
    alias: {
      // Alias para diretórios comuns
      '@': resolve(__dirname, 'static/src'),
      '@components': resolve(__dirname, 'static/src/components'),
      '@utils': resolve(__dirname, 'static/src/utils'),
      '@assets': resolve(__dirname, 'static/src/assets'),
      '@styles': resolve(__dirname, 'static/src/css'),
      '@scripts': resolve(__dirname, 'static/src/js'),
    },
    // Extensões de arquivo que o Vite tentará resolver
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
  },
  
  // Configurações de plugins
  plugins: [
    // Plugin para lidar com arquivos CSS
    {
      name: 'css-post-process',
      enforce: 'post',
      transformIndexHtml(html) {
        // Adicionar links para CSS gerados
        return html.replace(
          '</head>',
          `  <link rel="stylesheet" href="/static/dist/assets/styles-.css">\n  </head>`
        );
      },
    },
  ],
  
  // Configurações de otimização
  optimizeDeps: {
    // Incluir dependências que devem ser pré-bundled
    include: [
      'alpinejs',
      'chart.js',
      'axios',
      'htmx.org',
      '@fortawesome/fontawesome-free',
      'flowbite',
    ],
    // Excluir dependências que não devem ser pré-bundled
    exclude: [
      // Excluir dependências que devem ser carregadas diretamente
    ],
  },
  
  // Configurações de CSS
  css: {
    // Pré-processadores de CSS
    preprocessorOptions: {
      // Configurações para SCSS
      scss: {
        additionalData: `@import "@/styles/variables.scss";`,
      },
    },
    // Módulos CSS
    modules: {
      // Gerar nomes de classes únicos
      generateScopedName: '[name]__[local]___[hash:base64:5]',
    },
  },
  
  // Configurações de assets
  assetsInclude: [
    // Tipos de arquivo que devem ser tratados como assets
    '**/*.md',
    '**/*.yml',
    '**/*.yaml',
    '**/*.json',
    '**/*.svg',
    '**/*.png',
    '**/*.jpg',
    '**/*.jpeg',
    '**/*.gif',
    '**/*.webp',
    '**/*.ico',
    '**/*.woff',
    '**/*.woff2',
    '**/*.ttf',
    '**/*.eot',
  ],
  
  // Configurações de log
  logLevel: 'info',
  
  // Configurações de cache
  cacheDir: 'node_modules/.vite',
  
  // Configurações de ambiente
  define: {
    // Definir variáveis de ambiente
    __VITE_VERSION__: JSON.stringify(process.env.npm_package_version || '0.0.0'),
    __VITE_MODE__: JSON.stringify(process.env.NODE_ENV || 'development'),
  },
  
  // Configurações específicas para desenvolvimento
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
});