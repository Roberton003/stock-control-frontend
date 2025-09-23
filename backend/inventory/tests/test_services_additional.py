import pytest
from decimal import Decimal
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
class TestAdditionalServiceCoverage:
    """Testes adicionais para alcançar 100% de cobertura nos services"""
    
    def test_get_consumption_by_user_report_with_filters(self):
        """Testa o relatório de consumo por usuário com filtros"""
        category = Category.objects.create(name='Reagentes Filtrados')
        supplier = Supplier.objects.create(name='Fornecedor Filtrado')
        location = Location.objects.create(name='Laboratório Filtrado')
        user1 = User.objects.create_user(username='analista_filtrado_a', password='testpass', role='Analista')
        user2 = User.objects.create_user(username='analista_filtrado_b', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente Filtrado A',
            sku='REA-FIL-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Filtrado B',
            sku='REA-FIL-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        # Criar movimentações para diferentes usuários
        with freeze_time("2025-03-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='LOT-FIL-A-001',
                    location=location,
                    expiry_date=datetime.date(2026, 3, 1),
                    purchase_price=Decimal('12.00'),
                    initial_quantity=Decimal('400.00'),
                    current_quantity=Decimal('400.00')
                ),
                user=user1,
                quantity=Decimal('40.00'),
                move_type='Retirada'
            )
            
        with freeze_time("2025-03-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='LOT-FIL-B-001',
                    location=location,
                    expiry_date=datetime.date(2026, 3, 15),
                    purchase_price=Decimal('18.00'),
                    initial_quantity=Decimal('300.00'),
                    current_quantity=Decimal('300.00')
                ),
                user=user2,
                quantity=Decimal('35.00'),
                move_type='Retirada'
            )
            
        # Gerar relatório filtrado por usuário
        start_date = datetime.date(2025, 3, 1)
        end_date = datetime.date(2025, 3, 31)
        report_data_filtered_user = get_consumption_by_user_report(start_date, end_date, user_id=user1.id)
        
        # Verificar resultados filtrados por usuário
        assert len(report_data_filtered_user) == 1
        assert report_data_filtered_user[0]['user__username'] == 'analista_filtrado_a'
        assert report_data_filtered_user[0]['total_quantity'] == Decimal('40.00')
        
        # Gerar relatório filtrado por reagente
        report_data_filtered_reagent = get_consumption_by_user_report(start_date, end_date, reagent_id=reagent2.id)
        
        # Verificar resultados filtrados por reagente
        assert len(report_data_filtered_reagent) == 1
        assert report_data_filtered_reagent[0]['stock_lot__reagent__name'] == 'Reagente Filtrado B'
        assert report_data_filtered_reagent[0]['total_quantity'] == Decimal('35.00')
        
        # Gerar relatório com ambos os filtros
        report_data_double_filtered = get_consumption_by_user_report(start_date, end_date, user_id=user2.id, reagent_id=reagent2.id)
        
        # Verificar resultados com duplo filtro
        assert len(report_data_double_filtered) == 1
        assert report_data_double_filtered[0]['user__username'] == 'analista_filtrado_b'
        assert report_data_double_filtered[0]['stock_lot__reagent__name'] == 'Reagente Filtrado B'
        assert report_data_double_filtered[0]['total_quantity'] == Decimal('35.00')

    def test_get_waste_loss_report_with_reagent_filter(self):
        """Testa o relatório de desperdício/perda com filtro de reagente"""
        category = Category.objects.create(name='Reagentes de Teste Filtrado')
        supplier = Supplier.objects.create(name='Fornecedor Filtrado Ltda')
        location = Location.objects.create(name='Laboratório de Testes Filtrados')
        user = User.objects.create_user(username='teste_filtrado', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente para Teste A',
            sku='TEST-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente para Teste B',
            sku='TEST-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        # Criar movimentações de descarte para diferentes reagentes
        with freeze_time("2025-04-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='TEST-A-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 4, 1),
                    purchase_price=Decimal('22.00'),
                    initial_quantity=Decimal('800.00'),
                    current_quantity=Decimal('800.00')
                ),
                user=user,
                quantity=Decimal('60.00'),
                move_type='Descarte'
            )
            
        with freeze_time("2025-04-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='TEST-B-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 4, 15),
                    purchase_price=Decimal('28.00'),
                    initial_quantity=Decimal('600.00'),
                    current_quantity=Decimal('600.00')
                ),
                user=user,
                quantity=Decimal('-40.00'),  # Ajuste negativo
                move_type='Ajuste'
            )
            
        # Gerar relatório filtrado por reagente
        start_date = datetime.date(2025, 4, 1)
        end_date = datetime.date(2025, 4, 30)
        report_data_filtered = get_waste_loss_report(start_date, end_date, reagent_id=reagent1.id)
        
        # Verificar resultados filtrados
        assert len(report_data_filtered) == 1
        assert report_data_filtered[0]['stock_lot__reagent__name'] == 'Reagente para Teste A'
        assert report_data_filtered[0]['move_type'] == 'Descarte'
        assert report_data_filtered[0]['total_quantity'] == Decimal('60.00')

    def test_get_stock_value_report_with_grouping(self):
        """Testa o relatório de valor do estoque com agrupamento"""
        category1 = Category.objects.create(name='Categoria A')
        category2 = Category.objects.create(name='Categoria B')
        supplier = Supplier.objects.create(name='Fornecedor Agrupado')
        location1 = Location.objects.create(name='Localização Alpha')
        location2 = Location.objects.create(name='Localização Beta')
        reagent1 = Reagent.objects.create(
            name='Reagente Alpha',
            sku='ALPHA-001',
            category=category1,
            supplier=supplier,
            min_stock_level=Decimal('10.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Beta',
            sku='BETA-001',
            category=category2,
            supplier=supplier,
            min_stock_level=Decimal('15.00')
        )
        
        # Criar lotes de estoque
        StockLot.objects.create(
            reagent=reagent1,
            lot_number='ALPHA-2025',
            location=location1,
            expiry_date=datetime.date(2027, 1, 1),
            purchase_price=Decimal('1200.00'),
            initial_quantity=Decimal('12.00'),
            current_quantity=Decimal('10.00')
        )
        
        StockLot.objects.create(
            reagent=reagent2,
            lot_number='BETA-2025',
            location=location2,
            expiry_date=datetime.date(2027, 2, 1),
            purchase_price=Decimal('1800.00'),
            initial_quantity=Decimal('18.00'),
            current_quantity=Decimal('15.00')
        )
        
        # Gerar relatório agrupado por categoria
        category_report = get_stock_value_report(group_by='category')
        assert len(category_report) == 2
        category_values = {item['reagent__category__name']: item['total_value'] for item in category_report}
        assert category_values['Categoria A'] == Decimal('12000.00')  # 10 * 1200
        assert category_values['Categoria B'] == Decimal('27000.00')  # 15 * 1800
        
        # Gerar relatório agrupado por localização
        location_report = get_stock_value_report(group_by='location')
        assert len(location_report) == 2
        location_values = {item['location__name']: item['total_value'] for item in location_report}
        assert location_values['Localização Alpha'] == Decimal('12000.00')
        assert location_values['Localização Beta'] == Decimal('27000.00')

    def test_calculate_total_stock_value_with_valid_data(self):
        """Testa o cálculo do valor total do estoque com dados válidos"""
        category = Category.objects.create(name='Produtos Com Valor')
        supplier = Supplier.objects.create(name='Fornecedor Com Valor')
        location = Location.objects.create(name='Local Com Valor')
        reagent = Reagent.objects.create(
            name='Produto Com Valor',
            sku='VALOR-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('5.00')
        )
        
        # Criar lote de estoque com valor
        StockLot.objects.create(
            reagent=reagent,
            lot_number='VALOR-2025',
            location=location,
            expiry_date=datetime.date(2027, 12, 31),
            purchase_price=Decimal('500.00'),
            initial_quantity=Decimal('50.00'),
            current_quantity=Decimal('40.00')
        )
        
        # Calcular valor total
        total_value = calculate_total_stock_value()
        expected_value = Decimal('40.00') * Decimal('500.00')  # 20000
        assert total_value == expected_value