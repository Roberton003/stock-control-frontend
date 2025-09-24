# Documentação de Arquitetura e Fluxos de Dados - Stock Control Lab

## Visão Geral do Sistema

O Stock Control Lab é um sistema web de controle de estoque desenvolvido especificamente para laboratórios químicos. O sistema segue uma arquitetura baseada em microserviços lógicos com frontend e backend separados, ambos integrados em um monorepo.

### Tipos de Arquitetura
- **Frontend**: Single Page Application (SPA) com Vue.js 3
- **Backend**: API RESTful com Django e Django REST Framework
- **Banco de Dados**: Armazenamento relacional com SQLite (desenvolvimento) ou PostgreSQL (produção)
- **Estrutura**: Monorepo com frontend e backend integrados

## Arquitetura do Sistema

### Visão Geral da Arquitetura

```
┌─────────────────┐    ┌────────────────────┐    ┌─────────────────────┐
│   Frontend      │    │     Backend        │    │   Banco de Dados    │
│  (Vue.js +      │◄──►│ (Django REST API)  │◄──►│ (SQLite/PostgreSQL) │
│   Tailwind)     │    │                    │    │                     │
└─────────────────┘    └────────────────────┘    └─────────────────────┘
        │                        │
        │                        │
        ▼                        ▼
┌─────────────────┐    ┌────────────────────┐
│   Navegador     │    │   Servidor Web     │
│   do Usuário    │    │  (Django Server)   │
└─────────────────┘    └────────────────────┘
```

### Componentes do Frontend

#### 1. Camada de Apresentação
- **Componentes Vue.js**: Elementos reutilizáveis da interface
  - Componentes de layout (header, sidebar, footer)
  - Componentes UI (botões, cards, tabelas, formulários)
  - Componentes de dashboard (gráficos, resumos)
- **Páginas/Views**: Telas específicas da aplicação
- **Templates**: Estrutura HTML das páginas
- **Estilos**: Tailwind CSS e estilos personalizados

#### 2. Camada de Comunicação
- **Serviços API**: Módulos que encapsulam chamadas à API
- **Cliente HTTP**: Axios configurado com interceptadores
- **Configuração de API**: URL base, headers, tratamento de erros

#### 3. Camada de Estado
- **Pinia Stores**: Gerenciamento de estado global
- **Composables**: Lógica reutilizável do Vue Composition API
- **State Management**: Dados compartilhados entre componentes

#### 4. Camada de Roteamento
- **Vue Router**: Gerenciamento de navegação
- **Rotas protegidas**: Verificação de autenticação
- **Guards de navegação**: Controle de acesso

### Componentes do Backend

#### 1. Camada de Apresentação (API)
- **Views**: Controladores da API REST
- **Serializers**: Conversão entre modelos Django e JSON
- **URLs**: Rotas da API
- **Permissões**: Controle de acesso

#### 2. Camada de Lógica de Negócio
- **Services**: Funções de negócio encapsuladas
- **Utils**: Funções auxiliares
- **Validators**: Validações de negócio

#### 3. Camada de Acesso a Dados
- **Models**: Definição da estrutura de dados (ORM)
- **Managers**: Consultas personalizadas ao banco de dados
- **Migrations**: Histórico de alterações no banco de dados

#### 4. Camada de Infraestrutura
- **Configurações**: Configuração do Django
- **Middlewares**: Processamento de requisições/respostas
- **Signals**: Disparadores de ações pós-evento

## Modelos de Dados

### Principais Entidades

#### Reagent
- Relação com: Category, Supplier, Location
- Campos: nome, descrição, categoria, fornecedor, localização, quantidade mínima, unidade de medida
- Fluxos: cadastro, edição, listagem, exclusão, movimentações

#### Stock Lot (Lote de Estoque)
- Relação com: Reagent, Location
- Campos: número do lote, localização, data de validade, preço de compra, quantidade inicial e atual, data de entrada
- Fluxos: cadastro, edição, listagem, controle de movimentações

#### Stock Movement (Movimentação de Estoque)
- Relação com: Stock Lot, User
- Campos: tipo (entrada, saída, ajuste, descarte), quantidade, usuário, data/hora, observações
- Fluxos: registro, estatísticas, relatórios

#### Requisition (Requisição)
- Relação com: Reagent, User (requester, approved_by)
- Campos: reagente solicitado, quantidade, status, justificativa, usuário requisitante, aprovador
- Fluxos: criação, aprovação/rejeição, histórico

#### Category (Categoria)
- Relação com: Reagent
- Campos: nome, descrição
- Fluxos: cadastro, edição, listagem, associação a reagentes

#### Supplier (Fornecedor)
- Relação com: Reagent
- Campos: nome, contato, informações
- Fluxos: cadastro, edição, listagem, associação a reagentes

#### Location (Localização)
- Relação com: Reagent, Stock Lot
- Campos: nome, descrição, localização física
- Fluxos: cadastro, edição, listagem, associação a reagentes e lotes

## Fluxos de Dados

### 1. Fluxo de Cadastro de Reagente

```
1. Frontend → Backend: POST /api/v1/reagents/
2. Backend Valida Dados → Modelos
3. Backend Salva no BD → Resposta
4. Frontend Atualiza UI
```

### 2. Fluxo de Movimentação de Estoque

