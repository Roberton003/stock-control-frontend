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