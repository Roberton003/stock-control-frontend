# Stock Control Lab

Sistema de controle de estoque para laboratórios químicos, desenvolvido como monorepo com frontend e backend integrados.

## Funcionalidades Principais

### Controle de Reagentes
- Cadastro completo de reagentes químicos
- Classificação por categorias (ácidos, bases, sais, etc.)
- Definição de quantidade mínima em estoque
- Unidades de medida configuráveis

### Gestão de Lotes
- Registro detalhado de lotes de estoque
- Controle de datas de validade
- Associação com fornecedores e localizações
- Alertas automáticos para produtos próximos ao vencimento

### Movimentações de Estoque
- Registro de entradas e saídas
- Histórico completo de movimentações
- Rastreamento de responsáveis pelas transações
- Justificativas para cada movimentação

### Sistema de Requisições
- Interface para solicitação de materiais
- Fluxo de aprovação/rejeição
- Acompanhamento de status das requisições
- Histórico de requisições anteriores

### Relatórios e Dashboards
- Visão geral do estado do estoque
- Gráficos de consumo por período
- Alertas de produtos com estoque baixo
- Relatórios exportáveis (PDF, Excel, CSV)

## Tecnologias Utilizadas

### Frontend
- Vue.js 3 com Composition API
- Vite como bundler
- Tailwind CSS para estilização
- Pinia para gerenciamento de estado
- Vue Router para navegação
- Axios para requisições HTTP

### Backend
- Django 5.2+ com Django REST Framework
- PostgreSQL como banco de dados
- Docker para containerização
- Django Celery para tarefas assíncronas
- Redis para cache e mensagens

### Infraestrutura
- GitHub Actions para CI/CD
- Docker Compose para orquestração
- Nginx como proxy reverso

## Arquitetura do Sistema

```
┌─────────────────┐    ┌────────────────────┐
│   Frontend      │    │     Backend        │
│  (Vue.js +      │    │ (Django REST API)  │
│   Tailwind)     │◄──►│                    │
└─────────────────┘    └────────────────────┘
                              │
                     ┌────────────────────┐
                     │   Banco de Dados   │
                     │    (PostgreSQL)    │
                     └────────────────────┘
```

## Estrutura do Projeto (Monorepo)

```
stock-control-lab/
├── backend/             # Código do backend Django
│   ├── config/          # Configurações do projeto
│   ├── inventory/       # App principal com modelos e APIs
│   ├── templates/       # Templates HTML
│   ├── static/          # Arquivos estáticos
│   ├── manage.py        # Script de gerenciamento do Django
│   ├── requirements.txt # Dependências do backend
│   └── README.md        # Documentação do backend
├── src/                 # Código do frontend Vue.js
│   ├── assets/          # Imagens, fonts, ícones
│   ├── components/      # Componentes reutilizáveis
│   ├── views/           # Telas principais da aplicação
│   ├── services/        # Integração com a API
│   ├── stores/          # Gerenciamento de estado (Pinia)
│   ├── router/          # Configuração de rotas
│   ├── utils/           # Funções auxiliares
│   └── styles/          # Estilos globais e temas
├── public/              # Arquivos públicos do frontend
├── tests/               # Testes end-to-end
├── docker-compose.yml   # Configuração do Docker Compose
├── README.md            # Este arquivo (documentação geral)
└── LICENSE              # Licença do projeto
```

## Desenvolvimento

### Pré-requisitos
- Node.js >= 16.x
- Python >= 3.8
- Docker e Docker Compose
- PostgreSQL >= 12.x

### Configuração do Frontend
```bash
npm install
npm run dev
```

### Configuração do Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Execução com Docker
```bash
docker-compose up --build
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Roberto Nascimento - roberto.m0010@gmail.com

Link do Projeto: [https://github.com/Roberton003/stock-control-lab](https://github.com/Roberton003/stock-control-lab)