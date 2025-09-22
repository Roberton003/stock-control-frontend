# Controle de Atividades - Integração Backend/Frontend

## Setup e Configuração Inicial

### Backend
- [x] Verificar e configurar ambiente de desenvolvimento local para backend (Python, Django)
- [x] Criar banco de dados de desenvolvimento (SQLite ou PostgreSQL)
- [x] Configurar variáveis de ambiente para desenvolvimento

### Frontend
- [x] Verificar e configurar ambiente de desenvolvimento local para frontend (Node.js, npm)
- [x] Instalar dependências do frontend (npm install)

## Configuração do Backend

- [x] Rodar migrações do banco de dados do backend
- [x] Criar superusuário para acesso ao admin do Django
- [x] Iniciar servidor de desenvolvimento do backend (Django)
- [x] Verificar endpoints da API estão acessíveis

## Configuração do Frontend

- [x] Configurar URL base da API no frontend para apontar para o backend local
- [x] Criar script de build do frontend
- [x] Corrigir erros no frontend (se necessário)
- [x] Copiar arquivos do build do frontend para diretório static do Django

## Integração

- [x] Configurar Django para servir arquivos estáticos do frontend
- [x] Configurar URLs do Django para servir o frontend
- [ ] Testar integração backend/frontend acessando localhost:8000
- [ ] Verificar chamadas da API do frontend para o backend

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