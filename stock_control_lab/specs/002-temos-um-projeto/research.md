# Phase 0: Pesquisa

## Decisão da Stack Tecnológica

A stack tecnológica foi determinada através da análise da estrutura e dos arquivos de configuração existentes no projeto.

- **Backend**:
  - **Linguagem**: Python 3.11+
  - **Framework**: Django 5.2+
  - **API**: Django REST Framework
  - **Tarefas Assíncronas**: Celery com Redis
  - **Banco de Dados**: SQLite para desenvolvimento local (com suporte a PostgreSQL)
  - **Testes**: Pytest com pytest-django

- **Frontend**:
  - **Framework**: Vue.js 3
  - **Build Tool**: Vite
  - **Gerenciamento de Estado**: Pinia
  - **Roteamento**: Vue Router
  - **Cliente HTTP**: Axios
  - **Estilização**: Tailwind CSS
  - **Testes**: Vitest para testes unitários e Playwright para testes E2E.

## Racional

A utilização da stack existente minimiza o retrabalho e aproveita o desenvolvimento já realizado. A escolha do Vue.js como frontend principal baseia-se na estrutura mais completa encontrada no subdiretório `stock-control-lab/`, em detrimento da configuração com Alpine.js/htmx na raiz do projeto, que parece ser secundária ou legada.

## Alternativas Consideradas

Nenhuma nova tecnologia foi considerada para manter a consistência com o trabalho já iniciado.