```
1. Frontend → Backend: POST /api/v1/stock-movements/
2. Backend Valida Estoques → Models
3. Backend Atualiza Quantidades → BD
4. Backend Cria Registro Movimentação → BD
5. Backend Retorna Confirmação → Frontend
6. Frontend Atualiza Interface → Usuário
```

### 3. Fluxo de Requisição e Aprovação

```
1. Usuário Solicita → Frontend: POST /api/v1/requisitions/
2. Frontend → Backend: Cria requisição com status 'pendente'
3. Aprovador Visualiza → Backend: GET /api/v1/requisitions/
4. Aprovador Decide → Backend: POST /api/v1/requisitions/{id}/action/
5. Backend Processa → Atualiza Status
6. Frontend Atualiza Interface
```

### 4. Fluxo de Relatório de Dashboard

```
1. Frontend → Backend: GET /api/v1/dashboard/summary/
2. Backend Consulta Múltiplas Tabelas → Calcula Estatísticas
3. Backend Retorna Dados Agregados → Frontend
4. Frontend Renderiza Gráficos e Métricas
```

## Segurança e Autenticação

### Mecanismos Implementados

#### Autenticação
- **Token JWT**: Autenticação baseada em tokens
- **Login/Logout**: Endpoints de autenticação
- **Storage**: Tokens armazenados em localStorage

#### Autorização
- **Permissões por Função**: Baseadas em papéis de usuário
- **Controle de Acesso**: Nível de endpoint e objeto
- **Valiação de Token**: Interceptadores verificam tokens válidos

### Proteção de Dados
- **Validação de Entrada**: Serializers e validadores no backend
- **Sanitização**: Tratamento de entradas para prevenir XSS
- **Proteção CSRF**: Implementada pelo Django

## Performance e Otimização

### Estratégias Implementadas

#### Backend
- **Indexação de Banco de Dados**: Campos frequentemente consultados indexados
- **Consulta Otimizada**: Uso de select_related e prefetch_related
- **Cache**: Implementação planejada com Redis

#### Frontend
- **Componentização**: Componentes reutilizáveis e otimizados
- **Roteamento Lazy Loading**: Carregamento sob demanda de funcionalidades
- **Gestão de Estado**: Pinia para otimizar re-renderizações

### Estratégias Futuras
- **Paginação**: Implementação em listagens extensas
- **Caching HTTP**: Headers de cache apropriados
- **Otimização de Assets**: Minificação e compressão

## Testes e Qualidade de Código

### Estratégia de Testes

#### Backend (Pytest)
- **Testes Unitários**: Lógica de negócio nos services
- **Testes de API**: Endpoints e serialização
- **Testes de Integração**: Fluxos completos de negócio
- **Testes de Performance**: Verificação de tempo de resposta

#### Frontend (Vitest + Playwright)
- **Testes Unitários**: Componentes e composables Vue
- **Testes de Integração**: Interações entre módulos
- **Testes E2E**: Fluxos completos de usuário
- **Testes de Interface**: Validação visual e comportamento

## Integração e Deploy

### Estratégia de Integração
- **CI/CD Planejado**: GitHub Actions para integração contínua
- **Testes Automatizados**: Execução automática de testes
- **Verificação de Qualidade**: Análise de cobertura e qualidade de código

### Estratégia de Deploy
- **Frontend**: Build estático servido via Django
- **Backend**: Servidor Django com coleta de estáticos
- **Docker**: Planejado para containerização futura
- **Ambientes**: Desenvolvimento, staging e produção

## Módulos e Componentes Específicos

### Módulo de Dashboard
- **Resumo Estatístico**: Métricas principais do sistema
- **Gráficos de Tendência**: Consumo e movimentações ao longo do tempo
- **Alertas**: Produtos com estoque baixo ou vencendo

### Módulo de Controle de Estoque
- **Controle de Lotes**: Rastreamento por número de lote
- **Movimentações**: Registro detalhado de entradas e saídas
- **Contagem Física**: Sincronização com estoque real

### Módulo de Requisições
- **Fluxo de Aprovação**: Processo de autorização configurável
- **Histórico**: Rastreamento de todas as requisições
- **Relatórios**: Análise de padrões de solicitação

### Módulo de Relatórios
- **Relatórios Financeiros**: Valor de estoque e movimentações monetárias
- **Relatórios de Consumo**: Análise de uso de reagentes
- **Relatórios de Validade**: Produtos próximos ao vencimento
- **Exportação**: Formatos Excel, PDF e CSV

## Considerações de Escalabilidade

### Backend
- **Modelos Otimizados**: Estrutura de dados eficiente
- **Consultas Indexadas**: Performance para grandes volumes
- **Separação de Responsabilidades**: Arquitetura modular

### Frontend
- **Componentização**: Reutilização e manutenção
- **Lazy Loading**: Carregamento sob demanda
- **Gestão de Estado**: Evita sobrecarga de dados

## Melhores Práticas Arquiteturais Implementadas

1. **Separação de Responsabilidades**: Backend lógico separado de frontend
2. **API Restful**: Interface padronizada de comunicação
3. **Modelo em Camadas**: Separação clara entre apresentação, negócio e dados
4. **Desacoplamento**: Componentes independentes e reutilizáveis
5. **Padrões de Projeto**: Seguindo melhores práticas do Django e Vue.js
6. **Testabilidade**: Arquitetura projetada para fácil testagem
7. **Manutenibilidade**: Código organizado e documentado
8. **Segurança**: Práticas de segurança implementadas em vários níveis