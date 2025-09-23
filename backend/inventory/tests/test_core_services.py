import pytest
from decimal import Decimal
from inventory.models import (
    User, Category, Supplier, Location, Reagent, 
    StockLot, StockMovement, Requisition
)
from inventory.services import (
    get_lots_for_withdrawal, perform_withdrawal, approve_requisition,
    get_stock_value_report, get_expiry_report
)
import datetime
from django.utils import timezone
from freezegun import freeze_time


@pytest.mark.django_db
class TestCoreServices:
    """Testes para as funções principais dos services"""
    
    def test_get_lots_for_withdrawal_feFo_logic(self):
        """Testa a lógica FEFO na função get_lots_for_withdrawal"""
        category = Category.objects.create(name='Ácidos Teste')
        supplier = Supplier.objects.create(name='Fornecedor Teste')
        location = Location.objects.create(name='Armário Teste')
        reagent = Reagent.objects.create(
            name='Ácido Teste',
            sku='ACID-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('100.00')
        )
        
        # Criar múltiplos lotes com diferentes datas de validade
        lot_a = StockLot.objects.create(
            reagent=reagent,
            lot_number='ACID-TEST-A',
            location=location,
            expiry_date=datetime.date(2025, 1, 1),  # Expira primeiro
            purchase_price=Decimal('10.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        lot_b = StockLot.objects.create(
            reagent=reagent,
            lot_number='ACID-TEST-B',
            location=location,
            expiry_date=datetime.date(2025, 6, 1),  # Expira segundo
            purchase_price=Decimal('10.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        lot_c = StockLot.objects.create(
            reagent=reagent,
            lot_number='ACID-TEST-C',
            location=location,
            expiry_date=datetime.date(2026, 1, 1),  # Expira por último
            purchase_price=Decimal('10.00'),
            initial_quantity=Decimal('100.00'),
            current_quantity=Decimal('100.00')
        )
        
        # Testar seleção de lotes com quantidade que pode ser coberta por um lote
        lots_info = get_lots_for_withdrawal(reagent, 50.00)
        
        # Deve selecionar apenas o primeiro lote (FEFO)
        assert len(lots_info) == 1
        assert lots_info[0][0] == lot_a
        assert lots_info[0][1] == Decimal('50.00')
        
        # Testar seleção de lotes com quantidade que requer múltiplos lotes
        lots_info = get_lots_for_withdrawal(reagent, 150.00)
        
        # Deve selecionar os dois primeiros lotes (FEFO)
        assert len(lots_info) == 2
        assert lots_info[0][0] == lot_a
        assert lots_info[0][1] == Decimal('100.00')
        assert lots_info[1][0] == lot_b
        assert lots_info[1][1] == Decimal('50.00')

    def test_get_lots_for_withdrawal_insufficient_stock(self):
        """Testa comportamento quando não há estoque suficiente"""
        category = Category.objects.create(name='Bases Teste')
        supplier = Supplier.objects.create(name='Fornecedor Bases Teste')
        location = Location.objects.create(name='Laboratório B Teste')
        reagent = Reagent.objects.create(
            name='Base Teste',
            sku='BASE-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('50.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='BASE-TEST-001',
            location=location,
            expiry_date=datetime.date(2025, 12, 31),
            purchase_price=Decimal('15.00'),
            initial_quantity=Decimal('75.00'),
            current_quantity=Decimal('75.00')
        )
        
        # Testar solicitação de quantidade maior que o estoque disponível
        with pytest.raises(ValueError, match="Not enough stock"):
            get_lots_for_withdrawal(reagent, 100.00)

    def test_perform_withdrawal_updates_quantities(self):
        """Testa que a função perform_withdrawal atualiza corretamente as quantidades de estoque"""
        category = Category.objects.create(name='Sais Teste')
        supplier = Supplier.objects.create(name='Fornecedor Sais Teste')
        location = Location.objects.create(name='Prateleira C-1 Teste')
        user = User.objects.create_user(username='analista_teste', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Sal Teste',
            sku='SALT-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('200.00')
        )
        
        stock_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='SALT-TEST-2025',
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
        category = Category.objects.create(name='Solventes Teste')
        supplier = Supplier.objects.create(name='Fornecedor Solventes Teste')
        location = Location.objects.create(name='Armário 5 Teste')
        user = User.objects.create_user(username='analista_solventes', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Solvente Teste',
            sku='SOLV-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('500.00')
        )
        
        # Criar dois lotes
        lot_a = StockLot.objects.create(
            reagent=reagent,
            lot_number='SOLV-TEST-A',
            location=location,
            expiry_date=datetime.date(2025, 3, 1),
            purchase_price=Decimal('20.00'),
            initial_quantity=Decimal('300.00'),
            current_quantity=Decimal('300.00')
        )
        lot_b = StockLot.objects.create(
            reagent=reagent,
            lot_number='SOLV-TEST-B',
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

    def test_approve_requisition_success(self):
        """Testa aprovação bem-sucedida de uma requisição"""
        category = Category.objects.create(name='Indicadores Teste')
        supplier = Supplier.objects.create(name='Fornecedor Indicadores Teste')
        location = Location.objects.create(name='Laboratório C Teste')
        requester = User.objects.create_user(username='pesquisador_teste', password='testpass', role='Convidado')
        approver = User.objects.create_user(username='supervisor_teste', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Indicador Teste',
            sku='IND-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('25.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='IND-TEST-2025',
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
        category = Category.objects.create(name='Ácidos Status Inválido')
        supplier = Supplier.objects.create(name='Fornecedor Ácidos Status Inválido')
        requester = User.objects.create_user(username='pesquisador_status', password='testpass', role='Convidado')
        approver = User.objects.create_user(username='supervisor_status', password='testpass', role='Analista')
        reagent = Reagent.objects.create(
            name='Ácido Status Inválido',
            sku='ACID-STATUS-001',
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

    def test_get_stock_value_report_general(self):
        """Testa o relatório de valor do estoque geral"""
        category = Category.objects.create(name='Equipamentos Teste')
        supplier = Supplier.objects.create(name='Fornecedor Equipamentos Teste')
        location1 = Location.objects.create(name='Laboratório A Teste')
        location2 = Location.objects.create(name='Laboratório B Teste')
        reagent1 = Reagent.objects.create(
            name='Equipamento A Teste',
            sku='EQP-A-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('5.00')
        )
        reagent2 = Reagent.objects.create(
            name='Equipamento B Teste',
            sku='EQP-B-TEST-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('3.00')
        )
        
        # Criar lotes de estoque
        StockLot.objects.create(
            reagent=reagent1,
            lot_number='EQP-A-TEST-2025',
            location=location1,
            expiry_date=datetime.date(2027, 1, 1),
            purchase_price=Decimal('1000.00'),
            initial_quantity=Decimal('10.00'),
            current_quantity=Decimal('8.00')
        )
        
        StockLot.objects.create(
            reagent=reagent2,
            lot_number='EQP-B-TEST-2025',
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

    def test_get_stock_value_report_grouped_by_category(self):
        """Testa o relatório de valor do estoque agrupado por categoria"""
        category1 = Category.objects.create(name='Categoria A Teste')
        category2 = Category.objects.create(name='Categoria B Teste')
        supplier = Supplier.objects.create(name='Fornecedor Agrupado Teste')
        location = Location.objects.create(name='Localização Teste')
        reagent1 = Reagent.objects.create(
            name='Reagente Categoria A',
            sku='CAT-A-001',
            category=category1,
            supplier=supplier,
            min_stock_level=Decimal('10.00')
        )
        reagent2 = Reagent.objects.create(
            name='Reagente Categoria B',
            sku='CAT-B-001',
            category=category2,
            supplier=supplier,
            min_stock_level=Decimal('15.00')
        )
        
        # Criar lotes de estoque
        StockLot.objects.create(
            reagent=reagent1,
            lot_number='CAT-A-2025',
            location=location,
            expiry_date=datetime.date(2027, 3, 1),
            purchase_price=Decimal('500.00'),
            initial_quantity=Decimal('20.00'),
            current_quantity=Decimal('15.00')
        )
        
        StockLot.objects.create(
            reagent=reagent2,
            lot_number='CAT-B-2025',
            location=location,
            expiry_date=datetime.date(2027, 4, 1),
            purchase_price=Decimal('750.00'),
            initial_quantity=Decimal('10.00'),
            current_quantity=Decimal('8.00')
        )
        
        # Gerar relatório agrupado por categoria
        category_report = get_stock_value_report(group_by='category')
        assert len(category_report) == 2
        category_values = {item['reagent__category__name']: item['total_value'] for item in category_report}
        assert category_values['Categoria A Teste'] == Decimal('15.00') * Decimal('500.00')  # 7500
        assert category_values['Categoria B Teste'] == Decimal('8.00') * Decimal('750.00')   # 6000

    def test_get_stock_value_report_grouped_by_location(self):
        """Testa o relatório de valor do estoque agrupado por localização"""
        category = Category.objects.create(name='Reagentes Localização')
        supplier = Supplier.objects.create(name='Fornecedor Localização')
        location1 = Location.objects.create(name='Laboratório Alpha')
        location2 = Location.objects.create(name='Laboratório Beta')
        reagent = Reagent.objects.create(
            name='Reagente Localização',
            sku='LOC-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('20.00')
        )
        
        # Criar lotes de estoque em diferentes localizações
        StockLot.objects.create(
            reagent=reagent,
            lot_number='LOC-ALPHA-2025',
            location=location1,
            expiry_date=datetime.date(2027, 5, 1),
            purchase_price=Decimal('250.00'),
            initial_quantity=Decimal('30.00'),
            current_quantity=Decimal('25.00')
        )
        
        StockLot.objects.create(
            reagent=reagent,
            lot_number='LOC-BETA-2025',
            location=location2,
            expiry_date=datetime.date(2027, 6, 1),
            purchase_price=Decimal('250.00'),
            initial_quantity=Decimal('20.00'),
            current_quantity=Decimal('15.00')
        )
        
        # Gerar relatório agrupado por localização
        location_report = get_stock_value_report(group_by='location')
        assert len(location_report) == 2
        location_values = {item['location__name']: item['total_value'] for item in location_report}
        assert location_values['Laboratório Alpha'] == Decimal('25.00') * Decimal('250.00')  # 6250
        assert location_values['Laboratório Beta'] == Decimal('15.00') * Decimal('250.00')   # 3750

    def test_get_expiry_report_future_expiries(self):
        """Testa o relatório de validade para produtos com datas futuras"""
        category = Category.objects.create(name='Reagentes Validade Futura')
        supplier = Supplier.objects.create(name='Fornecedor Validade Futura')
        location = Location.objects.create(name='Laboratório Validade')
        reagent = Reagent.objects.create(
            name='Reagente Validade Futura',
            sku='VAL-FUT-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('10.00')
        )
        
        today = timezone.now().date()
        
        # Criar lotes com diferentes datas de validade futuras
        lot_near = StockLot.objects.create(
            reagent=reagent,
            lot_number='VAL-FUT-NEAR',
            location=location,
            expiry_date=today + datetime.timedelta(days=15),  # Expira em 15 dias
            purchase_price=Decimal('50.00'),
            initial_quantity=Decimal('50.00'),
            current_quantity=Decimal('50.00')
        )
        
        lot_far = StockLot.objects.create(
            reagent=reagent,
            lot_number='VAL-FUT-FAR',
            location=location,
            expiry_date=today + datetime.timedelta(days=180),  # Válido por 180 dias
            purchase_price=Decimal('50.00'),
            initial_quantity=Decimal('30.00'),
            current_quantity=Decimal('20.00')
        )
        
        # Gerar relatório geral (produtos válidos)
        all_valid_report = get_expiry_report()
        assert len(all_valid_report) == 2  # Ambos os lotes válidos
        lot_numbers = [item['lot_number'] for item in all_valid_report]
        assert 'VAL-FUT-NEAR' in lot_numbers
        assert 'VAL-FUT-FAR' in lot_numbers

    def test_get_expiry_report_expired_products(self):
        """Testa o relatório de validade para produtos expirados"""
        category = Category.objects.create(name='Reagentes Expirados')
        supplier = Supplier.objects.create(name='Fornecedor Expirados')
        location = Location.objects.create(name='Laboratório Expirados')
        reagent = Reagent.objects.create(
            name='Reagente Expirado',
            sku='VAL-EXP-001',
            category=category,
            supplier=supplier,
            min_stock_level=Decimal('5.00')
        )
        
        today = timezone.now().date()
        
        # Criar lotes com datas de validade passadas e futuras
        expired_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='VAL-EXP-EXPIRED',
            location=location,
            expiry_date=today - datetime.timedelta(days=5),  # Expirado
            purchase_price=Decimal('40.00'),
            initial_quantity=Decimal('40.00'),
            current_quantity=Decimal('40.00')
        )
        
        valid_lot = StockLot.objects.create(
            reagent=reagent,
            lot_number='VAL-EXP-VALID',
            location=location,
            expiry_date=today + datetime.timedelta(days=90),  # Válido
            purchase_price=Decimal('40.00'),
            initial_quantity=Decimal('60.00'),
            current_quantity=Decimal('50.00')
        )
        
        # Gerar relatório de produtos expirados
        expired_report = get_expiry_report(expired=True)
        assert len(expired_report) == 1
        assert expired_report[0]['lot_number'] == 'VAL-EXP-EXPIRED'
        
        # Gerar relatório geral (apenas produtos válidos)
        all_valid_report = get_expiry_report()
        assert len(all_valid_report) == 1
        assert all_valid_report[0]['lot_number'] == 'VAL-EXP-VALID'