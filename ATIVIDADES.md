# Controle de Atividades - Integração Backend/Frontend

## Setup e Configuração Inicial

### Backend
- [ ] Verificar e configurar ambiente de desenvolvimento local para backend (Python, Django)
- [ ] Criar banco de dados de desenvolvimento (SQLite ou PostgreSQL)
- [ ] Configurar variáveis de ambiente para desenvolvimento

### Frontend
- [ ] Verificar e configurar ambiente de desenvolvimento local para frontend (Node.js, npm)

## Configuração do Backend

- [ ] Rodar migrações do banco de dados do backend
- [ ] Criar superusuário para acesso ao admin do Django
- [ ] Iniciar servidor de desenvolvimento do backend (Django)
- [ ] Verificar endpoints da API estão acessíveis

## Configuração do Frontend

- [ ] Instalar dependências do frontend (npm install)
- [ ] Configurar URL base da API no frontend para apontar para o backend local
- [ ] Iniciar servidor de desenvolvimento do frontend (Vite)
- [ ] Verificar que o frontend carrega corretamente no navegador

## Integração

- [ ] Configurar CORS no backend para permitir requisições do frontend
- [ ] Verificar autenticação e autorização entre frontend e backend
- [ ] Testar fluxos completos de usuário (CRUD de reagentes, lotes, movimentações)
- [ ] Verificar funcionamento do dashboard e relatórios
- [ ] Testar sistema de requisições e aprovações
- [ ] Verificar tratamento de erros e validações

## Testes

- [ ] Executar testes unitários do backend
- [ ] Executar testes unitários do frontend
- [ ] Executar testes de integração entre frontend e backend
- [ ] Realizar testes manuais de todos os fluxos principais
- [ ] Verificar performance e tempo de resposta das APIs

## Documentação

- [ ] Atualizar documentação da API com endpoints e exemplos
- [ ] Documentar processo de configuração do ambiente de desenvolvimento
- [ ] Criar guia de desenvolvimento para novos contribuidores
- [ ] Documentar arquitetura do sistema e fluxos de dados

## Deployment (sem Docker)

- [ ] Criar script de build do frontend
- [ ] Configurar coleta de arquivos estáticos do Django
- [ ] Preparar ambiente de produção (sem Docker ainda)
- [ ] Testar deploy em ambiente de staging

## Docker (somente após tudo funcionando)

- [ ] Criar Dockerfile para o backend
- [ ] Criar Dockerfile para o frontend
- [ ] Criar docker-compose.yml para orquestração
- [ ] Testar ambiente Docker em desenvolvimento
- [ ] Testar ambiente Docker em produção