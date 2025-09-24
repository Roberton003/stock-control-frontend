#!/bin/bash
# Script de Build do Frontend para Integração com Django
# Autor: Stock Control Lab Team
# Data: 24/09/2025
#
# Este script gera o build de produção do frontend Vue.js
# e o integra com o backend Django.

set -e  # Sair se algum comando falhar

echo "🚀 Iniciando build do frontend para integração com Django..."

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ]; then
    echo "❌ Erro: package.json não encontrado. Execute este script no diretório raiz do frontend."
    exit 1
fi

# Limpar build anterior
echo "🧹 Limpando build anterior..."
rm -rf dist/

# Executar build do Vite
echo "🔨 Executando build do frontend com Vite..."
npm run build

echo "✅ Build do frontend concluído em dist/"

# Verificar se build foi criado com sucesso
if [ ! -d "dist" ]; then
    echo "❌ Erro: Diretório dist não encontrado após build."
    exit 1
fi

# Copiar o build para o diretório estático do Django
echo "🚚 Copiando arquivos estáticos para o backend Django..."

# Determinar o caminho relativo para o backend
BACKEND_PATH="backend/static/dist"

# Criar diretórios se não existirem
mkdir -p "$BACKEND_PATH"

# Copiar arquivos do build para o backend
cp -r dist/* "$BACKEND_PATH/"

echo "✅ Arquivos estáticos copiados para $BACKEND_PATH"

# Opcional: copiar arquivos para o diretório staticfiles do Django para coleta
STATICFILES_PATH="backend/staticfiles/dist"
mkdir -p "$STATICFILES_PATH"
cp -r dist/* "$STATICFILES_PATH/"

echo "✅ Arquivos copiados para $STATICFILES_PATH também"

# Verificar integridade dos arquivos copiados
if [ -f "$BACKEND_PATH/index.html" ]; then
    echo "✅ Integração com Django concluída com sucesso!"
    echo "   Arquivos disponíveis em: $BACKEND_PATH"
    echo "   Arquivos para coleta Django em: $STATICFILES_PATH"
else
    echo "❌ Erro: Arquivo index.html não encontrado no destino!"
    exit 1
fi

echo ""
echo "📋 Próximos passos:"
echo "   1. Execute 'python manage.py collectstatic' no backend para coletar os arquivos estáticos"
echo "   2. Execute 'python manage.py runserver' para iniciar o servidor Django com o frontend integrado"
echo ""
echo "💡 Dica: O frontend agora está integrado e será servido pelo Django em produção."