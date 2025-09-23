import pytest
import os
import sys
import django
from decimal import Decimal

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import (
    User, Category, Supplier, Location, Reagent, 
    StockLot, StockMovement, Requisition
)
from inventory.services import (
    get_consumption_by_user_report, get_waste_loss_report, 
    get_stock_value_report, calculate_total_stock_value
)
import datetime
from django.utils import timezone
from freezegun import freeze_time


@pytest.mark.django_db
class TestServiceCoverage:
    """Testes para alcançar 100% de cobertura nos services"""
    
    def test_get_consumption_by_user_report_with_user_id_filter(self):
        """Testa o relatório de consumo por usuário com filtro de user_id"""
        category = Category.objects.create(name='Reagentes User Filter')
        supplier = Supplier.objects.create(name='Fornecedor User Filter')
        location = Location.objects.create(name='Laboratório User Filter')
        user1 = User.objects.create_user(username='analista_user_filter_a', password='testpass', role='Analista')
        user2 = User.objects.create_user(username='analista_user_filter_b', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Reagente User Filter',
            sku='USER-FILTER-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        # Criar movimentações para diferentes usuários
        with freeze_time("2025-05-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent,
                    lot_number='USER-FILTER-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 5, 1),
                    purchase_price=Decimal('15.00'),
                    initial_quantity=Decimal('500.00'),
                    current_quantity=Decimal('500.00')
                ),
                user=user1,
                quantity=Decimal('50.00'),
                move_type='Retirada'
            )
            
        with freeze_time("2025-05-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent,
                    lot_number='USER-FILTER-2025-B',
                    location=location,
                    expiry_date=datetime.date(2026, 5, 15),
                    purchase_price=Decimal('15.00'),
                    initial_quantity=Decimal('500.00'),
                    current_quantity=Decimal('500.00')
                ),
                user=user2,
                quantity=Decimal('75.00'),
                move_type='Retirada'
            )
            
        # Gerar relatório filtrado por user_id
        start_date = datetime.date(2025, 5, 1)
        end_date = datetime.date(2025, 5, 31)
        report_data = get_consumption_by_user_report(start_date, end_date, user_id=user1.id)
        
        # Verificar que apenas as movimentações do usuário filtrado aparecem
        assert len(report_data) == 1
        assert report_data[0]['user__username'] == 'analista_user_filter_a'
        assert report_data[0]['total_quantity'] == Decimal('50.00')

    def test_get_consumption_by_user_report_with_reagent_id_filter(self):
        """Testa o relatório de consumo por usuário com filtro de reagent_id"""
        category = Category.objects.create(name='Reagentes Reagent Filter')
        supplier = Supplier.objects.create(name='Fornecedor Reagent Filter')
        location = Location.objects.create(name='Laboratório Reagent Filter')
        user = User.objects.create_user(username='analista_reagent_filter', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente Reagent Filter A',
            sku='REAGENT-FILTER-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Reagent Filter B',
            sku='REAGENT-FILTER-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        # Criar movimentações para diferentes reagentes
        with freeze_time("2025-06-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='REAGENT-FILTER-A-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 6, 1),
                    purchase_price=Decimal('20.00'),
                    initial_quantity=Decimal('600.00'),
                    current_quantity=Decimal('600.00')
                ),
                user=user,
                quantity=Decimal('60.00'),
                move_type='Retirada'
            )
            
        with freeze_time("2025-06-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='REAGENT-FILTER-B-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 6, 15),
                    purchase_price=Decimal('20.00'),
                    initial_quantity=Decimal('600.00'),
                    current_quantity=Decimal('600.00')
                ),
                user=user,
                quantity=Decimal('85.00'),
                move_type='Retirada'
            )
            
        # Gerar relatório filtrado por reagent_id
        start_date = datetime.date(2025, 6, 1)
        end_date = datetime.date(2025, 6, 30)
        report_data = get_consumption_by_user_report(start_date, end_date, reagent_id=reagent1.id)
        
        # Verificar que apenas as movimentações do reagente filtrado aparecem
        assert len(report_data) == 1
        assert report_data[0]['stock_lot__reagent__name'] == 'Reagente Reagent Filter A'
        assert report_data[0]['total_quantity'] == Decimal('60.00')

    def test_get_waste_loss_report_with_reagent_id_filter(self):
        """Testa o relatório de desperdício/perda com filtro de reagent_id"""
        category = Category.objects.create(name='Reagentes Waste Filter')
        supplier = Supplier.objects.create(name='Fornecedor Waste Filter')
        location = Location.objects.create(name='Laboratório Waste Filter')
        user = User.objects.create_user(username='analista_waste_filter', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente Waste Filter A',
            sku='WASTE-FILTER-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('30.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Waste Filter B',
            sku='WASTE-FILTER-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('30.00')
        )
        
        # Criar movimentações de descarte para diferentes reagentes
        with freeze_time("2025-07-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='WASTE-FILTER-A-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 7, 1),
                    purchase_price=Decimal('25.00'),
                    initial_quantity=Decimal('700.00'),
                    current_quantity=Decimal('700.00')
                ),
                user=user,
                quantity=Decimal('70.00'),
                move_type='Descarte'
            )
            
        with freeze_time("2025-07-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='WASTE-FILTER-B-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 7, 15),
                    purchase_price=Decimal('25.00'),
                    initial_quantity=Decimal('700.00'),
                    current_quantity=Decimal('700.00')
                ),
                user=user,
                quantity=Decimal('-55.00'),  # Ajuste negativo
                move_type='Ajuste'
            )
            
        # Gerar relatório filtrado por reagent_id
        start_date = datetime.date(2025, 7, 1)
        end_date = datetime.date(2025, 7, 31)
        report_data = get_waste_loss_report(start_date, end_date, reagent_id=reagent1.id)
        
        # Verificar que apenas as movimentações do reagente filtrado aparecem
        assert len(report_data) == 1
        assert report_data[0]['stock_lot__reagent__name'] == 'Reagente Waste Filter A'
        assert report_data[0]['move_type'] == 'Descarte'
        assert report_data[0]['total_quantity'] == Decimal('70.00')

    def test_get_stock_value_report_invalid_group_by(self):
        """Testa o relatório de valor do estoque com group_by inválido"""
        # Tentar chamar com group_by inválido
        with pytest.raises(ValueError, match="Invalid group_by parameter. Must be 'category', 'location', or None."):
            get_stock_value_report(group_by='invalid')

    def test_calculate_total_stock_value_with_data(self):
        """Testa o cálculo do valor total do estoque com dados"""
        category = Category.objects.create(name='Produtos Com Valor Real')
        supplier = Supplier.objects.create(name='Fornecedor Com Valor Real')
        location = Location.objects.create(name='Local Com Valor Real')
        reagent = Reagent.objects.create(
            name='Produto Com Valor Real',
            sku='VALOR-REAL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('10.00')
        )
        
        # Criar lote de estoque com valor real
        StockLot.objects.create(
            reagent=reagent,
            lot_number='VALOR-REAL-2025',
            location=location,
            expiry_date=datetime.date(2028, 1, 1),
            purchase_price=Decimal('1000.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('80.00')
        )
        
        # Calcular valor total
        total_value = calculate_total_stock_value()
        expected_value = Decimal('80.00') * Decimal('1000.00')  # 80000
        assert total_value == expected_value