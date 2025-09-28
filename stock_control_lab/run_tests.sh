#!/bin/bash
# run_tests.sh - Script para executar todos os testes do sistema

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de utilidade
print_header() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}==========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    print_error "Este script deve ser executado na raiz do projeto Django"
    exit 1
fi

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Ambiente virtual não está ativado. Tentando ativar..."
    if [ -d "venv" ]; then
        source venv/bin/activate
        print_success "Ambiente virtual ativado com sucesso"
    else
        print_error "Ambiente virtual não encontrado. Por favor, crie um ambiente virtual primeiro."
        exit 1
    fi
fi

# Verificar dependências
print_header "Verificando dependências"

# Verificar se o Django está instalado
if ! python -c "import django" &> /dev/null; then
    print_error "Django não está instalado"
    exit 1
fi

# Verificar se o Playwright está instalado
if ! python -c "import playwright" &> /dev/null; then
    print_warning "Playwright não está instalado. Instalando..."
    pip install playwright
    print_success "Playwright instalado com sucesso"
fi

# Instalar browsers do Playwright se necessário
print_header "Verificando browsers do Playwright"
playwright install --with-deps chromium firefox webkit &> /dev/null || {
    print_warning "Instalando browsers do Playwright..."
    playwright install --with-deps
    print_success "Browsers do Playwright instalados com sucesso"
}

# Verificar se o pytest está instalado
if ! command -v pytest &> /dev/null; then
    print_warning "Pytest não está instalado. Instalando..."
    pip install pytest pytest-django
    print_success "Pytest instalado com sucesso"
fi

print_success "Todas as dependências verificadas"

# Executar testes unitários e de integração
print_header "Executando testes unitários e de integração"

# Criar diretório para resultados dos testes
mkdir -p test_results/unit test_results/integration

# Executar testes unitários
echo "Executando testes unitários..."
python -m pytest inventory/tests/ -v \
    --junitxml=test_results/unit/results.xml \
    --html=test_results/unit/report.html \
    --self-contained-html \
    --cov=inventory \
    --cov-report=html:test_results/unit/coverage_html \
    --cov-report=xml:test_results/unit/coverage.xml \
    --tb=short

if [ $? -eq 0 ]; then
    print_success "Testes unitários executados com sucesso"
else
    print_error "Alguns testes unitários falharam"
fi

# Executar testes de integração
echo "Executando testes de integração..."
python -m pytest e2e_tests/test_ui.py -v \
    --junitxml=test_results/integration/results.xml \
    --html=test_results/integration/report.html \
    --self-contained-html \
    --tb=short

if [ $? -eq 0 ]; then
    print_success "Testes de integração executados com sucesso"
else
    print_error "Alguns testes de integração falharam"
fi

# Executar testes E2E com Playwright
print_header "Executando testes E2E com Playwright"

# Verificar se o servidor Django está rodando
SERVER_PID=$(pgrep -f "manage.py runserver")
if [ -z "$SERVER_PID" ]; then
    print_warning "Servidor Django não está rodando. Iniciando..."
    python manage.py runserver 8000 > django_server.log 2>&1 &
    DJANGO_PID=$!
    sleep 5  # Aguardar servidor iniciar
    
    # Verificar se o servidor iniciou corretamente
    if curl -s http://localhost:8000 > /dev/null; then
        print_success "Servidor Django iniciado com sucesso (PID: $DJANGO_PID)"
    else
        print_error "Falha ao iniciar servidor Django"
        exit 1
    fi
else
    print_success "Servidor Django já está rodando (PID: $SERVER_PID)"
fi

# Criar diretório para resultados dos testes E2E
mkdir -p test_results/e2e

# Executar testes E2E
echo "Executando testes E2E com Playwright..."
python -m pytest e2e_tests/test_playwright_ui.py -v \
    --junitxml=test_results/e2e/results.xml \
    --html=test_results/e2e/report.html \
    --self-contained-html \
    --tb=short

PLAYWRIGHT_EXIT_CODE=$?

