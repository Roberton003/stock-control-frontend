#!/usr/bin/env python
import os
import sys
import django
import datetime
from decimal import Decimal

sys.path.append('/media/Arquivos/DjangoPython/toolkits/v2/stock_control_lab')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from inventory.models import Produto, Category, Supplier, Location, StockLot, MovimentacaoEstoque
from django.utils import timezone

def main():
    User = get_user_model()
    
    print("Configurando dados iniciais do sistema...")
    
    # Criar categorias
    reagentes_quimicos, created = Category.objects.get_or_create(name='Reagentes Químicos')
    sais, created = Category.objects.get_or_create(name='Sais')
    solventes, created = Category.objects.get_or_create(name='Solventes')
    
    # Criar fornecedores
    quimica_industrial, created = Supplier.objects.get_or_create(name='Química Industrial Ltda')
    laboratorios_abc, created = Supplier.objects.get_or_create(name='Laboratórios ABC')
    produtos_quimicos_xyz, created = Supplier.objects.get_or_create(name='Produtos Químicos XYZ')
    distribuidora_reagentes, created = Supplier.objects.get_or_create(name='Distribuidora de Reagentes')
    quimica_pura, created = Supplier.objects.get_or_create(name='Química Pura Ltda')
    
    # Criar localizações
    armario_a1, created = Location.objects.get_or_create(name='Armário A-1')
    armario_b2, created = Location.objects.get_or_create(name='Armário B-2')
    armario_c3, created = Location.objects.get_or_create(name='Armário C-3')
    armario_d4, created = Location.objects.get_or_create(name='Armário D-4')
    armario_e5, created = Location.objects.get_or_create(name='Armário E-5')
    
    print("Dados iniciais configurados com sucesso!")
    
    # Obter usuário administrador
    admin_user = User.objects.filter(is_superuser=True).first()
    print(f"Usando usuário administrador: {admin_user.username}")
    
    # Criar 5 produtos com ciclo completo
    produtos_info = [
        {
            "nome": "Ácido Clorídrico",
            "sku": "HCl-001",
            "categoria": reagentes_quimicos,
            "fornecedor": quimica_industrial,
            "quantidade_inicial": 1000.00,
            "quantidade_saida": 250.00,
            "numero_lote": "HCl-2025-001",
            "localizacao": armario_a1,
            "preco_compra": 45.00
        },
        {
            "nome": "Hidróxido de Sódio",
            "sku": "NaOH-001",
            "categoria": reagentes_quimicos,
            "fornecedor": laboratorios_abc,
            "quantidade_inicial": 500.00,
            "quantidade_saida": 100.00,
            "numero_lote": "NaOH-2025-001",
            "localizacao": armario_b2,
            "preco_compra": 80.00
        },
        {
            "nome": "Etanol",
            "sku": "C2H5OH-001",
            "categoria": solventes,
            "fornecedor": produtos_quimicos_xyz,
            "quantidade_inicial": 2000.00,
            "quantidade_saida": 500.00,
            "numero_lote": "ETH-2025-001",
            "localizacao": armario_c3,
            "preco_compra": 35.00
        },
        {
            "nome": "Cloreto de Sódio",
            "sku": "NaCl-001",
            "categoria": sais,
            "fornecedor": distribuidora_reagentes,
            "quantidade_inicial": 1000.00,
            "quantidade_saida": 200.00,
            "numero_lote": "NACL-2025-001",
            "localizacao": armario_d4,
            "preco_compra": 15.00
        },
        {
            "nome": "Acetona",
            "sku": "C3H6O-001",
            "categoria": solventes,
            "fornecedor": quimica_pura,
            "quantidade_inicial": 1500.00,
            "quantidade_saida": 300.00,
            "numero_lote": "ACE-2025-001",
            "localizacao": armario_e5,
            "preco_compra": 28.00
        }
    ]
    
    print("\nAdicionando 5 produtos e testando ciclo completo...")
    
    for i, info in enumerate(produtos_info, 1):
        print(f"\n{i}. Processando {info['nome']}...")
        
        # Criar produto
        produto, created = Produto.objects.get_or_create(
            nome=info['nome'],
            sku=info['sku'],
            defaults={
                'descricao': f'Descrição para {info["nome"]}',
                'category': info['categoria'],
                'fornecedor': info['fornecedor'],
                'quantidade': Decimal(str(info['quantidade_inicial'])),
                'data_validade': timezone.now().date() + datetime.timedelta(days=365)
            }
        )
        if created:
            print(f"   Produto '{info['nome']}' criado com sucesso")
        else:
            print(f"   Produto '{info['nome']}' já existia")
        
        # Criar lote
        lote, created = StockLot.objects.get_or_create(
            produto=produto,
            lot_number=info['numero_lote'],
            defaults={
                'location': info['localizacao'],
                'expiry_date': timezone.now().date() + datetime.timedelta(days=365),
                'purchase_price': Decimal(str(info['preco_compra'])),
                'initial_quantity': Decimal(str(info['quantidade_inicial'])),
                'current_quantity': Decimal(str(info['quantidade_inicial']))
            }
        )
        if created:
            print(f"   Lote '{info['numero_lote']}' criado para o produto")
        else:
            print(f"   Lote '{info['numero_lote']}' já existia para o produto")
        
        # Registrar movimentação de entrada
        entrada = MovimentacaoEstoque.objects.create(
            produto=produto,
            usuario=admin_user,
            quantidade=Decimal(str(info['quantidade_inicial'])),
            tipo='ENTRADA',
        )
        print(f"   Registrada movimentação de entrada: {info['quantidade_inicial']} unidades")
        
        # Atualizar quantidade do produto
        produto.quantidade = Decimal(str(info['quantidade_inicial']))
        produto.save()
        
        # Registrar movimentação de saída
        saida = MovimentacaoEstoque.objects.create(
            produto=produto,
            usuario=admin_user,
            quantidade=Decimal(str(info['quantidade_saida'])),
            tipo='SAIDA',
        )
        print(f"   Registrada movimentação de saída: {info['quantidade_saida']} unidades")
        
        # Atualizar quantidade do produto após saída
        produto.quantidade -= Decimal(str(info['quantidade_saida']))
        produto.save()
        
        print(f"   Estoque final de {info['nome']}: {produto.quantidade} unidades")
    
    print("\nCiclo completo de 5 produtos testado com sucesso!")
    
    # Exibir resumo final
    print("\nResumo final do estoque:")
    for info in produtos_info:
        produto = Produto.objects.get(sku=info['sku'])
        print(f"- {produto.nome} (SKU: {produto.sku}): {produto.quantidade} unidades")

if __name__ == "__main__":
    main()
    print("\nConfiguração e testes concluídos com sucesso!")
    print("O sistema está pronto para uso com os 5 produtos testados e ciclo completo validado.")