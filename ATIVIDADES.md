# 🎯 Plano de Atividades: Stock Control Lab 🎯

---

## ✅ Concluído

### 🚀 Setup e Configuração Inicial
- ✅ Verificar e configurar ambiente de desenvolvimento local para backend (Python, Django)
- ✅ Criar banco de dados de desenvolvimento (SQLite ou PostgreSQL)
- ✅ Configurar variáveis de ambiente para desenvolvimento
- ✅ Verificar e configurar ambiente de desenvolvimento local para frontend (Node.js, npm)
- ✅ Instalar dependências do frontend (npm install)

### ⚙️ Configuração dos Servidores
- ✅ Rodar migrações do banco de dados do backend
- ✅ Criar superusuário para acesso ao admin do Django
- ✅ Iniciar servidor de desenvolvimento do backend (Django)
- ✅ Verificar endpoints da API estão acessíveis
- ✅ Configurar URL base da API no frontend para apontar para o backend local
- ✅ Iniciar servidor de desenvolvimento do frontend (Vite)
- ✅ Verificar que o frontend carrega corretamente no navegador

### 🔗 Integração
- ✅ Configurar CORS no backend para permitir requisições do frontend
- ✅ Verificar autenticação e autorização entre frontend e backend
- ✅ Testar fluxos completos de usuário (CRUD de reagentes, lotes, movimentações)
- ✅ Verificar funcionamento do dashboard e relatórios

### 🧪 Testes
- ✅ Executar testes unitários do backend
- ✅ Verificar performance e tempo de resposta das APIs

### 🛠️ Correções de Erros
- ✅ Corrigir erro no dashboard relacionado ao uso incorreto do módulo datetime
- ✅ Corrigir erro no relatório de perda/desperdício relacionado ao uso incorreto de datetime.strptime
- ✅ Ajustar tempo limite do teste de performance de lotes de estoque
- ✅ Criar fixture de cliente autenticado para os testes de API
- ✅ Atualizar testes de API para usar o cliente autenticado
- ✅ Corrigir problema com a criação de movimentações de estoque no teste de API

### 📋 Atividades do Dia 23/09/2025
- ✅ Concluir correções de testes de API
- ✅ Garantir integração completa frontend/backend
- ✅ Atualizar documentação e sistema de tarefas
- ✅ Fazer versionamento das alterações

---

## 📝 Próximas Atividades

### 🔴 Integração (Prioridade Alta)
- [x] Testar sistema de requisições e aprovações
- [ ] Verificar tratamento de erros e validações

### 🟡 Testes (Prioridade Média)
- [ ] Executar testes unitários do frontend
- [ ] Executar testes de integração entre frontend e backend

### 🟡 Documentação (Prioridade Média)
- [ ] Atualizar documentação da API com endpoints e exemplos
- [ ] Documentar processo de configuração do ambiente de desenvolvimento
- [ ] Criar guia de desenvolvimento para novos contribuidores
- [ ] Documentar arquitetura do sistema e fluxos de dados

### 🟡 Deployment (sem Docker) (Prioridade Média/Alta)
- [ ] Criar script de build do frontend
- [ ] Configurar coleta de arquivos estáticos do Django
- [ ] Preparar ambiente de produção (sem Docker ainda)
- [ ] Testar deploy em ambiente de staging

### 🔵 Docker (somente após tudo funcionando) (Prioridade Baixa)
- [ ] Criar Dockerfile para o backend
- [ ] Criar Dockerfile para o frontend
- [ ] Criar docker-compose.yml para orquestração
- [ ] Testar ambiente Docker em desenvolvimento
- [ ] Testar ambiente Docker em produção
