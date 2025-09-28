# Quickstart Guide: Testes de Controle de Estoque na Web

**Feature Number**: 003  
**Feature Branch**: `003-gostaria-que-testassemos`  
**Created**: 27 de setembro de 2025

## Overview
Este guia fornece instruções para executar testes abrangentes no sistema de controle de estoque em ambiente web local.

## Environment Setup

### 1. Pré-requisitos
- Python 3.8+
- Node.js 16+
- Sistema operacional Linux, Windows ou macOS

### 2. Configuração do ambiente
```bash
# Clone o repositório (se necessário)
git clone <url-do-repositorio>
cd stock_control_lab

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Instale as dependências de frontend
npm install
```

### 3. Configuração do banco de dados
```bash
# Execute as migrações
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser
```

## Running Tests

### 1. Iniciar o servidor de desenvolvimento
```bash
# Terminal 1: Iniciar o servidor Django
python manage.py runserver

# Terminal 2: Iniciar o servidor Vite (se necessário)
npm run dev
```

### 2. Executar testes automatizados
```bash
# Testes unitários e de integração
python -m pytest

# Testes de interface (se configurados)
# Exemplo com Playwright:
playwright install
python -m pytest e2e_tests/
```

## Testing Checklist

### 1. Login e Autenticação
- [ ] Acesso à página de login
- [ ] Validação de credenciais
- [ ] Redirecionamento após login
- [ ] Funcionalidade de logout
- [ ] Recuperação de senha

### 2. Navegação
- [ ] Acesso ao dashboard
- [ ] Navegação por menus
- [ ] Funcionalidade de todos os links
- [ ] Comportamento de botões de navegação
- [ ] Histórico de navegação

### 3. Funcionalidades de Produtos
- [ ] Visualização de lista de produtos
- [ ] Criação de novos produtos
- [ ] Edição de produtos existentes
- [ ] Remoção de produtos
- [ ] Filtros e busca

### 4. Componentes UI
- [ ] Botões e sua funcionalidade
- [ ] Formulários e validações
- [ ] Tabelas e sua interatividade
- [ ] Modais e popups
- [ ] Feedback visual (alerts, toasts)

## Expected Outcomes

### Success Criteria
- Todos os testes automatizados passando
- Navegação sem erros
- Funcionalidades CRUD operando corretamente
- Interações de UI respondendo adequadamente
- Dados sendo persistidos corretamente

### Common Issues to Verify
- Erros de autenticação
- Problemas de carregamento de páginas
- Falhas em validações de formulário
- Erros de permissão
- Problemas de conexão com o banco de dados