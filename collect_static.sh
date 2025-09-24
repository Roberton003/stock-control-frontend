#!/bin/bash
# Script para Configurar Coleta de Arquivos Estáticos do Django
# Autor: Stock Control Lab Team
# Data: 24/09/2025
#
# Este script configura e executa a coleta de arquivos estáticos do Django,
# preparando o ambiente para produção.

set -e  # Sair se algum comando falhar

echo "⚙️  Configurando coleta de arquivos estáticos do Django..."

# Verificar se estamos no diretório correto (raiz do projeto)
if [ ! -d "backend" ]; then
    echo "❌ Erro: Diretório backend não encontrado. Execute este script na raiz do projeto."
    exit 1
fi

# Navegar para o diretório backend
cd backend

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Aviso: Ambiente virtual do Python não parece estar ativado."
    echo "   Certifique-se de ativar o ambiente virtual antes de continuar."
    read -p "Deseja continuar mesmo assim? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operação cancelada."
        exit 1
    fi
fi

# Coletar arquivos estáticos
echo "📦 Executando coleta de arquivos estáticos..."
python manage.py collectstatic --noinput

if [ $? -eq 0 ]; then
    echo "✅ Coleta de arquivos estáticos concluída com sucesso!"
else
    echo "❌ Erro durante a coleta de arquivos estáticos."
    exit 1
fi

# Verificar se os arquivos do frontend estão presentes
if [ -d "static/dist" ] || [ -d "staticfiles/dist" ]; then
    echo "✅ Arquivos do frontend encontrados e incluídos na coleta."
else
    echo "⚠️  Aviso: Arquivos do frontend não encontrados."
    echo "   Certifique-se de que o build do frontend foi executado antes deste script."
fi

# Verificar se o arquivo principal do frontend está presente
if [ -f "static/dist/index.html" ] || [ -f "staticfiles/dist/index.html" ]; then
    echo "✅ Arquivo principal do frontend encontrado."
else
    echo "⚠️  Arquivo index.html do frontend não encontrado em local esperado."
fi

echo ""
echo "📋 Coleta de arquivos estáticos concluída!"
echo "   Arquivos coletados em: staticfiles/ (ou conforme configurado em STATIC_ROOT)"
echo ""
echo "💡 Dica: Os arquivos estáticos agora estão prontos para serem servidos pelo Django em produção."
echo "   Configure seu servidor web (Nginx, Apache) para servir estes arquivos para melhor performance."