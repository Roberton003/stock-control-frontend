#!/bin/bash
# Script para medir o tempo de resposta das páginas do sistema

echo "==================================================="
echo "MEDINDO TEMPO DE RESPOSTA DAS PÁGINAS"
echo "==================================================="

URLS=(
    "http://localhost:8000/dashboard/"
    "http://localhost:8000/produtos/list/"
    "http://localhost:8000/requisitions/list/"
    "http://localhost:8000/stock-lots/create/"
    "http://localhost:8000/movimentacoes/withdraw/"
    "http://localhost:8000/admin/"
)

for URL in "${URLS[@]}"; do
    echo "---------------------------------------------------"
    echo "Testando: $URL"
    
    # Medir tempo de resposta
    START_TIME=$(date +%s.%N)
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL" 2>/dev/null)
    END_TIME=$(date +%s.%N)
    
    # Calcular tempo decorrido em milissegundos
    ELAPSED_TIME=$(echo "($END_TIME - $START_TIME) * 1000" | bc -l)
    FORMATTED_TIME=$(printf "%.0f" "$ELAPSED_TIME")
    
    if [ $? -eq 0 ]; then
        if [ "$RESPONSE" -eq 200 ]; then
            echo "  ✅ Status: $RESPONSE"
            echo "  ⏱️  Tempo de resposta: ${FORMATTED_TIME}ms"
        elif [ "$RESPONSE" -eq 302 ]; then
            echo "  ➡️  Status: $RESPONSE (Redirecionamento)"
            echo "  ⏱️  Tempo de resposta: ${FORMATTED_TIME}ms"
        else
            echo "  ⚠️  Status: $RESPONSE"
            echo "  ⏱️  Tempo de resposta: ${FORMATTED_TIME}ms"
        fi
    else
        echo "  ❌ Erro ao conectar"
    fi
done

echo "---------------------------------------------------"
echo "Teste de performance concluído!"
echo "==================================================="