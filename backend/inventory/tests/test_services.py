import pytest
from decimal import Decimal
from inventory.models import (
    User, Category, Supplier, Location, Reagent, 
    StockLot, StockMovement, Requisition
)
from inventory.services import (
    get_lots_for_withdrawal, perform_withdrawal, approve_requisition,
    get_consumption_by_user_report, get_waste_loss_report, 
    get_stock_value_report, get_expiry_report, calculate_total_stock_value
)
import datetime
from django.utils import timezone
from freezegun import freeze_time


@pytest.mark.django_db
class TestGetLotsForWithdrawal:
    """Testes para a função get_lots_for_withdrawal"""
    
    def test_get_lots_for_withdrawal_fefo_order(self):
        """Testa que a função aplica corretamente a lógica FEFO"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor Exemplo')
        location = Location.objects.create(name='Armário Principal')
        reagent = Reagent.objects.create(
            name='Ácido Clorídrico',
            sku='HCL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        
        # Criar múltiplos lotes com diferentes datas de validade
        lot_a = StockLot.objects.create(
            reagent=reagent,
            lot_number='HCL-A',
            location=location,
            expiry_date=datetime.date(2025, 1, 1),  # Expira primeiro
            purchase_price=Decimal('10.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        lot_b = StockLot.objects.create(
            reagent=reagent,
            lot_number='HCL-B',
            location=location,
            expiry_date=datetime.date(2025, 6, 1),  # Expira segundo
            purchase_price=Decimal('10.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        lot_c = StockLot.objects.create(
            reagent=reagent,
            lot_number='HCL-C',
            location=location,
            expiry_date=datetime.date(2026, 1, 1),  # Expira por último
            purchase_price=Decimal('10.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        
        # Solicitar quantidade que pode ser coberta por um lote
        lots_info = get_lots_for_withdrawal(reagent, 50.00)
        
        # Deve selecionar apenas o primeiro lote (FEFO)
        assert len(lots_info) == 1
        assert lots_info[0][0] == lot_a
        assert lots_info[0][1] == Decimal('50.00')
        
        # Solicitar quantidade que requer múltiplos lotes
        lots_info = get_lots_for_withdrawal(reagent, 150.00)
        
        # Deve selecionar os dois primeiros lotes (FEFO)
        assert len(lots_info) == 2
        assert lots_info[0][0] == lot_a
        assert lots_info[0][1] == Decimal('100.00')
        assert lots_info[1][0] == lot_b
        assert lots_info[1][1] == Decimal('50.00')

    def test_get_lots_for_withdrawal_insufficient_stock(self):
        """Testa comportamento quando não há estoque suficiente"""
        category = Category.objects.create(name='Bases')
        supplier = Supplier.objects.create(name='Outro Fornecedor')
        location = Location.objects.create(name='Laboratório B')
        reagent = Reagent.objects.create(
            name='Hidróxido de Sódio',
            sku='NAOH-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='NAOH-001',
            location=location,
            expiry_date=datetime.date(2025, 12, 31),
            purchase_price=Decimal('15.00'),
            initial_quantity=Decimal('75.00'),
            current_quantity=Decimal('75.00')
        )
        
        # Solicitar quantidade maior que o estoque disponível
        with pytest.raises(ValueError, match="Not enough stock"):
            get_lots_for_withdrawal(reagent, 100.00)


@pytest.mark.django_db
class TestPerformWithdrawal:
    """Testes para a função perform_withdrawal"""
    
    def test_perform_withdrawal_updates_quantities(self):
        """Testa que a função atualiza corretamente as quantidades de estoque"""
        category = Category.objects.create(name='Sais')
        supplier = Supplier.objects.create(name='Fornecedor de Sais')
        location = Location.objects.create(name='Prateleira C-1')
        user = User.objects.create_user(username='analista1', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Cloreto de Sódio',
            sku='NACL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('200.00')
        )
        
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='NACL20250917',
            location=location,
            expiry_date=datetime.date(2026, 9, 17),
            purchase_price=Decimal('25.00'),
            initial_quantity=Decimal('1000.00'),
            current_quantity=Decimal('1000.00')
        )
        
        # Realizar retirada
        total_withdrawn = perform_withdrawal(reagent, 100.00, user)
        
        # Verificar resultados
        assert total_withdrawn == Decimal('100.00')
        stock_lot.refresh_from_db()
        assert stock_lot.current_quantity == Decimal('900.00')
        
        # Verificar que foi criado um registro de movimentação
        movement = StockMovement.objects.get(stock_lot=stock_lot, user=user)
        assert movement.quantity == Decimal('100.00')
        assert movement.move_type == 'Retirada'

    def test_perform_withdrawal_multiple_lots(self):
        """Testa retirada que utiliza múltiplos lotes"""
        category = Category.objects.create(name='Solventes')
        supplier = Supplier.objects.create(name='Fornecedor de Solventes')
        location = Location.objects.create(name='Armário 5')
        user = User.objects.create_user(username='analista2', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Etanol',
            sku='ETOH-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('500.00')
        )
        
        # Criar dois lotes
        lot_a = StockLot.objects.create(
            reagent=reagent,
            lot_number='ETOH-A',
            location=location,
            expiry_date=datetime.date(2025, 3, 1),
            purchase_price=Decimal('20.00'),
            initial_quantity=Decimal('300.00'),
            current_quantity=Decimal('300.00')
        )
        lot_b = StockLot.objects.create(
            reagent=reagent,
            lot_number='ETOH-B',
            location=location,
            expiry_date=datetime.date(2025, 9, 1),
            purchase_price=Decimal('20.00'),
            initial_quantity=Decimal('400.00'),
            current_quantity=Decimal('400.00')
        )
        
        # Realizar retirada que usa ambos os lotes
        total_withdrawn = perform_withdrawal(reagent, 500.00, user)
        
        # Verificar resultados
        assert total_withdrawn == Decimal('500.00')
        lot_a.refresh_from_db()
        lot_b.refresh_from_db()
        assert lot_a.current_quantity == Decimal('0.00')  # Lote A esgotado
        assert lot_b.current_quantity == Decimal('200.00')  # Lote B com 200 restantes
        
        # Verificar registros de movimentação
        movements = StockMovement.objects.filter(stock_lot__reagent=reagent, user=user)
        assert movements.count() == 2
        assert movements.filter(stock_lot=lot_a, quantity=Decimal('300.00')).exists()
        assert movements.filter(stock_lot=lot_b, quantity=Decimal('200.00')).exists()


@pytest.mark.django_db
class TestApproveRequisition:
    """Testes para a função approve_requisition"""
    
    def test_approve_requisition_success(self):
        """Testa aprovação bem-sucedida de uma requisição"""
        category = Category.objects.create(name='Indicadores')
        supplier = Supplier.objects.create(name='Fornecedor de Indicadores')
        location = Location.objects.create(name='Laboratório C')
        requester = User.objects.create_user(username='pesquisador1', password='testpass', role='Convidado')
        approver = User.objects.create_user(username='supervisor1', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Fenolftaleína',
            sku='FENOL-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='FENOL20250101',
            location=location,
            expiry_date=datetime.date(2026, 1, 1),
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        
        requisition = Requisition.objects.create(
            requester=requester,
            reagent=reagent,
            quantity=Decimal('10.00'),
            status='Pendente'
        )
        
        # Aprovar requisição
        result = approve_requisition(requisition, approver)
        
        # Verificar resultados
        assert result is True
        requisition.refresh_from_db()
        assert requisition.status == 'Aprovada'
        assert requisition.approver == approver
        assert requisition.approval_date is not None
        
        # Verificar que o estoque foi atualizado
        reagent.refresh_from_db()
        stock_lot = StockLot.objects.get(reagent=reagent)
        assert stock_lot.current_quantity == Decimal('90.00')  # 100 - 10
        
        # Verificar que foi criado um registro de movimentação
        movement = StockMovement.objects.get(stock_lot=stock_lot, user=approver)
        assert movement.quantity == Decimal('10.00')
        assert movement.move_type == 'Retirada'

    def test_approve_requisition_invalid_status(self):
        """Testa tentativa de aprovar uma requisição com status inválido"""
        category = Category.objects.create(name='Ácidos')
        supplier = Supplier.objects.create(name='Fornecedor Ácidos')
        requester = User.objects.create_user(username='pesquisador2', password='testpass', role='Convidado')
        approver = User.objects.create_user(username='supervisor2', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Ácido Sulfúrico',
            sku='H2SO4-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        requisition = Requisition.objects.create(
            requester=requester,
            reagent=reagent,
            quantity=Decimal('5.00'),
            status='Aprovada'  # Já aprovada
        )
        
        # Tentar aprovar requisição já aprovada
        with pytest.raises(ValueError, match="Requisition is not in 'Pendente' status"):
            approve_requisition(requisition, approver)


@pytest.mark.django_db
class TestReports:
    """Testes para as funções de relatórios"""
    
    def test_get_consumption_by_user_report(self):
        """Testa o relatório de consumo por usuário"""
        category = Category.objects.create(name='Reagentes')
        supplier = Supplier.objects.create(name='Fornecedor Geral')
        location = Location.objects.create(name='Laboratório Principal')
        user1 = User.objects.create_user(username='analista_a', password='testpass', role='Analista')
        user2 = User.objects.create_user(username='analista_b', password='testpass', role='Analista')
        reagent1 = Reagent.objects.create(
            name='Reagente A',
            sku='REA-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente B',
            sku='REA-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        
        # Criar movimentações para diferentes usuários
        with freeze_time("2025-01-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent1,
                    lot_number='LOT-A-001',
                    location=location,
                    expiry_date=datetime.date(2026, 1, 1),
                    purchase_price=Decimal('10.00'),
                    initial_quantity=Decimal('500.00'),
                    current_quantity=Decimal('500.00')
                ),
                user=user1,
                quantity=Decimal('50.00'),
                move_type='Retirada'
            )
            
        with freeze_time("2025-02-10"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent2,
                    lot_number='LOT-B-001',
                    location=location,
                    expiry_date=datetime.date(2026, 2, 1),
                    purchase_price=Decimal('15.00'),
                    initial_quantity=Decimal('300.00'),
                    current_quantity=Decimal('300.00')
                ),
                user=user2,
                quantity=Decimal('30.00'),
                move_type='Retirada'
            )
            
        # Gerar relatório
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 2, 28)
        report_data = get_consumption_by_user_report(start_date, end_date)
        
        # Verificar resultados
        assert len(report_data) == 2
        assert any(item['user__username'] == 'analista_a' and item['total_quantity'] == Decimal('50.00') for item in report_data)
        assert any(item['user__username'] == 'analista_b' and item['total_quantity'] == Decimal('30.00') for item in report_data)

    def test_get_waste_loss_report(self):
        """Testa o relatório de desperdício/perda"""
        category = Category.objects.create(name='Limpeza')
        supplier = Supplier.objects.create(name='Fornecedor de Limpeza')
        location = Location.objects.create(name='Área de Limpeza')
        user = User.objects.create_user(username='limpeza', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Álcool Isopropílico',
            sku='ISO-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('200.00')
        )
        
        # Criar movimentações de descarte e ajuste negativo
        with freeze_time("2025-01-20"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent,
                    lot_number='ISO-2025',
                    location=location,
                    expiry_date=datetime.date(2026, 1, 1),
                    purchase_price=Decimal('20.00'),
                    initial_quantity=Decimal('1000.00'),
                    current_quantity=Decimal('1000.00')
                ),
                user=user,
                quantity=Decimal('50.00'),
                move_type='Descarte'
            )
            
        with freeze_time("2025-02-15"):
            StockMovement.objects.create(
                stock_lot=StockLot.objects.create(
                    reagent=reagent,
                    lot_number='ISO-2025-B',
                    location=location,
                    expiry_date=datetime.date(2026, 2, 1),
                    purchase_price=Decimal('20.00'),
                    initial_quantity=Decimal('500.00'),
                    current_quantity=Decimal('500.00')
                ),
                user=user,
                quantity=Decimal('-25.00'),  # Ajuste negativo
                move_type='Ajuste'
            )
            
        # Gerar relatório
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 2, 28)
        report_data = get_waste_loss_report(start_date, end_date)
        
        # Verificar resultados
        assert len(report_data) == 2
        assert any(item['move_type'] == 'Descarte' and item['total_quantity'] == Decimal('50.00') for item in report_data)
        assert any(item['move_type'] == 'Ajuste' and item['total_quantity'] == Decimal('-25.00') for item in report_data)

    def test_get_stock_value_report(self):
        """Testa o relatório de valor do estoque"""
        category = Category.objects.create(name='Equipamentos')
        supplier = Supplier.objects.create(name='Fornecedor de Equipamentos')
        location1 = Location.objects.create(name='Laboratório A')
        location2 = Location.objects.create(name='Laboratório B')
        reagent1 = Reagent.objects.create(
            name='Equipamento A',
            sku='EQP-A-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('5.00')
        )
        reagent2 = Reagent.objects.create(
            name='Equipamento B',
            sku='EQP-B-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('3.00')
        )
        
        # Criar lotes de estoque
        StockLot.objects.create(
            reagent=reagent1,
            lot_number='EQP-A-001',
            location=location1,
            expiry_date=datetime.date(2027, 1, 1),
            purchase_price=Decimal('1000.00'),
            initial_quantity=Decimal('10.00'),
            current_quantity=Decimal('8.00')
        )
        
        StockLot.objects.create(
            reagent=reagent2,
            lot_number='EQP-B-001',
            location=location2,
            expiry_date=datetime.date(2027, 2, 1),
            purchase_price=Decimal('1500.00'),
            initial_quantity=Decimal('5.00'),
            current_quantity=Decimal('3.00')
        )
        
        # Gerar relatório geral
        total_report = get_stock_value_report()
        expected_total = Decimal('8.00') * Decimal('1000.00') + Decimal('3.00') * Decimal('1500.00')  # 8000 + 4500 = 12500
        assert 'total_value' in total_report
        assert total_report['total_value'] == expected_total
        
        # Gerar relatório agrupado por categoria
        category_report = get_stock_value_report(group_by='category')
        assert len(category_report) == 1
        assert category_report[0]['reagent__category__name'] == 'Equipamentos'
        assert category_report[0]['total_value'] == expected_total
        
        # Gerar relatório agrupado por localização
        location_report = get_stock_value_report(group_by='location')
        assert len(location_report) == 2
        location_values = {item['location__name']: item['total_value'] for item in location_report}
        assert location_values['Laboratório A'] == Decimal('8000.00')
        assert location_values['Laboratório B'] == Decimal('4500.00')

    def test_get_expiry_report(self):
        """Testa o relatório de validade"""
        category = Category.objects.create(name='Reagentes Especiais')
        supplier = Supplier.objects.create(name='Fornecedor Especializado')
        location = Location.objects.create(name='Laboratório Especial')
        reagent = Reagent.objects.create(
            name='Reagente Especial',
            sku='ESP-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('10.00')
        )
        
        today = timezone.now().date()
        
        # Criar lotes com diferentes datas de validade
        expired_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='ESP-EXPIRED',
            location=location,
            expiry_date=today - datetime.timedelta(days=5),  # Expirado
            purchase_price=Decimal('50.00'),
            initial_quantity=Decimal('50.00'),
            current_quantity=Decimal('50.00')
        )
        
        expiring_soon_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='ESP-SOON',
            location=location,
            expiry_date=today + datetime.timedelta(days=15),  # Expira em 15 dias
            purchase_price=Decimal('50.00'),
            initial_quantity=Decimal('30.00'),
            current_quantity=Decimal('30.00')
        )
        
        valid_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='ESP-VALID',
            location=location,
            expiry_date=today + datetime.timedelta(days=180),  # Válido por 180 dias
            purchase_price=Decimal('50.00'),
            initial_quantity=Decimal('20.00'),
            current_quantity=Decimal('20.00')
        )
        
        # Gerar relatório de produtos expirados
        expired_report = get_expiry_report(expired=True)
        assert len(expired_report) == 1
        assert expired_report[0]['lot_number'] == 'ESP-EXPIRED'
        
        # Gerar relatório de produtos que expiram em breve (30 dias)
        soon_report = get_expiry_report(days_until_expiry=30)
        assert len(soon_report) == 1
        assert soon_report[0]['lot_number'] == 'ESP-SOON'
        
        # Gerar relatório geral (produtos válidos)
        all_valid_report = get_expiry_report()
        assert len(all_valid_report) == 2  # Apenas os válidos
        lot_numbers = [item['lot_number'] for item in all_valid_report]
        assert 'ESP-SOON' in lot_numbers
        assert 'ESP-VALID' in lot_numbers
        assert 'ESP-EXPIRED' not in lot_numbers

    def test_calculate_total_stock_value(self):
        """Testa o cálculo do valor total do estoque"""
        category = Category.objects.create(name='Produtos Químicos')
        supplier = Supplier.objects.create(name='Fornecedor Químico')
        location = Location.objects.create(name='Estoque Químico')
        reagent1 = Reagent.objects.create(
            name='Produto Químico A',
            sku='PQA-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        reagent2 = Reagent.objects.create(
            name='Produto Químico B',
            sku='PQB-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        # Criar lotes de estoque
        StockLot.objects.create(
            reagent=reagent1,
            lot_number='PQA-2025',
            location=location,
            expiry_date=datetime.date(2026, 12, 31),
            purchase_price=Decimal('25.00'),
            initial_quantity=Decimal('200.00'),
            current_quantity=Decimal('150.00')
        )
        
        StockLot.objects.create(
            reagent=reagent2,
            lot_number='PQB-2025',
            location=location,
            expiry_date=datetime.date(2026, 12, 31),
            purchase_price=Decimal('30.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('75.00')
        )
        
        # Calcular valor total
        total_value = calculate_total_stock_value()
        expected_value = Decimal('150.00') * Decimal('25.00') + Decimal('75.00') * Decimal('30.00')  # 3750 + 2250 = 6000
        assert total_value == expected_value