#!/bin/bash
# Script para testar os links do sistema de controle de estoque

echo "==================================================="
echo "TESTANDO LINKS DO SISTEMA DE CONTROLE DE ESTOQUE"
echo "==================================================="

URLS=(
    "http://localhost:8000/dashboard/"
    "http://localhost:8000/produtos/list/"
    "http://localhost:8000/requisitions/list/"
    "http://localhost:8000/stock-lots/create/"
    "http://localhost:8000/movimentacoes/withdraw/"
    "http://localhost:8000/admin/"
)

SUCESSO_TOTAL=0
TOTAL_URLS=${#URLS[@]}

for URL in "${URLS[@]}"; do
    echo "---------------------------------------------------"
    echo "Testando: $URL"
    
    # Tentar conectar e obter status HTTP
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        if [ "$RESPONSE" -eq 200 ]; then
            echo "  ✅ Status: $RESPONSE (OK)"
            ((SUCESSO_TOTAL++))
        elif [ "$RESPONSE" -eq 404 ]; then
            echo "  ❌ Status: $RESPONSE (Não encontrado)"
        elif [ "$RESPONSE" -eq 403 ]; then
            echo "  ⚠️  Status: $RESPONSE (Acesso negado - pode exigir autenticação)"
            # Considerar como sucesso parcial pois o endpoint existe
            ((SUCESSO_TOTAL++))
        elif [ "$RESPONSE" -eq 302 ] || [ "$RESPONSE" -eq 301 ]; then
            echo "  ➡️  Status: $RESPONSE (Redirecionamento - endpoint existe)"
            # Considerar como sucesso pois o endpoint existe
            ((SUCESSO_TOTAL++))
        else
            echo "  ⚠️  Status: $RESPONSE (Outro status)"
            # Verificar se é um código de sucesso (2xx)
            if [ "$RESPONSE" -ge 200 ] && [ "$RESPONSE" -lt 300 ]; then
                ((SUCESSO_TOTAL++))
            fi
        fi
    else
        echo "  ❌ Erro: Não foi possível conectar"
    fi
done

echo "---------------------------------------------------"
echo "RESUMO:"
echo "==================================================="
echo "Links testados: $TOTAL_URLS"
echo "Links funcionando: $SUCESSO_TOTAL"
echo "==================================================="

if [ "$SUCESSO_TOTAL" -eq "$TOTAL_URLS" ]; then
    echo "✅ TODOS OS LINKS ESTÃO ATIVOS"
else
    echo "⚠️  ALGUNS LINKS POSSIVELMENTE NÃO ESTÃO FUNCIONANDO"
fi

echo "==================================================="