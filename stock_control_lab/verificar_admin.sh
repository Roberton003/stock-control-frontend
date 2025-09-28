#!/bin/bash
# Script para verificar se o Django Admin está acessível

echo "========================================="
echo "VERIFICANDO ACESSO AO DJANGO ADMIN"
echo "========================================="

# Testar acesso ao admin
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/)
echo "Status do acesso ao admin: $RESPONSE"

if [ "$RESPONSE" -eq 302 ]; then
    echo "✅ Redirecionamento detectado (esperado para login)"
    echo "➡️  O Django Admin está configurado corretamente"
elif [ "$RESPONSE" -eq 200 ]; then
    echo "✅ Página do admin acessível diretamente"
else
    echo "⚠️  Status inesperado: $RESPONSE"
fi

# Verificar se conseguimos acessar a página de login
LOGIN_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/login/)
echo "Status da página de login: $LOGIN_RESPONSE"

if [ "$LOGIN_RESPONSE" -eq 200 ]; then
    echo "✅ Página de login acessível"
else
    echo "⚠️  Problema ao acessar a página de login"
fi

echo "========================================="
echo "Verificação concluída"
echo "========================================="