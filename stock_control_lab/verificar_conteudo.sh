#!/bin/bash
# Script para verificar conteúdo das páginas principais

echo "==================================================="
echo "VERIFICANDO CONTEÚDO DAS PÁGINAS PRINCIPAIS"
echo "==================================================="

# URLs para verificar
declare -A PAGES=(
    ["/dashboard/"]="Dashboard"
    ["/produtos/list/"]="Lista de Produtos"
    ["/requisitions/list/"]="Lista de Requisições"
    ["/stock-lots/create/"]="Criação de Lotes"
    ["/movimentacoes/withdraw/"]="Retirada de Estoque"
)

for url in "${!PAGES[@]}"; do
    page_name="${PAGES[$url]}"
    full_url="http://localhost:8000${url}"
    
    echo "---------------------------------------------------"
    echo "Verificando: $page_name ($full_url)"
    
    # Baixar conteúdo da página
    CONTENT=$(curl -s --max-time 10 "$full_url" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        # Verificar tamanho do conteúdo
        CONTENT_SIZE=${#CONTENT}
        
        if [ $CONTENT_SIZE -gt 100 ]; then
            echo "  ✅ Página carregada ($CONTENT_SIZE caracteres)"
            
            # Verificar se contém palavras-chave esperadas
            if [[ "$CONTENT" == *"<!DOCTYPE"* ]] || [[ "$CONTENT" == *"<html"* ]]; then
                echo "  📄 Contém estrutura HTML válida"
            else
                echo "  ⚠️  Estrutura HTML não encontrada"
            fi
            
            # Verificar título da página (se existir)
            if [[ "$CONTENT" == *"<title>"* ]]; then
                TITLE=$(echo "$CONTENT" | grep -oP '<title>\K[^<]*')
                if [ -n "$TITLE" ]; then
                    echo "  🏷️  Título: $TITLE"
                fi
            fi
        else
            echo "  ⚠️  Conteúdo muito pequeno ($CONTENT_SIZE caracteres)"
        fi
    else
        echo "  ❌ Erro ao carregar a página"
    fi
done

echo "---------------------------------------------------"
echo "Verificação de conteúdo concluída!"
echo "==================================================="