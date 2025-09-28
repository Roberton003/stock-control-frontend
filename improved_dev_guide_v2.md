# Guia de Desenvolvimento Django v2.0 - Manual de Operações para Agente IA

Este documento serve como um manual completo e **seguro** de operações para o agente de IA, contendo comandos exatos, workflows e procedimentos para desenvolvimento e manutenção de projetos Django.

> **Nota para Agentes de IA:** Como os comandos são executados de forma não-interativa, não é possível "ativar" um ambiente virtual com `source`. Portanto, todos os comandos que dependem do ambiente virtual (como `python`, `pip`, `pytest`) devem ser prefixados com o caminho completo para o executável dentro do `venv`. Exemplo: `projeto_teste_v2/venv/bin/python manage.py migrate`.

## 📋 Índice

1. [Pré-requisitos e Ambiente](#pré-requisitos-e-ambiente)
2. [Workflows Principais](#workflows-principais)
3. [Segurança e Validações](#segurança-e-validações)
4. [Desenvolvimento](#desenvolvimento)
5. [Qualidade e Testes](#qualidade-e-testes)
6. [Administração](#administração)
7. [Monitoramento e Rollback](#monitoramento-e-rollback)
8. [Troubleshooting](#troubleshooting)
9. [Referências Rápidas](#referências-rápidas)

---

## 🔒 Segurança e Validações

### Validação de Configurações

#### Validação Segura de ALLOWED_HOSTS
```python
# settings.py - Configuração SEGURA
import os
from decouple import config

def validate_allowed_hosts(hosts_string):
    """Valida e limpa ALLOWED_HOSTS de forma segura"""
    if not hosts_string:
        return ['127.0.0.1', 'localhost']
    
    hosts = [host.strip() for host in hosts_string.split(',') if host.strip()]
    
    # Remover hosts vazios ou inválidos
    valid_hosts = []
    for host in hosts:
        # Validação básica de formato de host
        if host and (
            host in ['127.0.0.1', 'localhost'] or  # Locais permitidos
            host.replace('.', '').replace('-', '').replace('_', '').isalnum() or  # Domínios básicos
            host.startswith('.')  # Subdomínios (.example.com)
        ):
            valid_hosts.append(host)
    
    return valid_hosts if valid_hosts else ['127.0.0.1', 'localhost']

# Aplicar validação
ALLOWED_HOSTS = validate_allowed_hosts(
    config('ALLOWED_HOSTS', default='127.0.0.1,localhost')
)
```

#### Validação de SECRET_KEY
```python
# settings.py - Geração e validação segura de SECRET_KEY
import secrets
from django.core.management.utils import get_random_secret_key

def get_validated_secret_key():
    """Gera ou valida SECRET_KEY"""
    secret_key = config('SECRET_KEY', default='')
    
    # Se não houver secret key ou for muito simples, gerar uma nova
    if not secret_key or len(secret_key) < 50:
        new_key = get_random_secret_key()
        print(f"⚠️ ATENÇÃO: SECRET_KEY gerada automaticamente: {new_key}")
        print("   Adicione esta chave ao arquivo .env para manter consistência")
        return new_key
    
    return secret_key

SECRET_KEY = get_validated_secret_key()
```

#### Configuração de Banco Segura
```python
# settings.py - Database com failsafe
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        } if config('DB_ENGINE', default='').endswith('mysql') else {},
    }
}

# Validação de configuração de produção
if not DEBUG and DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    import warnings
    warnings.warn(
        "SQLite não é recomendado para produção. Configure um banco robusto.",
        category=UserWarning
    )
```

### Arquivo .env Seguro

**.env.example (template seguro):**
```env
# CONFIGURAÇÕES ESSENCIAIS
SECRET_KEY=sua-secret-key-aqui-deve-ter-50-caracteres-ou-mais
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,seu-dominio.com

# BANCO DE DADOS
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nome_do_banco
DB_USER=usuario_banco
DB_PASSWORD=senha_banco
DB_HOST=localhost
DB_PORT=5432

# EMAIL (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-app-password

# REDIS (opcional)
REDIS_URL=redis://localhost:6379/1

# LOGGING
LOG_LEVEL=INFO
```

### Script de Validação de Segurança

**scripts/security_check.py:**
```python
#!/usr/bin/env python
"""
Script para validar configurações de segurança do Django
Uso: python scripts/security_check.py
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from io import StringIO

class SecurityValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def check_secret_key(self):
        """Validar SECRET_KEY"""
        if not settings.SECRET_KEY:
            self.errors.append("SECRET_KEY não configurada")
        elif len(settings.SECRET_KEY) < 50:
            self.warnings.append("SECRET_KEY muito curta (recomendado: 50+ caracteres)")
        elif settings.SECRET_KEY == 'django-insecure-default-key':
            self.errors.append("SECRET_KEY usando valor padrão inseguro")
    
    def check_debug_settings(self):
        """Validar configurações de DEBUG"""
        if settings.DEBUG and 'production' in os.environ.get('ENVIRONMENT', '').lower():
            self.errors.append("DEBUG=True em ambiente de produção")
    
    def check_allowed_hosts(self):
        """Validar ALLOWED_HOSTS"""
        if not settings.ALLOWED_HOSTS and not settings.DEBUG:
            self.errors.append("ALLOWED_HOSTS vazio em produção")
        elif '*' in settings.ALLOWED_HOSTS and not settings.DEBUG:
            self.errors.append("ALLOWED_HOSTS contém '*' em produção")
    
    def check_database_config(self):
        """Validar configuração do banco"""
        db_config = settings.DATABASES['default']
        
        if db_config['ENGINE'] == 'django.db.backends.sqlite3' and not settings.DEBUG:
            self.warnings.append("SQLite não recomendado para produção")
        
        if not db_config.get('PASSWORD') and not settings.DEBUG:
            self.warnings.append("Banco sem senha em produção")
    
    def check_security_middleware(self):
        """Validar middlewares de segurança"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ]
        
        for middleware in required_middleware:
            if middleware not in settings.MIDDLEWARE:
                self.warnings.append(f"Middleware recomendado ausente: {middleware}")
    
    def run_django_checks(self):
        """Executar checks de segurança do Django"""
        try:
            output = StringIO()
            call_command('check', '--deploy', stdout=output, stderr=output)
            
            output_str = output.getvalue()
            if 'ERRORS' in output_str:
                self.errors.append("Django check encontrou erros de deploy")
            if 'WARNINGS' in output_str:
                self.warnings.append("Django check encontrou warnings de deploy")
                
        except Exception as e:
            self.errors.append(f"Erro ao executar Django checks: {e}")
    
    def validate_all(self):
        """Executar todas as validações"""
        print("🔍 Executando validações de segurança...\n")
        
        self.check_secret_key()
        self.check_debug_settings()
        self.check_allowed_hosts()
        self.check_database_config()
        self.check_security_middleware()
        self.run_django_checks()
        
        # Exibir resultados
        if self.errors:
            print("❌ ERROS CRÍTICOS:")
            for error in self.errors:
                print(f"   • {error}")
            print()
        
        if self.warnings:
            print("⚠️  AVISOS:")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ Todas as validações passaram!")
        
        return len(self.errors) == 0

if __name__ == '__main__':
    validator = SecurityValidator()
    is_secure = validator.validate_all()
    sys.exit(0 if is_secure else 1)
```

---

## Pré-requisitos e Ambiente

### Verificação do Ambiente
```bash
# Use o caminho completo para o executável do venv
[caminho_projeto]/venv/bin/python --version
[caminho_projeto]/venv/bin/pip --version

# Listar dependências instaladas
[caminho_projeto]/venv/bin/pip list

# Executar validação de segurança
[caminho_projeto]/venv/bin/python scripts/security_check.py
```

### Configuração do Ambiente Virtual
```bash
# Criar ambiente virtual (se ainda não existir)
# Use 'python3' para garantir que a versão 3 do Python seja utilizada.
python3 -m venv [caminho_projeto]/venv
```

---

## Workflows Principais

> **Regra Geral de Execução de Comandos para Agentes:**
> Todos os comandos listados abaixo devem ser executados a partir do **diretório raiz do projeto Django**.
> Para comandos que utilizam o Python ou ferramentas instaladas no ambiente virtual (`pip`, `django-admin`, `manage.py`, `pytest`, `isort`, `black`, `flake8`, `coverage`), utilize o executável completo do `venv`.

### Workflow: Scaffolding Completo e Seguro de Projeto Django

Este workflow inclui validações de segurança em cada etapa.

1. **Criar o Ambiente Virtual:**
   ```bash
   python3 -m venv [caminho_para_o_novo_projeto]/venv
   ```

2. **Instalar Django e ferramentas essenciais:**
   ```bash
   cd [caminho_para_o_novo_projeto]
   venv/bin/pip install --upgrade pip
   venv/bin/pip install django python-decouple pip-tools
   ```

3. **Criar o Projeto Django:**
   ```bash
   cd [caminho_para_o_novo_projeto]
   venv/bin/django-admin startproject [nome_do_projeto] .
   ```

4. **Criar Arquivos de Dependências Seguros:**

   **requirements.in:**
   ```
   # Core
   django>=4.2,<5.0
   python-decouple>=3.6
   
   # Database
   psycopg2-binary>=2.9.5  # PostgreSQL
   
   # Security
   django-cors-headers>=4.0.0
   django-csp>=3.7
   
   # Utils
   pillow>=9.3.0
   django-extensions>=3.2.0
   ```

   **requirements-dev.in:**
   ```
   -r requirements.in
   
   # Testing
   pytest>=7.2.0
   pytest-django>=4.5.2
   pytest-cov>=4.0.0
   coverage>=7.0.0
   
   # Code Quality
   black>=22.10.0
   isort>=5.11.4
   flake8>=6.0.0
   mypy>=0.991
   
   # Development
   django-debug-toolbar>=3.2.4
   pip-tools>=6.12.1
   
   # Security Testing
   bandit>=1.7.4
   safety>=2.3.4
   ```

5. **Compilar e Instalar Dependências:**
   ```bash
   cd [caminho_para_o_novo_projeto]
   venv/bin/pip-compile requirements.in
   venv/bin/pip-compile requirements-dev.in
   venv/bin/pip-sync requirements-dev.txt
   ```

6. **Criar Script de Segurança:**
   ```bash
   mkdir -p scripts
   # Criar o arquivo scripts/security_check.py com o conteúdo fornecido acima
   ```

7. **Configurar settings.py com Segurança:**
   
   **[nome_do_projeto]/settings.py:**
   ```python
   import os
   from pathlib import Path
   from decouple import config
   from django.core.management.utils import get_random_secret_key
   
   BASE_DIR = Path(__file__).resolve().parent.parent
   
   # SECURITY WARNING: keep the secret key used in production secret!
   def get_validated_secret_key():
       secret_key = config('SECRET_KEY', default='')
       if not secret_key or len(secret_key) < 50:
           new_key = get_random_secret_key()
           print(f"⚠️ SECRET_KEY gerada: {new_key}")
           print("   Adicione ao .env: SECRET_KEY={new_key}")
           return new_key
       return secret_key
   
   SECRET_KEY = get_validated_secret_key()
   
   # SECURITY WARNING: don't run with debug turned on in production!
   DEBUG = config('DEBUG', default=True, cast=bool)
   
   # Validação segura de ALLOWED_HOSTS
   def validate_allowed_hosts(hosts_string):
       if not hosts_string:
           return ['127.0.0.1', 'localhost']
       
       hosts = [host.strip() for host in hosts_string.split(',') if host.strip()]
       valid_hosts = []
       
       for host in hosts:
           if host and (
               host in ['127.0.0.1', 'localhost'] or
               host.replace('.', '').replace('-', '').replace('_', '').isalnum() or
               host.startswith('.')
           ):
               valid_hosts.append(host)
       
       return valid_hosts if valid_hosts else ['127.0.0.1', 'localhost']
   
   ALLOWED_HOSTS = validate_allowed_hosts(
       config('ALLOWED_HOSTS', default='127.0.0.1,localhost')
   )
   
   # Application definition
   DJANGO_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   
   THIRD_PARTY_APPS = [
       'corsheaders',
   ]
   
   LOCAL_APPS = [
       # Seus apps aqui
   ]
   
   INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
   
   # Security Middleware (ordem importa!)
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'corsheaders.middleware.CorsMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]
   
   ROOT_URLCONF = '[nome_do_projeto].urls'
   
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [BASE_DIR / 'templates'],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   
   WSGI_APPLICATION = '[nome_do_projeto].wsgi.application'
   
   # Database
   DATABASES = {
       'default': {
           'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
           'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
           'USER': config('DB_USER', default=''),
           'PASSWORD': config('DB_PASSWORD', default=''),
           'HOST': config('DB_HOST', default=''),
           'PORT': config('DB_PORT', default=''),
       }
   }
   
   # Security Settings
   if not DEBUG:
       SECURE_BROWSER_XSS_FILTER = True
       SECURE_CONTENT_TYPE_NOSNIFF = True
       SECURE_HSTS_SECONDS = 31536000
       SECURE_HSTS_INCLUDE_SUBDOMAINS = True
       SECURE_HSTS_PRELOAD = True
       X_FRAME_OPTIONS = 'DENY'
       SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
   
   # Internationalization
   LANGUAGE_CODE = 'pt-br'
   TIME_ZONE = 'America/Sao_Paulo'
   USE_I18N = True
   USE_TZ = True
   
   # Static files
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_DIRS = [BASE_DIR / 'static']
   
   # Media files
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   
   # Default primary key field type
   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
   
   # Logging
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.handlers.RotatingFileHandler',
               'filename': BASE_DIR / 'logs' / 'django.log',
               'maxBytes': 1024*1024*10,  # 10MB
               'backupCount': 5,
               'formatter': 'verbose',
           },
           'console': {
               'level': 'INFO',
               'class': 'logging.StreamHandler',
               'formatter': 'verbose',
           },
       },
       'root': {
           'handlers': ['console', 'file'] if not DEBUG else ['console'],
           'level': config('LOG_LEVEL', default='INFO'),
       },
   }
   
   # Criar diretório de logs se não existir
   os.makedirs(BASE_DIR / 'logs', exist_ok=True)
   ```

8. **Criar Arquivo .env Seguro:**
   ```env
   # .env (não commitar!)
   SECRET_KEY=sua-chave-gerada-de-50-caracteres-pelo-django
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   
   # Database
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   
   # Logging
   LOG_LEVEL=DEBUG
   ```

9. **Criar .gitignore Seguro:**
   ```gitignore
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   share/python-wheels/
   *.egg-info/
   .installed.cfg
   *.egg
   MANIFEST
   
   # Django
   *.log
   local_settings.py
   db.sqlite3
   db.sqlite3-journal
   media/
   staticfiles/
   
   # Environment
   .env
   .venv
   venv/
   ENV/
   env/
   
   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   *~
   
   # Security
   *.pem
   *.key
   ```

10. **Executar Migrações e Validação:**
    ```bash
    cd [caminho_para_o_novo_projeto]
    
    # Criar diretórios necessários
    mkdir -p logs static media templates
    
    # Executar migrações
    venv/bin/python manage.py makemigrations
    venv/bin/python manage.py migrate
    
    # Validar configurações de segurança
    venv/bin/python scripts/security_check.py
    
    # Executar checks do Django
    venv/bin/python manage.py check --deploy
    ```

---

## Monitoramento e Rollback

### Sistema de Backup Automático

**scripts/backup.py:**
```python
#!/usr/bin/env python
"""
Sistema de backup automático para projetos Django
"""

import os
import sys
import shutil
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class BackupManager:
    def __init__(self):
        self.backup_dir = BASE_DIR / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self, description=""):
        """Criar backup completo do projeto"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        if description:
            backup_name += f"_{description}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir()
        
        # Backup do código
        code_backup = backup_path / 'code'
        shutil.copytree(BASE_DIR, code_backup, ignore=shutil.ignore_patterns(
            'venv', '__pycache__', '*.pyc', '.git', 'backups', 'logs', 'media'
        ))
        
        # Backup do banco de dados
        self.backup_database(backup_path)
        
        # Backup de arquivos de mídia
        media_dir = BASE_DIR / 'media'
        if media_dir.exists():
            shutil.copytree(media_dir, backup_path / 'media')
        
        print(f"✅ Backup criado: {backup_path}")
        return backup_path
    
    def backup_database(self, backup_path):
        """Backup específico do banco de dados"""
        try:
            os.system(f"cd {BASE_DIR} && venv/bin/python manage.py dumpdata > {backup_path}/database.json")
        except Exception as e:
            print(f"⚠️ Erro no backup do banco: {e}")
    
    def list_backups(self):
        """Listar backups disponíveis"""
        backups = sorted([d for d in self.backup_dir.iterdir() if d.is_dir()], reverse=True)
        
        print("📦 Backups disponíveis:")
        for i, backup in enumerate(backups):
            size = self.get_dir_size(backup)
            print(f"   {i+1}. {backup.name} ({size:.1f}MB)")
        
        return backups
    
    def restore_backup(self, backup_name):
        """Restaurar backup específico"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print(f"❌ Backup não encontrado: {backup_name}")
            return False
        
        # Confirmar restauração
        print(f"⚠️ Isso irá sobrescrever o projeto atual com {backup_name}")
        confirm = input("Confirmar? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("Restauração cancelada.")
            return False
        
        # Restaurar código
        code_backup = backup_path / 'code'
        if code_backup.exists():
            # Backup atual antes de restaurar
            self.create_backup("pre_restore")
            
            # Restaurar arquivos (exceto venv)
            for item in code_backup.iterdir():
                if item.name == 'venv':
                    continue
                
                target = BASE_DIR / item.name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
        
        # Restaurar banco
        db_backup = backup_path / 'database.json'
        if db_backup.exists():
            os.system(f"cd {BASE_DIR} && venv/bin/python manage.py flush --noinput")
            os.system(f"cd {BASE_DIR} && venv/bin/python manage.py loaddata {db_backup}")
        
        # Restaurar mídia
        media_backup = backup_path / 'media'
        media_dir = BASE_DIR / 'media'
        if media_backup.exists():
            if media_dir.exists():
                shutil.rmtree(media_dir)
            shutil.copytree(media_backup, media_dir)
        
        print(f"✅ Backup restaurado: {backup_name}")
        return True
    
    def cleanup_old_backups(self, keep_count=10):
        """Limpar backups antigos mantendo apenas os mais recentes"""
        backups = sorted([d for d in self.backup_dir.iterdir() if d.is_dir()], reverse=True)
        
        for backup in backups[keep_count:]:
            shutil.rmtree(backup)
            print(f"🗑️ Backup removido: {backup.name}")
    
    @staticmethod
    def get_dir_size(path):
        """Calcular tamanho do diretório em MB"""
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total += os.path.getsize(filepath)
        return total / (1024 * 1024)

if __name__ == '__main__':
    manager = BackupManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create':
            description = sys.argv[2] if len(sys.argv) > 2 else ""
            manager.create_backup(description)
        elif command == 'list':
            manager.list_backups()
        elif command == 'restore':
            if len(sys.argv) > 2:
                manager.restore_backup(sys.argv[2])
            else:
                print("Uso: python scripts/backup.py restore <backup_name>")
        elif command == 'cleanup':
            manager.cleanup_old_backups()
        else:
            print("Comandos: create, list, restore, cleanup")
    else:
        print("Uso: python scripts/backup.py <command>")
```

### Comandos de Backup e Rollback

```bash
# Criar backup antes de mudanças importantes
cd [caminho_projeto]
venv/bin/python scripts/backup.py create "before_feature_x"

# Listar backups disponíveis
venv/bin/python scripts/backup.py list

# Restaurar backup específico
venv/bin/python scripts/backup.py restore backup_20241217_143022_before_feature_x

# Limpar backups antigos (manter apenas 10 mais recentes)
venv/bin/python scripts/backup.py cleanup
```

---

## Desenvolvimento

### Comandos de Desenvolvimento Seguros

```bash
# Iniciar servidor de desenvolvimento com validação
cd [caminho_projeto]
venv/bin/python scripts/security_check.py && venv/bin/python manage.py runserver

# Executar testes com cobertura
venv/bin/python -m pytest --cov=. --cov-report=html --cov-report=term

# Executar verificações de código
venv/bin/python -m black . --check
venv/bin/python -m isort . --check-only
venv/bin/python -m flake8 .

# Verificação de segurança
venv/bin/python -m bandit -r . -x tests/
venv/bin/python -m safety check

# Aplicar formatação automática
venv/bin/python -m black .
venv/bin/python -m isort .
```

### Makefile Integrado com Segurança

**Makefile:**
```makefile
.PHONY: help install dev test security backup clean

VENV_PATH = venv/bin

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .* $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $1, $2}'

install: ## Instalar dependências
	$(VENV_PATH)/pip install --upgrade pip
	$(VENV_PATH)/pip-sync requirements-dev.txt

security: ## Executar verificações de segurança
	$(VENV_PATH)/python scripts/security_check.py
	$(VENV_PATH)/python manage.py check --deploy
	$(VENV_PATH)/python -m bandit -r . -x tests/ --quiet
	$(VENV_PATH)/python -m safety check --short-report

test: ## Executar testes com cobertura
	$(VENV_PATH)/python -m pytest --cov=. --cov-report=html --cov-report=term-missing

quality: ## Verificar qualidade do código
	$(VENV_PATH)/python -m black . --check
	$(VENV_PATH)/python -m isort . --check-only
	$(VENV_PATH)/python -m flake8 .

format: ## Formatar código automaticamente
	$(VENV_PATH)/python -m black .
	$(VENV_PATH)/python -m isort .

backup: ## Criar backup do projeto
	$(VENV_PATH)/python scripts/backup.py create manual_backup

dev: security ## Iniciar desenvolvimento (com validação)
	$(VENV_PATH)/python manage.py migrate
	$(VENV_PATH)/python manage.py runserver

migrate: ## Aplicar migrações
	$(VENV_PATH)/python manage.py makemigrations
	$(VENV_PATH)/python manage.py migrate

shell: ## Abrir shell Django
	$(VENV_PATH)/python manage.py shell_plus

clean: ## Limpar arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

all: security quality test ## Executar todas as verificações
	@echo "✅ Todas as verificações passaram!"
```

---

## Referências Rápidas

### Comandos Essenciais com Validação

```bash
# Setup inicial seguro
make install
make security

# Desenvolvimento diário
make dev          # Inicia com validações
make test         # Testes com cobertura
make quality      # Verificação de código

# Antes de commit
make all          # Todas as verificações

# Backup e recuperação
make backup                           # Backup manual
venv/bin/python scripts/backup.py list    # Listar backups
venv/bin/python scripts/backup.py restore <nome>  # Restaurar
```

### Checklist de Segurança

- [ ] SECRET_KEY configurada e válida (50+ caracteres)
- [ ] DEBUG=False em produção
- [ ] ALLOWED_HOSTS corretamente configurado
- [ ] Middlewares de segurança ativados
- [ ] Banco de dados com senha em produção
- [ ] Logs configurados
- [ ] Backups automatizados
- [ ] Verificações de código passando
- [ ] Testes com boa cobertura

### Troubleshooting Comum

**Erro: SECRET_KEY não configurada**
```bash
# Gerar nova chave
venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Adicionar ao .env
```

**Erro: Banco de dados não encontrado**
```bash
# Recriar banco
venv/bin/python manage.py migrate
```

**Erro: Permissões negadas**
```bash
# Verificar propriedade dos arquivos
sudo chown -R $USER:$USER .
```

Este guia fornece uma base sólida e segura para desenvolvimento Django com validações automatizadas e mecanismos de recuperação.