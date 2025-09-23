#!/bin/bash
# Script para retomar o trabalho no projeto amanhã
# Autor: Roberton003
# Data: 22/09/2025

echo "🚀 Preparando ambiente para retomar o trabalho no Stock Control Lab..."

# Navegar para o diretório do projeto
cd /media/Arquivos/DjangoPython/toolkits/v2/stock_control_lab/stock-control-lab

echo "📁 Diretório atual: $(pwd)"

# Mostrar status do git
echo -e "\n📊 Status do Git:"
git status --short

# Mostrar último commit
echo -e "\n📝 Último commit:"
git log -1 --oneline

# Mostrar conteúdo do checkpoint
echo -e "\n📋 Checkpoint salvo:"
cat CHECKPOINT.md

echo -e "\n✅ Pronto para retomar o trabalho!"
echo "💡 Siga as instruções no CHECKPOINT.md para continuar"

# --- Iniciar Servidores de Desenvolvimento (Automático para o agente, pode ser comentado para uso manual) ---
echo -e "\n--- Iniciando Servidores de Desenvolvimento ---"

echo "Iniciando servidor backend (Django)..."
cd backend && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=config.settings && python manage.py runserver > backend.log 2>&1 &
cd ..
echo "Servidor backend iniciado em segundo plano. Log em backend/backend.log"

echo "Iniciando servidor frontend (Vite)..."
npm run dev > frontend.log 2>&1 &
echo "Servidor frontend iniciado em segundo plano. Log em frontend.log"

echo -e "\nServidores iniciados. Verifique os logs para detalhes."
