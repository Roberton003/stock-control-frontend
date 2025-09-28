# Stack do Projeto Frontend Protótipo

Este documento descreve a stack tecnológica recomendada para o desenvolvimento do frontend do aplicativo web responsivo que consumirá as APIs do sistema de controle de estoque laboratorial.

## Tecnologias Principais

### Framework Frontend
- **Vue.js 3** (Composition API)
  - Framework progressivo e leve
  - Curva de aprendizado menor comparado a React/Angular
  - Excelente desempenho e tamanho reduzido do bundle

### Bundler
- **Vite**
  - Desenvolvimento extremamente rápido com Hot Module Replacement (HMR)
  - Suporte nativo a TypeScript, JSX, CSS, etc.
  - Build otimizado para produção

### Estilização
- **Tailwind CSS**
  - Framework CSS utility-first
  - Permite criar designs responsivos e elegantes rapidamente
  - Alta personalização através do arquivo de configuração

### Gerenciamento de Estado
- **Pinia**
  - Gerenciamento de estado oficial para Vue.js
  - Mais simples e intuitivo que Vuex
  - Suporte a Composition API

### Roteamento
- **Vue Router 4**
  - Roteamento oficial para Vue.js 3
  - Suporte a rotas aninhadas, guards de navegação, etc.

### Cliente HTTP
- **Axios**
  - Cliente HTTP robusto e amplamente utilizado
  - Interceptadores para tratamento de requisições/respostas
  - Cancelamento de requisições

### Ícones
- **Font Awesome**
  - Biblioteca completa de ícones vetoriais
  - Suporte a ícones gratuitos e pro
  - Fácil integração com Vue.js

## Estrutura de Pastas

```
src/
├── assets/              # Imagens, fonts, ícones
├── components/          # Componentes reutilizáveis
│   ├── layout/         # Header, Sidebar, Footer
│   ├── ui/             # Botões, cards, inputs, tabelas
│   └── dashboard/      # Componentes específicos do dashboard
├── views/              # Telas principais da aplicação
│   ├── Dashboard.vue
│   ├── Reagents/
│   ├── StockLots/
│   ├── Requisitions/
│   └── Reports/
├── services/           # Integração com a API
├── stores/             # Gerenciamento de estado (Pinia)
├── router/             # Configuração de rotas
├── utils/              # Funções auxiliares
└── styles/             # Estilos globais e temas
```

## Componentes Específicos

### Componentes de Layout
- `AppHeader.vue` - Cabeçalho da aplicação
- `AppSidebar.vue` - Barra lateral de navegação
- `AppFooter.vue` - Rodapé
- `AppLayout.vue` - Layout principal

### Componentes UI
- `Button.vue` - Botões estilizados
- `Card.vue` - Cards para conteúdo
- `Table.vue` - Tabelas responsivas
- `Input.vue` - Campos de entrada
- `Select.vue` - Seletores
- `Modal.vue` - Modais e diálogos
- `Alert.vue` - Alertas e notificações
- `Badge.vue` - Indicadores e tags
- `Spinner.vue` - Indicador de carregamento

### Componentes Dashboard
- `SummaryCard.vue` - Cards de resumo
- `Chart.vue` - Componente de gráficos
- `RecentActivity.vue` - Lista de atividades recentes
- `ExpirationAlert.vue` - Alertas de validade

## Configuração de Cores (Tailwind)

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#0C4B6A',      // Azul petróleo
        secondary: '#3DBEA3',    // Verde água
        accent: '#FF6B35',       // Laranja
        light: '#F8F9FA',        // Cinza claro
        dark: '#2D3748',         // Cinza escuro
      }
    }
  }
}
```

## Estratégia de Desenvolvimento

### 1. Setup Inicial
- Criar projeto Vue com Vite
- Configurar Tailwind CSS
- Instalar dependências necessárias
- Configurar estrutura de pastas

### 2. Componentes Base
- Criar layout principal (header, sidebar, footer)
- Desenvolver componentes UI reutilizáveis
- Implementar sistema de rotas

### 3. Integração com API
- Criar serviços para comunicação com API
- Configurar interceptadores para tratamento de erros
- Implementar autenticação (se necessário)

### 4. Telas Principais
- Dashboard com métricas e gráficos
- Listagem e detalhes de reagentes
- Gestão de lotes de estoque
- Sistema de requisições
- Relatórios

### 5. Funcionalidades Avançadas
- Filtros e buscas avançadas
- Paginação de listas
- Validações de formulários
- Notificações e alertas
- Exportação de dados

## Boas Práticas

### Organização de Código
- Componentes com nomes descritivos em PascalCase
- Props tipadas com validação
- Uso de composables para lógica reutilizável
- Separação clara entre lógica de apresentação e negócio

### Performance
- Lazy loading de rotas
- Componentes assíncronos quando apropriado
- Virtual scrolling para listas grandes
- Memoização de computações pesadas

### Acessibilidade
- Atributos ARIA adequados
- Navegação por teclado
- Contraste de cores adequado
- Labels descritivos

### Responsividade
- Breakpoints personalizados no Tailwind
- Componentes adaptáveis
- Mobile-first approach
- Touch targets adequados para dispositivos móveis

## Dependências Necessárias

```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.4.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0",
    "@fortawesome/fontawesome-free": "^6.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

## Recursos Visuais Específicos

### Sistema de Alertas por Validade
- Verde: Produtos válidos (> 90 dias para vencer)
- Amarelo: Produtos próximos ao vencimento (30-90 dias)
- Vermelho: Produtos vencidos ou próximos (< 30 dias)

### Gráficos
- Utilizar biblioteca Chart.js com wrapper para Vue
- Gráficos de barras para consumo por período
- Gráficos de pizza para distribuição de estoque
- Gráficos de linha para tendências

### Design System
- Consistência visual em toda a aplicação
- Componentes reutilizáveis com props configuráveis
- Temas claros e escuros (opcional)
- Animações sutis para melhor experiência do usuário

## Considerações Finais

Esta stack proporciona um equilíbrio ideal entre simplicidade e poder, permitindo o desenvolvimento rápido de uma aplicação web moderna e responsiva que se integra perfeitamente com as APIs existentes. A escolha de Vue.js com Tailwind CSS garante uma curva de aprendizado acessível mesmo para desenvolvedores menos experientes, enquanto mantém a capacidade de criar interfaces sofisticadas e altamente funcionais.