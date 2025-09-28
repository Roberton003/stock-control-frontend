# Tasks: Sistema Avançado de Controle de Estoque para Laboratório

**Input**: Design documents from `/specs/001-sistema-de-controle/`
**Prerequisites**: plan.md, data-model.md, contracts/api.v1.openapi.yml, quickstart.md

## Phase 3.1: Setup
- [ ] T001 Create Django app `inventory` using `python manage.py startapp inventory`
- [ ] T002 Create Django app `auditing` using `python manage.py startapp auditing`
- [ ] T003 Add `djangorestframework`, `celery`, `redis`, `django-celery-results` to `requirements.txt` and run `pip install -r requirements.txt`
- [ ] T004 Configure `settings.py`: add `inventory`, `auditing`, `rest_framework`, `django_celery_results` to `INSTALLED_APPS`
- [ ] T005 Configure Celery broker URL (Redis) in `config/settings.py` and create `config/celery.py`
- [ ] T006 Include `inventory.urls` and `auditing.urls` in `config/urls.py`

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T007 [P] Contract test for Reagent API in `inventory/tests/test_reagents_api.py` (Covers GET/POST /api/v1/reagents/ and GET/PUT /api/v1/reagents/{id}/)
- [ ] T008 [P] Contract test for Stock Lot API in `inventory/tests/test_stock_lots_api.py` (Covers GET/POST /api/v1/stock-lots/)
- [ ] T009 [P] Contract test for Stock Movement API in `inventory/tests/test_stock_movements_api.py` (Covers POST /api/v1/stock-movements/)
- [ ] T010 [P] Contract test for Dashboard API in `inventory/tests/test_dashboard_api.py` (Covers GET /api/v1/dashboard/summary/)
- [ ] T011 [P] Contract test for Financial Report API in `inventory/tests/test_reports_api.py` (Covers GET /api/v1/reports/financial/)
- [ ] T012 [P] Integration test for FEFO logic in `inventory/tests/test_fefo_logic.py` based on quickstart scenario 4.
- [ ] T013 [P] Integration test for full inventory cycle in `e2e_tests/test_inventory_cycle.py` (add reagent, lot, and withdraw).

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T014 [P] Implement models `Category`, `Supplier`, `Location` in `inventory/models.py`
- [ ] T015 [P] Implement model `Reagent` in `inventory/models.py`
- [ ] T016 [P] Implement model `StockLot` in `inventory/models.py`
- [ ] T017 [P] Implement models `StockMovement`, `Attachment`, `Requisition` in `inventory/models.py`
- [ ] T018 [P] Implement model `AuditLog` in `auditing/models.py`
- [ ] T019 Run `python manage.py makemigrations` and `python manage.py migrate`
- [ ] T020 [P] Implement serializers for all models in `inventory/serializers.py`
- [ ] T021 Implement `ReagentViewSet` in `inventory/views.py`
- [ ] T022 Implement `StockLotViewSet` in `inventory/views.py`
- [ ] T023 Implement `StockMovementService` with FEFO logic in `inventory/services.py`
- [ ] T024 Implement `StockMovementViewSet` in `inventory/views.py` that uses the `StockMovementService`
- [ ] T025 Implement `DashboardSummaryView` in `inventory/views.py`
- [ ] T026 Implement `FinancialReportView` in `inventory/views.py`
- [ ] T027 Define URL patterns in `inventory/urls.py` for all implemented views.

## Phase 3.4: Integration
- [ ] T028 Implement Celery task for low stock/expiry notifications in `inventory/tasks.py`
- [ ] T029 Implement audit log signals in `auditing/signals.py` to automatically create `AuditLog` entries on model changes.
- [ ] T030 [P] Create basic Django admin configurations for all new models in `inventory/admin.py` and `auditing/admin.py`

## Phase 3.5: Polish
- [ ] T031 [P] Write unit tests for the `StockMovementService` FEFO logic in `inventory/tests/test_services.py`
- [ ] T032 [P] Create a simple dashboard template `templates/dashboard.html` to display data from the dashboard summary API.
- [ ] T033 [P] Update API documentation in `docs/api.md` with the new endpoints.
- [ ] T034 Review and refactor code for clarity and performance.

## Dependencies
- Setup (T001-T006) must be done first.
- All Test tasks (T007-T013) must be completed and failing before Core Implementation (T014-T027).
- Models (T014-T018) block Migrations (T019).
- Migrations (T019) block further implementation.
- Models and Serializers (T014-T018, T020) block Views (T021-T026).
- Services (T023) block the dependent View (T024).
- Views (T021-T026) block URL configuration (T027).

## Parallel Example
```
# The following test creation tasks can run in parallel:
Task: "T007 [P] Contract test for Reagent API in inventory/tests/test_reagents_api.py"
Task: "T008 [P] Contract test for Stock Lot API in inventory/tests/test_stock_lots_api.py"
Task: "T009 [P] Contract test for Stock Movement API in inventory/tests/test_stock_movements_api.py"
Task: "T010 [P] Contract test for Dashboard API in inventory/tests/test_dashboard_api.py"
Task: "T011 [P] Contract test for Financial Report API in inventory/tests/test_reports_api.py"

# The following model creation tasks can also run in parallel:
Task: "T014 [P] Implement models Category, Supplier, Location in inventory/models.py"
Task: "T015 [P] Implement model Reagent in inventory/models.py"
# ... and so on for other independent models.
```
