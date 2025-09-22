# Stock Control Lab - Backend

Sistema de controle de estoque para laboratórios químicos, desenvolvido com Django e Django REST Framework.

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

### Backend
- Django 5.2+
- Django REST Framework 3.14+
- Celery 5.3+ para tarefas assíncronas
- Redis 4.5+ para mensagens e cache
- PostgreSQL 15+ como banco de dados
- Django Celery Beat para agendamento de tarefas

### Testes
- Pytest 7.4+
- Pytest-Django 4.5+
- Freezegun 1.2+ para testes de data/hora

### Integração Contínua
- GitHub Actions

## Estrutura do Projeto

```
backend/
├── config/              # Configurações do projeto Django
├── inventory/           # App principal com modelos e APIs
│   ├── models.py        # Modelos de dados
│   ├── views.py         # Views/APIs
│   ├── serializers.py   # Serializers para APIs
│   ├── services.py      # Lógica de negócio
│   ├── tasks.py         # Tarefas assíncronas do Celery
│   ├── urls.py          # URLs da API
│   ├── admin.py         # Configurações do Django Admin
│   ├── apps.py          # Configurações do app
│   ├── signals.py       # Sinais do Django
│   ├── utils.py         # Funções auxiliares
│   ├── tests/           # Testes unitários e de integração
│   └── migrations/      # Migrações do banco de dados
├── templates/           # Templates HTML (para views renderizadas)
├── static/              # Arquivos estáticos
├── manage.py            # Script de gerenciamento do Django
├── requirements.txt     # Dependências do projeto
├── pytest.ini           # Configuração dos testes
└── db.sqlite3          # Banco de dados (desenvolvimento)
```

## Desenvolvimento

### Pré-requisitos
- Python >= 3.8
- Docker e Docker Compose (recomendado)
- PostgreSQL >= 12.x (se não usar Docker)

### Configuração do Ambiente

1. Criar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Rodar migrações:
```bash
python manage.py migrate
```

4. Criar superusuário (opcional):
```bash
python manage.py createsuperuser
```

5. Rodar o servidor de desenvolvimento:
```bash
python manage.py runserver
```

### Execução com Docker
```bash
docker-compose up --build
```

### Testes
```bash
pytest
```

## API Endpoints

A API está disponível em `/api/v1/` com os seguintes endpoints principais:

- `POST /api/v1/reagents/` - Criar reagente
- `GET /api/v1/reagents/` - Listar reagentes
- `GET /api/v1/reagents/{id}/` - Detalhes de um reagente
- `PUT /api/v1/reagents/{id}/` - Atualizar reagente
- `DELETE /api/v1/reagents/{id}/` - Deletar reagente

- `POST /api/v1/stock-lots/` - Criar lote de estoque
- `GET /api/v1/stock-lots/` - Listar lotes
- `POST /api/v1/stock-movements/` - Registrar movimentação

- `POST /api/v1/requisitions/` - Criar requisição
- `POST /api/v1/requisitions/{id}/action/` - Aprovar/rejeitar requisição

- `GET /api/v1/dashboard/summary/` - Resumo do dashboard
- `GET /api/v1/reports/financial/` - Relatório financeiro

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](../LICENSE) para detalhes.

## Contato

Roberto Nascimento - roberto.m0010@gmail.com

Link do Projeto: [https://github.com/Roberton003/stock-control-lab](https://github.com/Roberton003/stock-control-lab)