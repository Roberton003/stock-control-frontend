import pytest
from decimal import Decimal
from inventory.models import (
    User, Category, Supplier, Location, Reagent, 
    StockLot, StockMovement, Requisition
)
from inventory.services import (
    get_consumption_by_user_report, get_waste_loss_report, 
    get_stock_value_report, get_expiry_report, calculate_total_stock_value
)
import datetime
from django.utils import timezone
from freezegun import freeze_time


@pytest.mark.django_db
class TestRemainingServices:
    """Testes para as funções restantes dos services com baixa cobertura"""
    
    def test_get_consumption_by_user_report_with_filters(self):
        """Testa o relatório de consumo por usuário com filtros"""
        category = Category.objects.create(name='Reagentes Report Filter')
        supplier = Supplier.objects.create(name='Fornecedor Report Filter')
        location = Location.objects.create(name='Laboratório Report Filter')
        user1 = User.objects.create_user(username='analista_report_a', password='testpass', role='Analista')
        user2 = User.objects.create_user(username='analista_report_b', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente Report A',
            sku='REP-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Report B',
            sku='REP-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        # Criar movimentações para diferentes usuários e reagentes
        with freeze_time("2025-08-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='REP-A-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 8, 1),
                    purchase_price=Decimal('10.00'),
                    initial_quantity=Decimal('500.00'),
                    current_quantity=Decimal('500.00')
                ),
                user=user1,
                quantity=Decimal('50.00'),
                move_type='Retirada'
            )
            
        with freeze_time("2025-08-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='REP-B-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 8, 15),
                    purchase_price=Decimal('15.00'),
                    initial_quantity=Decimal('300.00'),
                    current_quantity=Decimal('300.00')
                ),
                user=user2,
                quantity=Decimal('35.00'),
                move_type='Retirada'
            )
            
        # Gerar relatório filtrado por usuário
        start_date = datetime.date(2025, 8, 1)
        end_date = datetime.date(2025, 8, 31)
        user_report = get_consumption_by_user_report(start_date, end_date, user_id=user1.id)
        
        # Verificar resultados filtrados por usuário
        assert len(user_report) == 1
        assert user_report[0]['user__username'] == 'analista_report_a'
        assert user_report[0]['stock_lot__reagent__name'] == 'Reagente Report A'
        assert user_report[0]['total_quantity'] == Decimal('50.00')
        
        # Gerar relatório filtrado por reagente
        reagent_report = get_consumption_by_user_report(start_date, end_date, reagent_id=reagent2.id)
        
        # Verificar resultados filtrados por reagente
        assert len(reagent_report) == 1
        assert reagent_report[0]['user__username'] == 'analista_report_b'
        assert reagent_report[0]['stock_lot__reagent__name'] == 'Reagente Report B'
        assert reagent_report[0]['total_quantity'] == Decimal('35.00')
        
        # Gerar relatório com ambos os filtros
        combined_report = get_consumption_by_user_report(start_date, end_date, user_id=user2.id, reagent_id=reagent2.id)
        
        # Verificar resultados com filtros combinados
        assert len(combined_report) == 1
        assert combined_report[0]['user__username'] == 'analista_report_b'
        assert combined_report[0]['stock_lot__reagent__name'] == 'Reagente Report B'
        assert combined_report[0]['total_quantity'] == Decimal('35.00')

    def test_get_waste_loss_report_with_filters(self):
        """Testa o relatório de desperdício/perda com filtros"""
        category = Category.objects.create(name='Reagentes Waste Filter')
        supplier = Supplier.objects.create(name='Fornecedor Waste Filter')
        location = Location.objects.create(name='Laboratório Waste Filter')
        user = User.objects.create_user(username='analista_waste', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente Waste A',
            sku='WST-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Waste B',
            sku='WST-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        # Criar movimentações de desperdício para diferentes reagentes
        with freeze_time("2025-09-01"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='WST-A-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 9, 1),
                    purchase_price=Decimal('20.00'),
                    initial_quantity=Decimal('400.00'),
                    current_quantity=Decimal('400.00')
                ),
                user=user,
                quantity=Decimal('60.00'),
                move_type='Descarte'
            )
            
        with freeze_time("2025-09-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='WST-B-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 9, 15),
                    purchase_price=Decimal('25.00'),
                    initial_quantity=Decimal('300.00'),
                    current_quantity=Decimal('300.00')
                ),
                user=user,
                quantity=Decimal('-40.00'),  # Ajuste negativo
                move_type='Ajuste'
            )
            
        # Gerar relatório filtrado por reagente
        start_date = datetime.date(2025, 9, 1)
        end_date = datetime.date(2025, 9, 30)
        reagent_filtered_report = get_waste_loss_report(start_date, end_date, reagent_id=reagent1.id)
        
        # Verificar resultados filtrados por reagente
        assert len(reagent_filtered_report) == 1
        assert reagent_filtered_report[0]['stock_lot__reagent__name'] == 'Reagente Waste A'
        assert reagent_filtered_report[0]['move_type'] == 'Descarte'
        assert reagent_filtered_report[0]['total_quantity'] == Decimal('60.00')

    def test_get_stock_value_report_invalid_group_by(self):
        """Testa o relatório de valor do estoque com group_by inválido"""
        # Tentar chamar com group_by inválido
        with pytest.raises(ValueError, match="Invalid group_by parameter. Must be 'category', 'location', or None."):
            get_stock_value_report(group_by='invalid_parameter')

    def test_get_expiry_report_with_days_until_expiry(self):
        """Testa o relatório de validade com filtro de dias até expirar"""
        category = Category.objects.create(name='Reagentes Expiry Days')
        supplier = Supplier.objects.create(name='Fornecedor Expiry Days')
        location = Location.objects.create(name='Laboratório Expiry Days')
        reagent = Reagent.objects.create(
            name='Reagente Expiry Days',
            sku='EXP-DAYS-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('15.00')
        )
        
        today = timezone.now().date()
        
        # Criar lotes com diferentes datas de validade
        near_expiry_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='EXP-DAYS-NEAR',
            location=location,
            expiry_date=today + datetime.timedelta(days=10),  # Expira em 10 dias
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('200.00'),
            current_quantity=Decimal('200.00')
        )
        
        far_expiry_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='EXP-DAYS-FAR',
            location=location,
            expiry_date=today + datetime.timedelta(days=60),  # Expira em 60 dias
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('150.00'),
            current_quantity=Decimal('150.00')
        )
        
        # Criar lote expirado
        expired_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='EXP-DAYS-EXPIRED',
            location=location,
            expiry_date=today - datetime.timedelta(days=5),  # Expirado
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        
        # Gerar relatório para produtos que expiram em até 30 dias
        expiry_report = get_expiry_report(days_until_expiry=30)
        
        # Verificar que apenas o lote próximo da validade aparece
        assert len(expiry_report) == 1
        assert expiry_report[0]['lot_number'] == 'EXP-DAYS-NEAR'
        assert expiry_report[0]['reagent__name'] == 'Reagente Expiry Days'
        assert expiry_report[0]['current_quantity'] == Decimal('200.00')

    def test_calculate_total_stock_value_with_data(self):
        """Testa o cálculo do valor total do estoque com dados"""
        category = Category.objects.create(name='Reagentes Stock Value')
        supplier = Supplier.objects.create(name='Fornecedor Stock Value')
        location = Location.objects.create(name='Laboratório Stock Value')
        reagent = Reagent.objects.create(
            name='Reagente Stock Value',
            sku='STOCK-VAL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('20.00')
        )
        
        # Criar múltiplos lotes de estoque
        StockLot.objects.create(
            reagent=reagent,
            lot_number='STOCK-VAL-A',
            location=location,
            expiry_date=datetime.date(2027, 1, 1),
            purchase_price=Decimal('100.00'),
            initial_quantity=Decimal('50.00'),
            current_quantity=Decimal('50.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='STOCK-VAL-B',
            location=location,
            expiry_date=datetime.date(2027, 2, 1),
            purchase_price=Decimal('150.00'),
            initial_quantity=Decimal('30.00'),
            current_quantity=Decimal('30.00')
        )
        
        # Calcular valor total do estoque
        total_value = calculate_total_stock_value()
        
        # Verificar resultado (50 * 100) + (30 * 150) = 5000 + 4500 = 9500
        expected_value = Decimal('50.00') * Decimal('100.00') + Decimal('30.00') * Decimal('150.00')
        assert total_value == expected_value