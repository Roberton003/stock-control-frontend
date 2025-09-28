#!/usr/bin/env python3
import os
import sys
import django

sys.path.append('/media/Arquivos/DjangoPython/toolkits/v2/stock_control_lab')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import Produto, MovimentacaoEstoque, StockLot
from django.contrib.auth import get_user_model

User = get_user_model()

print('=' * 60)
print('VERIFICAÇÃO DO STATUS DO SISTEMA DE CONTROLE DE ESTOQUE')
print('=' * 60)

# Verificar usuários
total_usuarios = User.objects.count()
usuarios_admin = User.objects.filter(is_superuser=True).count()
print(f'Usuarios cadastrados: {total_usuarios}')
print(f'Usuarios administradores: {usuarios_admin}')

# Verificar produtos
total_produtos = Produto.objects.count()
print(f'Produtos cadastrados: {total_produtos}')

# Verificar movimentações
total_movimentacoes = MovimentacaoEstoque.objects.count()
movimentacoes_entrada = MovimentacaoEstoque.objects.filter(tipo='ENTRADA').count()
movimentacoes_saida = MovimentacaoEstoque.objects.filter(tipo='SAIDA').count()
print(f'Movimentacoes registradas: {total_movimentacoes}')
print(f'  - Entradas: {movimentacoes_entrada}')
print(f'  - Saidas: {movimentacoes_saida}')

# Verificar lotes
total_lotes = StockLot.objects.count()
print(f'Lotes de estoque: {total_lotes}')

# Listar produtos testes
if total_produtos > 0:
    print('')
    print('Produtos principais:')
    produtos_teste = ['HCl-001', 'NaOH-001', 'C2H5OH-001', 'NaCl-001', 'C3H6O-001']
    for produto in Produto.objects.filter(sku__in=produtos_teste):
        print(f'  - {produto.nome} ({produto.sku}): {produto.quantidade} unidades')

print('')
print('=' * 60)
print('STATUS: SISTEMA OPERACIONAL')
print('=' * 60)