if [ $PLAYWRIGHT_EXIT_CODE -eq 0 ]; then
    print_success "Testes E2E executados com sucesso"
else
    print_error "Alguns testes E2E falharam"
fi

# Parar servidor Django se foi iniciado por este script
if [ ! -z "$DJANGO_PID" ]; then
    print_header "Parando servidor Django"
    kill $DJANGO_PID
    print_success "Servidor Django parado"
fi

# Gerar relatório de cobertura combinado
print_header "Gerando relatórios finais"

# Combinar relatórios de cobertura
if [ -f "test_results/unit/coverage.xml" ] || [ -f "test_results/integration/coverage.xml" ]; then
    print_success "Relatórios de cobertura gerados"
fi

# Exibir resumo dos resultados
print_header "Resumo dos Testes"

echo "Testes Unitários:"
if [ -f "test_results/unit/results.xml" ]; then
    UNIT_TESTS=$( grep -o 'tests="[0-9]*"' test_results/unit/results.xml | cut -d '"' -f 2 )
    UNIT_FAILURES=$( grep -o 'failures="[0-9]*"' test_results/unit/results.xml | cut -d '"' -f 2 )
    UNIT_ERRORS=$( grep -o 'errors="[0-9]*"' test_results/unit/results.xml | cut -d '"' -f 2 )
    echo "  - Total: $UNIT_TESTS testes"
    echo "  - Falhas: $UNIT_FAILURES"
    echo "  - Erros: $UNIT_ERRORS"
else
    echo "  - Nenhum resultado encontrado"
fi

echo ""
echo "Testes de Integração:"
if [ -f "test_results/integration/results.xml" ]; then
    INTEGRATION_TESTS=$( grep -o 'tests="[0-9]*"' test_results/integration/results.xml | cut -d '"' -f 2 )
    INTEGRATION_FAILURES=$( grep -o 'failures="[0-9]*"' test_results/integration/results.xml | cut -d '"' -f 2 )
    INTEGRATION_ERRORS=$( grep -o 'errors="[0-9]*"' test_results/integration/results.xml | cut -d '"' -f 2 )
    echo "  - Total: $INTEGRATION_TESTS testes"
    echo "  - Falhas: $INTEGRATION_FAILURES"
    echo "  - Erros: $INTEGRATION_ERRORS"
else
    echo "  - Nenhum resultado encontrado"
fi

echo ""
echo "Testes E2E:"
if [ -f "test_results/e2e/results.xml" ]; then
    E2E_TESTS=$( grep -o 'tests="[0-9]*"' test_results/e2e/results.xml | cut -d '"' -f 2 )
    E2E_FAILURES=$( grep -o 'failures="[0-9]*"' test_results/e2e/results.xml | cut -d '"' -f 2 )
    E2E_ERRORS=$( grep -o 'errors="[0-9]*"' test_results/e2e/results.xml | cut -d '"' -f 2 )
    echo "  - Total: $E2E_TESTS testes"
    echo "  - Falhas: $E2E_FAILURES"
    echo "  - Erros: $E2E_ERRORS"
else
    echo "  - Nenhum resultado encontrado"
fi

# Verificar se todos os testes passaram
TOTAL_FAILURES=$(( ${UNIT_FAILURES:-0} + ${INTEGRATION_FAILURES:-0} + ${E2E_FAILURES:-0} ))
TOTAL_ERRORS=$(( ${UNIT_ERRORS:-0} + ${INTEGRATION_ERRORS:-0} + ${E2E_ERRORS:-0} ))

echo ""
if [ $TOTAL_FAILURES -eq 0 ] && [ $TOTAL_ERRORS -eq 0 ]; then
    print_success "🎉 Todos os testes passaram com sucesso!"
    exit 0
else
    print_warning "⚠ Alguns testes falharam ou tiveram erros"
    echo "  - Total de falhas: $TOTAL_FAILURES"
    echo "  - Total de erros: $TOTAL_ERRORS"
    exit 1
fi