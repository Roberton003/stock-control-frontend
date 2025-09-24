# Configuração de Ambiente de Produção - Stock Control Lab

## Visão Geral

Este documento descreve os passos necessários para configurar o ambiente de produção do Stock Control Lab sem o uso de Docker. O sistema é composto por um backend Django e um frontend Vue.js integrado.

## Requisitos do Servidor

### Sistema Operacional
- Ubuntu 20.04 LTS ou superior (ou sistema equivalente)
- Acesso root ou sudo para instalação de pacotes

### Recursos Mínimos
- Memória RAM: 2GB (4GB recomendado)
- Armazenamento: 5GB disponíveis
- CPU: 2 cores (2.0 GHz ou superior)

## Instalação de Dependências do Sistema

### 1. Atualização do Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalação de Pacotes Básicos
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y nginx supervisor postgresql postgresql-contrib
sudo apt install -y git curl wget
```

### 3. Instalação do Node.js e npm
```bash
# Adicionando o repositório NodeSource
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

## Preparação do Ambiente Backend (Django)

### 1. Criação de Usuário para Aplicação
```bash
sudo adduser --system --group --home /opt/stock-control stock-control
```

### 2. Cópia do Código Fonte
```bash
sudo mkdir -p /opt/stock-control/app
sudo chown stock-control:stock-control /opt/stock-control/app
sudo -u stock-control -H bash -c "git clone https://github.com/seu-usuario/stock-control-lab.git /opt/stock-control/app/"
```

### 3. Configuração do Ambiente Virtual
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && python3 -m venv venv"
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && pip install --upgrade pip"
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && pip install -r requirements.txt"
```

### 4. Configuração do Banco de Dados PostgreSQL
```bash
# Login no PostgreSQL
sudo -u postgres psql

# Executar estes comandos no prompt do PostgreSQL:
CREATE DATABASE stock_control_db;
CREATE USER stock_control_user WITH PASSWORD 'senha-segura-aqui';
ALTER ROLE stock_control_user SET client_encoding TO 'utf8';
ALTER ROLE stock_control_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE stock_control_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE stock_control_db TO stock_control_user;
\q
```

### 5. Configuração do Django para Produção

Criar arquivo de configuração `/opt/stock-control/app/stock-control-lab/backend/.env`:
```bash
SECRET_KEY=sua-chave-privada-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgresql://stock_control_user:senha-segura-aqui@localhost/stock_control_db
DJANGO_SETTINGS_MODULE=config.settings.production
```

### 6. Execução de Migrações
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py migrate --settings=config.settings.production"
```

### 7. Criação de Superusuário (Opcional)
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py createsuperuser --settings=config.settings.production"
```

## Configuração do Frontend para Produção

### 1. Build do Frontend
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab && npm install"
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab && npm run build"
```

### 2. Coleta de Arquivos Estáticos do Django
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py collectstatic --settings=config.settings.production --noinput"
```

## Configuração do Servidor Web (Nginx)

### 1. Arquivo de Configuração do Nginx

Criar arquivo `/etc/nginx/sites-available/stock-control`:
```nginx
upstream stock_control_app_server {
    server unix:/opt/stock-control/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Timeout para uploads maiores
    client_max_body_size 100M;

    # Gunicorn proxy
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://stock_control_app_server;
    }

    # Servir arquivos estáticos via Nginx
    location /static/ {
        alias /opt/stock-control/app/stock-control-lab/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Servir arquivos de mídia
    location /media/ {
        alias /opt/stock-control/app/stock-control-lab/backend/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
}
```

### 2. Ativar Site e Reiniciar Nginx
```bash
sudo ln -s /etc/nginx/sites-available/stock-control /etc/nginx/sites-enabled/
sudo nginx -t  # Verificar configuração
sudo systemctl reload nginx
```

## Configuração do Processo Django (Gunicorn + Supervisor)

### 1. Instalar Gunicorn
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && pip install gunicorn"
```

### 2. Criar diretório para socket Unix
```bash
sudo mkdir -p /opt/stock-control/run
sudo chown stock-control:stock-control /opt/stock-control/run
```

### 3. Criar arquivo de configuração do Supervisor `/etc/supervisor/conf.d/stock-control.conf`:
```ini
[program:stock-control]
command=/opt/stock-control/app/stock-control-lab/backend/venv/bin/gunicorn config.wsgi:application --bind unix:/opt/stock-control/run/gunicorn.sock --workers 3 --timeout 120 --max-requests 500 --max-requests-jitter 50
directory=/opt/stock-control/app/stock-control-lab/backend
user=stock-control
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/stock-control.log
environment=DJANGO_SETTINGS_MODULE="config.settings.production"

[group:stock-control]
programs:stock-control
```

### 4. Reiniciar Supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start stock-control:*
```

## Configurações de Segurança Adicionais

### 1. SSL/HTTPS com Let's Encrypt (recomendado)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

### 2. Configuração de Firewall
```bash
sudo ufw enable
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
```

## Testes de Verificação

### 1. Verificar Status dos Serviços
```bash
sudo systemctl status nginx
sudo supervisorctl status stock-control
```

### 2. Testar Conexão com Banco de Dados
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py dbshell"
```

### 3. Executar Testes (Opcional)
```bash
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py test --settings=config.settings.production"
```

## Manutenção e Monitoramento

### 1. Backup de Dados
```bash
# Script para backup do banco de dados
pg_dump -h localhost -U stock_control_user -d stock_control_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Logs Importantes
- Nginx: `/var/log/nginx/`
- Gunicorn: `/var/log/stock-control.log`
- Django: Configurável nos settings

## Atualizações

### 1. Atualizar Aplicação
```bash
# Fazer backup primeiro!
sudo systemctl stop stock-control

# Atualizar código
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab && git pull origin main"

# Atualizar dependências backend
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && pip install -r requirements.txt"

# Atualizar dependências frontend
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab && npm install"

# Fazer build do frontend
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab && npm run build"

# Coletar arquivos estáticos
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py collectstatic --settings=config.settings.production --noinput"

# Rodar migrações se necessário
sudo -u stock-control -H bash -c "cd /opt/stock-control/app/stock-control-lab/backend && source venv/bin/activate && python manage.py migrate --settings=config.settings.production"

# Reiniciar serviço
sudo supervisorctl start stock-control
```

## Solução de Problemas

### 1. Verificar Logs
```bash
sudo tail -f /var/log/stock-control.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Verificar Conexões
```bash
sudo netstat -tlnp | grep :80
ls -la /opt/stock-control/run/
```

### 3. Testes de Conexão
```bash
# Testar se o socket do Gunicorn responde
ls -la /opt/stock-control/run/gunicorn.sock
```

Esta configuração prepara o Stock Control Lab para execução em ambiente de produção com segurança, performance e escalabilidade adequadas para um sistema de controle de estoque para laboratórios químicos.