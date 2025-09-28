#!/bin/bash

# Simple Django Project Installer (v2)

set -e

# --- Configuração de Cores e Funções de Log ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_info() { echo -e "${CYAN}[INFO]${NC} $1"; }

# --- Lógica de Criação do Projeto ---
create_django_project() {
    local project_name=$1
    local use_postgres=${2:-false}
    local is_api=${3:-false}
    
    print_info "Criando projeto: $project_name (PostgreSQL: $use_postgres, API: $is_api)"
    
    mkdir -p "$project_name"
    cd "$project_name"
    
    print_step "Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    
    print_step "Instalando dependências..."
    pip install --upgrade pip
    local base_packages="django django-extensions ipython python-decouple pillow django-cors-headers"
    local dev_packages="pytest pytest-cov flake8 black isort pip-tools"
    
    [ "$use_postgres" = true ] && base_packages="$base_packages psycopg2-binary"
    [ "$is_api" = true ] && base_packages="$base_packages djangorestframework django-filter"
    
    pip install $base_packages $dev_packages

    print_step "Configurando arquivos de dependências (pip-tools)..."
    echo "$base_packages" | tr ' ' '\n' > requirements.in
    echo "-r requirements.in" > requirements-dev.in
    echo "$dev_packages" | tr ' ' '\n' >> requirements-dev.in

    pip-compile requirements.in
    pip-compile requirements-dev.in
    
    print_step "Criando projeto Django..."
    django-admin startproject config .
    
    print_step "Criando estrutura de diretórios..."
    mkdir -p {static/{css,js,img},media,templates,logs,backups}
    
    print_step "Gerando .gitignore..."
    cat > .gitignore << 'EOF'
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
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtualenv
virtualenv/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Outros
/backups/
/logs/
*.txt
EOF
    
    print_step "Configurando ambiente inicial..."
    cat > .env << EOL
DEBUG=True
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=localhost,127.0.0.1
EOL
    
    print_step "Inicializando repositório Git..."
    git init
    git add .
    git commit -m "Initial project structure created by Toolkit v2"
    
    print_success "Projeto $project_name criado com sucesso!"
    echo
    print_info "Próximos passos:"
    print_info "1. cd $project_name"
    print_info "2. source venv/bin/activate"
    print_info "3. Consulte o dev_guide.md para os comandos de desenvolvimento."
}

# --- Roteador de Comandos ---

# ... (a lógica interativa e de flags pode ser adicionada aqui se necessário)

main() {
    if [ -z "$1" ]; then
        print_error "O nome do projeto é obrigatório."
        echo "Uso: $0 <nome_do_projeto>"
        exit 1
    fi
    create_django_project "$1"
}

main "$@"
