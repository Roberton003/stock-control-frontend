# Teste de Deploy em Ambiente de Staging - Stock Control Lab

## Visão Geral

Este documento descreve o processo de teste de deploy do Stock Control Lab em ambiente de staging, que serve como ambiente de pré-produção para validação final antes do deploy em produção.

## Configuração do Ambiente de Staging

### 1. Provisionamento do Servidor de Staging

O ambiente de staging deve ser o mais próximo possível do ambiente de produção para garantir validade nos testes:

#### Requisitos Mínimos
- Ubuntu 20.04 LTS ou superior
- 2GB RAM (4GB recomendado para staging)
- 10GB de armazenamento
- Acesso SSH com chave configurada
- Acesso à internet

#### Semelhança com Produção
- Mesmo sistema operacional e versões de pacotes
- Mesma versão do Python e dependências
- Mesma versão do Node.js
- Banco de dados similar (PostgreSQL na mesma versão)

### 2. Configuração do Banco de Dados de Staging

#### Criar Banco de Dados Separado
```sql
-- Conectar como superusuário no PostgreSQL
CREATE DATABASE stock_control_staging_db;
CREATE USER stock_control_staging_user WITH PASSWORD 'senha-staging-segura';
ALTER ROLE stock_control_staging_user SET client_encoding TO 'utf8';
ALTER ROLE stock_control_staging_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE stock_control_staging_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE stock_control_staging_db TO stock_control_staging_user;
```

## Processo de Deploy para Staging

### 1. Script de Deploy Automatizado

Criar arquivo `deploy_staging.sh`:

```bash
#!/bin/bash
# Script de Deploy para Ambiente de Staging
# Autor: Stock Control Lab Team
# Data: 24/09/2025

set -e  # Sair se algum comando falhar

echo "🚀 Iniciando deploy para ambiente de staging..."

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ Erro: Estrutura de projeto não encontrada."
    exit 1
fi

# Atualizar código da branch de staging
echo "🔄 Atualizando código da branch staging..."
git checkout staging
git pull origin staging

# Atualizar dependências backend
echo "📦 Atualizando dependências do backend..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Atualizar dependências frontend
echo "📦 Atualizando dependências do frontend..."
npm install

# Executar build do frontend
echo "🔨 Executando build do frontend..."
npm run build

# Coletar arquivos estáticos
echo "🧹 Coletando arquivos estáticos..."
cd backend
python manage.py collectstatic --settings=config.settings.staging --noinput
cd ..

# Rodar migrações (se houver)
echo "🔄 Executando migrações (se houver)..."
cd backend
python manage.py migrate --settings=config.settings.staging
cd ..

# Executar testes (opcional mas recomendado)
echo "🧪 Executando testes..."
cd backend
python -m pytest --settings=config.settings.staging -xvs
cd ..

echo "✅ Deploy para staging concluído com sucesso!"
echo "   Acesse https://staging.stock-control-lab.com para testar"
```

Tornar executável:
```bash
chmod +x deploy_staging.sh
```

### 2. Configuração de Staging no Django

Criar arquivo `backend/config/settings/staging.py`:

```python
from .base import *
import os

# Segurança para staging
DEBUG = False
ALLOWED_HOSTS = ['staging.stock-control-lab.com', 'staging.stock-control-lab.com.br']

# Banco de dados de staging
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('STAGING_DB_NAME', 'stock_control_staging_db'),
        'USER': os.environ.get('STAGING_DB_USER', 'stock_control_staging_user'),
        'PASSWORD': os.environ.get('STAGING_DB_PASSWORD'),
        'HOST': os.environ.get('STAGING_DB_HOST', 'localhost'),
        'PORT': os.environ.get('STAGING_DB_PORT', '5432'),
    }
}

# Cache (opcional para staging)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Email de staging (não enviar emails reais)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/stock-control-staging.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Testes de Funcionalidade em Staging

### 1. Testes Automatizados

Executar suíte completa de testes no ambiente de staging:

```bash
# Testes backend
cd backend
python -m pytest --settings=config.settings.staging

