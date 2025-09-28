// postcss.config.js - Configuração do PostCSS para o projeto

module.exports = {
  plugins: {
    // Plugin para processar CSS aninhado
    'postcss-nested': {},
    
    // Plugin para importar outros arquivos CSS
    'postcss-import': {},
    
    // Plugin para utilizar variáveis CSS no Tailwind
    'tailwindcss': {},
    
    // Plugin para adicionar prefixos de vendor automaticamente
    'autoprefixer': {},
    
    // Plugin para otimizar CSS em produção
    '@fullhuman/postcss-purgecss': {
      content: [
        './templates/**/*.html',
        './static/src/**/*.js',
        './static/src/**/*.css',
        './static/src/**/*.vue',
      ],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
      safelist: [
        // Classes que podem ser usadas dinamicamente e não aparecem no HTML
        'dark',
        'show',
        'active',
        'hidden',
        'block',
        'flex',
        'grid',
        // Cores que podem ser usadas dinamicamente
        /^bg-/,
        /^text-/,
        /^border-/,
        /^hover:/,
        /^focus:/,
        /^dark:/,
        // Classes de animação
        /^animate-/,
        /^transition-/,
        /^duration-/,
        /^delay-/,
        // Classes de espaçamento
        /^p-/,
        /^m-/,
        /^px-/,
        /^py-/,
        /^mx-/,
        /^my-/,
        // Classes de tamanho
        /^w-/,
        /^h-/,
        /^min-/,
        /^max-/,
        // Classes de layout
        /^grid-/,
        /^flex-/,
        /^items-/,
        /^justify-/,
        // Classes de tipografia
        /^font-/,
        /^text-/,
        // Classes de sombra
        /^shadow-/,
        // Classes de borda
        /^rounded-/,
        /^border-/,
        // Classes de cursor
        /^cursor-/,
        // Classes de visibilidade
        /^opacity-/,
        // Classes de transformação
        /^transform/,
        /^scale-/,
        /^rotate-/,
        /^translate-/,
        // Classes de z-index
        /^z-/,
      ]
    }
  }
}