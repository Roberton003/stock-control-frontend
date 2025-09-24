#!/bin/bash
# Script de validação do pipeline CI/CD

set -e  # Sair se algum comando falhar

echo "🚀 Iniciando validação do pipeline CI/CD..."

# Verificar ambiente
echo "🔍 Verificando ambiente..."

# Verificar se está no diretório correto
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ Erro: Estrutura de projeto não encontrada."
    exit 1
fi

echo "✅ Estrutura de projeto verificada"

# Testar backend
echo "🧪 Testando backend..."
cd backend

# Verificar se o ambiente virtual está ativo
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Aviso: Ambiente virtual do Python não está ativo, criando temporariamente..."
    python -m venv venv_temp_ci
    source venv_temp_ci/bin/activate
    pip install -r requirements.txt
    deactivate
    source venv_temp_ci/bin/activate
else
    pip install -r requirements.txt
fi

# Rodar testes do backend
echo "🔍 Rodando testes do backend..."
python -m pytest --tb=short

# Validar configurações do Django
echo "🔍 Validando configurações do Django..."
python manage.py check

cd ..

# Testar frontend
echo "🧪 Testando frontend..."
npm install
npm run build
npm test -- --passWithNoTests  # Passar mesmo sem testes

# Verificar se build foi criado
if [ -d "dist" ]; then
    echo "✅ Build do frontend criado com sucesso"
else
    echo "❌ Erro: Build do frontend não foi criado"
    exit 1
fi

# Testar configuração do Docker
echo "🐳 Testando configuração do Docker..."
if command -v docker &> /dev/null; then
    docker build -f backend/Dockerfile . --target backend
    docker build -f Dockerfile . --target frontend
    echo "✅ Configuração do Docker verificada"
else
    echo "⚠️  Docker não encontrado, pulando validação do Docker"
fi

# Testar configuração do docker-compose
echo "🐳 Testando configuração do docker-compose..."
if command -v docker-compose &> /dev/null; then
    docker-compose config
    echo "✅ Configuração do docker-compose verificada"
else
    echo "⚠️  Docker Compose não encontrado, pulando validação"
fi

echo "✅ Validação do pipeline completada com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Fazer push para o repositório para acionar o pipeline CI/CD"
echo "   2. Verificar o status do pipeline no GitHub Actions"
echo "   3. Se for para produção, verificar o deployment"