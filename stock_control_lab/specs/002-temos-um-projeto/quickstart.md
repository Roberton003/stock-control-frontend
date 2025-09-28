# Guia de Início Rápido (Quickstart)

Este guia fornece as instruções para configurar e executar o ambiente de desenvolvimento local.

## Pré-requisitos

- Python 3.11+
- Node.js 20.x+
- Git

## Configuração do Backend (Django)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Roberton003/stock-control-lab.git
   cd stock-control-lab
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências do Python:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor de desenvolvimento do Django:**
   ```bash
   python manage.py runserver
   ```
   O backend estará rodando em `http://127.0.0.1:8000`.

## Configuração do Frontend (Vue.js)

1. **Navegue até o diretório do frontend:**
   ```bash
   cd stock-control-lab
   ```

2. **Instale as dependências do Node.js:**
   ```bash
   npm install
   ```

3. **Inicie o servidor de desenvolvimento do Vite:**
   ```bash
   npm run dev
   ```
   O frontend estará rodando em `http://localhost:3000` e se comunicará com o backend.

## Executando os Testes

- **Backend (pytest):**
  ```bash
  pytest
  ```

- **Frontend (vitest):**
  ```bash
  cd stock-control-lab
  npm test
  ```

- **Frontend E2E (Playwright):**
  ```bash
  cd stock-control-lab
  npm run test:e2e
  ```
