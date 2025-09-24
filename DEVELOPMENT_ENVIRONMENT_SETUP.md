# Documentação de Configuração do Ambiente de Desenvolvimento - Stock Control Lab

## Visão Geral

Este guia detalha o processo de configuração do ambiente de desenvolvimento para o projeto Stock Control Lab, um sistema de controle de estoque para laboratórios químicos desenvolvido com Django (backend) e Vue.js (frontend) em um monorepo.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em seu sistema:

### Backend (Django)
- **Python 3.8+**
- **pip** (gerenciador de pacotes Python)
- **virtualenv** (recomendado para isolar dependências)
- **Git** para controle de versão

### Frontend (Vue.js)
- **Node.js 16.x+**
- **npm** ou **yarn** (gerenciador de pacotes Node.js)

### Banco de Dados
- O projeto utiliza **SQLite** para desenvolvimento (não requer instalação adicional)
- **PostgreSQL** para produção (instalação opcional para testes de produção)

### Opcionais
- **Docker e Docker Compose** (para ambiente de produção futura)
- **Git Bash** (no Windows) ou terminal Unix/Linux/Mac

## Estrutura do Projeto

```
stock-control-lab/
├── backend/                 # Código do backend Django
│   ├── config/              # Configurações do projeto Django
│   ├── inventory/           # App principal com modelos e APIs
│   ├── templates/           # Templates HTML (futuro)
│   ├── static/              # Arquivos estáticos
│   ├── manage.py            # Script de gerenciamento Django
│   ├── requirements.txt     # Dependências do backend
│   └── db.sqlite3           # Banco de dados SQLite (desenvolvimento)
├── src/                     # Código do frontend Vue.js
├── public/                  # Arquivos públicos do frontend
├── tests/                   # Testes unitários do frontend
├── e2e_tests/               # Testes de integração
├── package.json             # Configuração do frontend (npm)
├── README.md                # Documentação geral
└── LICENSE                  # Licença do projeto
```

## Configuração do Backend (Django)

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd stock-control-lab/stock-control-lab
```

### 2. Configurar Ambiente Virtual Python

```bash
# Navegar para o diretório do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Ativar ambiente virtual (Windows)
# Windows CMD
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências do Backend

```bash
# Com o ambiente virtual ativado no diretório backend/
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente (Opcional)

O sistema pode usar variáveis de ambiente para configurações específicas. Crie um arquivo `.env` na pasta `backend/`:

```bash
# backend/.env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
DJANGO_SETTINGS_MODULE=config.settings
```

### 5. Rodar Migrações do Banco de Dados

```bash
# No diretório backend/, com o ambiente virtual ativado
python manage.py migrate
```

### 6. Criar Superusuário (Opcional)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar o superusuário administrativo.

### 7. Rodar o Servidor de Desenvolvimento do Backend

```bash
python manage.py runserver
```

O servidor backend estará disponível em `http://localhost:8000`

## Configuração do Frontend (Vue.js)

### 1. Instalar Dependências do Frontend

```bash
# No diretório root do projeto (stock-control-lab/stock-control-lab)
npm install
```

### 2. Verificar Configurações do Frontend

O projeto frontend já está configurado com:

- **Vue.js 3** com Composition API
- **Vite** como bundler
- **Tailwind CSS** para estilização
- **Pinia** para gerenciamento de estado
- **Vue Router** para navegação
- **Axios** para chamadas à API

Arquivos de configuração:
- `vite.config.js` - Configurações do Vite
- `tailwind.config.js` - Configurações do Tailwind CSS
- `package.json` - Dependências e scripts do projeto

### 3. Configuração da API no Frontend

A URL base da API está configurada no arquivo `src/plugins/axios.js`:

```javascript
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // URL base do backend
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

Certifique-se de que esta URL aponta para o servidor backend em execução.

## Configuração Completa do Ambiente

### 1. Iniciar Backend e Frontend Simultaneamente

Para desenvolvimento, é necessário ter ambos os servidores rodando:

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate  # Linux/Mac
python manage.py runserver
```

Terminal 2 (Frontend):
```bash
# No diretório root
npm run dev
```

### 2. Endereços de Serviço

- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`
- **API**: `http://localhost:8000/api/v1/`
- **Admin Django**: `http://localhost:8000/admin/`

### 3. Configuração de CORS

O backend já está configurado para permitir requisições do frontend. A configuração está no arquivo `config/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## Execução de Testes

### Testes do Backend (Django)

```bash
# No diretório backend/, com ambiente virtual ativado
python -m pytest
```

Para ver a cobertura de testes:
```bash
python -m pytest --cov=inventory --cov-report=html
```

### Testes do Frontend (Vitest)

```bash
# No diretório root
npm test
```

### Testes de Integração (Playwright)

```bash
# No diretório root
npx playwright test
```

Para abrir o Playwright UI:
```bash
npx playwright test --ui
```

## Scripts Disponíveis

No diretório root do projeto, os seguintes scripts npm estão disponíveis:

- `npm run dev` - Inicia o servidor de desenvolvimento do frontend
- `npm test` - Executa os testes unitários do frontend
- `npm run test:ui` - Executa os testes com interface visual
- `npm run preview` - Pré-visualiza o build de produção

## Build de Produção do Frontend

Para gerar o build de produção do frontend:

```bash
npm run build
```

O build será gerado no diretório `dist/` e pode ser servido como arquivos estáticos.

## Troubleshooting

### Problemas Comuns

1. **Erro: Porta já em uso**
   - Verifique se já há um processo rodando na porta 8000 (backend) ou 3000 (frontend)
   - Altere as portas com `python manage.py runserver 8001` ou `npm run dev -- --port 3001`

2. **Erro: Módulo não encontrado**
   - Verifique se o ambiente virtual está ativado
   - Execute novamente `pip install -r requirements.txt` ou `npm install`

3. **Erro: Falha na comunicação API**
   - Verifique se o backend está rodando
   - Confirme se a URL da API no frontend está correta
   - Verifique as configurações de CORS

### Verificação de Status do Sistema

Para verificar se todos os componentes estão funcionando:

```bash
# Verificar backend
curl -I http://localhost:8000/

# Verificar API
curl -I http://localhost:8000/api/v1/reagents/

# Verificar frontend (depois de iniciar)
curl -I http://localhost:3000/
```

## Atualização do Sistema

Para atualizar o sistema com as últimas alterações:

```bash
# Atualizar código-fonte
git pull origin main

# Atualizar dependências do backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Atualizar dependências do frontend
cd ..
npm install

# Executar migrações do banco de dados (se houver alterações)
cd backend
python manage.py migrate
```

## Considerações Finais

- O ambiente de desenvolvimento está otimizado para desenvolvimento local
- Use ambientes separados para desenvolvimento, staging e produção
- Mantenha suas dependências atualizadas mas testando antes de atualizar
- Faça backup do banco de dados antes de executar migrações

Este ambiente de desenvolvimento está configurado para suportar o desenvolvimento ágil e testes contínuos do sistema Stock Control Lab.