# Testes frontend (se configurados)
cd ../
npm run test
```

### 2. Testes Manuais de Casos de Uso

#### Fluxo Básico de Uso
1. Cadastro de usuário
2. Login no sistema
3. Cadastro de um reagente
4. Criação de lote de estoque
5. Registro de movimentação
6. Visualização do dashboard
7. Geração de relatório

#### Fluxo de Requisição
1. Criação de requisição
2. Aprovação/rejeição por administrador
3. Atualização de estoque após aprovação

#### Validações Importantes
1. Validações de quantidade (estoque não pode ser negativo)
2. Controle de validade
3. Permissões de acesso
4. Integridade dos dados

### 3. Testes de Performance

Executar testes com JMeter ou similar:
- Carga de usuários simulados
- Tempo de resposta das APIs
- Uso de recursos do servidor

## Validação da Integração

### 1. Verificar Comunicação API
```bash
# Verificar endpoints essenciais
curl -I https://staging.stock-control-lab.com/api/v1/reagents/
curl -I https://staging.stock-control-lab.com/api/v1/stock-lots/
curl -I https://staging.stock-control-lab.com/api/v1/dashboard/summary/
```

### 2. Verificar Frontend
- Carregamento da aplicação
- Roteamento entre páginas
- Chamadas à API funcionando
- Exibição de dados correta

### 3. Verificar Arquivos Estáticos
- CSS carregando corretamente
- Imagens e fontes acessíveis
- JavaScript funcionando

## Documentação dos Testes

### 1. Checklist de Validação

- [ ] Backend acessível e respondendo
- [ ] Frontend carregando corretamente
- [ ] Autenticação funcionando
- [ ] CRUD de reagentes completo
- [ ] Controle de estoque funcional
- [ ] Relatórios gerando corretamente
- [ ] Dashboard exibindo informações corretamente
- [ ] Requisições e aprovações funcionando
- [ ] Validações de negócio aplicadas
- [ ] Segurança adequada aplicada
- [ ] Performance aceitável (> 80 no Lighthouse)
- [ ] Nenhuma falha crítica detectada

### 2. Registros de Testes

Documentar resultados dos testes em `staging_test_results_YYYYMMDD.md`:

```markdown
# Resultados dos Testes em Staging - Data

## Informações Gerais
- Data do teste: 24/09/2025
- Versão: v1.2.3
- Testador: [Nome do testador]

## Resultados dos Testes

### Funcionalidades Testadas
- [x] Login/Sessão
- [x] Cadastro de Reagentes
- [x] Controle de Estoque
- [x] Dashboard
- [x] Relatórios
- [ ] Requisições (com problemas - ver seção de issues)

### Issues Encontradas
1. Issue: [descrição]
   - Severidade: [alta/média/baixa]
   - Status: [aberto/resolvido/testado]
   - Solução: [ação tomada]

### Performance
- Tempo médio de resposta: X ms
- Tempo de carregamento da página inicial: X ms
- Uso de memória: X%
- CPU: X%

### Conclusão
[Resumo do status dos testes]
```

## Rollback Procedure (se necessário)

Caso problemas críticos sejam encontrados:

```bash
# Script de rollback
#!/bin/bash
echo "⚠️  Iniciando procedimento de rollback..."

# Reverter para versão anterior
git checkout v1.2.2  # versão anterior estável

# Atualizar deploy
./deploy_staging.sh

echo "✅ Rollback concluído"
```

## Aprovação para Produção

Após testes bem sucedidos em staging:

1. Documentar resultados dos testes
2. Obter aprovação da equipe técnica
3. Agendar janela de deploy para produção
4. Preparar script de deploy para produção (semelhante ao de staging)
5. Fazer backup da produção antes do deploy

## Monitoramento Pós-Deploy

### 1. Métricas a Serem Monitoradas
- Tempo de resposta das APIs
- Uso de recursos do servidor
- Erros de aplicação
- Uso por parte dos usuários

### 2. Ferramentas de Monitoramento
- Logs do Django
- Métricas do Nginx
- Monitoramento de banco de dados
- (Opcional) Ferramentas como New Relic, DataDog, etc.

## Considerações Finais

O ambiente de staging é crítico para garantir a qualidade e estabilidade do sistema antes do deploy em produção. Todos os testes devem ser realizados com atenção antes de aprovar qualquer versão para produção.

A aprovação para deploy em produção deve ser feita somente após:
- 100% dos testes automatizados passando
- Nenhuma falha crítica identificada nos testes manuais
- Aprovação formal da equipe de desenvolvimento e QA
- Confirmação de que a rollback procedure está pronta