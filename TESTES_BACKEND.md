# Plano de Testes - Backend Django

## Status Atual
- [x] Testes para models já criados
- [ ] Testes para serializers - PENDENTE
- [ ] Testes para services - PENDENTE  
- [ ] Testes para views/API - PENDENTE
- [ ] Configuração de cobertura de código - PENDENTE

## Objetivo
Alcançar cobertura mínima de 80% em todas as áreas críticas:
- Models: 100%
- Serializers: 80%+
- Services: 80%+
- Views/API: 70%+

## Estrutura de Testes

### 1. Testes de Serializers
Arquivo: `inventory/tests/test_serializers.py`
- Testar serialização de cada model
- Testar desserialização e validação
- Testar campos obrigatórios e opcionais
- Testar relacionamentos entre models

### 2. Testes de Services  
Arquivo: `inventory/tests/test_services.py`
- Testar lógica de negócio crítica (FEFO, alertas, etc.)
- Testar cálculos (valores totais, quantidades, etc.)
- Testar integração com models
- Testar tratamento de erros

### 3. Testes de Views/API
Arquivo: `inventory/tests/test_views.py` (ou expandir `test_api.py`)
- Testar todos os endpoints CRUD
- Testar autenticação e permissões
- Testar validações de entrada
- Testar respostas de erro

### 4. Configuração de Cobertura
Arquivo: `pytest.ini` ou `pyproject.toml`
- Configurar relatórios de cobertura
- Definir limites mínimos
- Excluir arquivos não relevantes

## Priorização

### Fase 1: Serializers (Alta Prioridade)
1. ReagentSerializer
2. StockLotSerializer  
3. StockMovementSerializer
4. RequisitionSerializer
5. UserSerializer
6. CategorySerializer, SupplierSerializer, LocationSerializer
7. AttachmentSerializer, AuditLogSerializer
8. AlertSerializer, NotificationSerializer

### Fase 2: Services (Média-Alta Prioridade)
1. Serviços de movimentação de estoque (FEFO)
2. Serviços de requisições
3. Serviços de relatórios
4. Serviços de alertas
5. Serviços de cálculos

### Fase 3: Views/API (Média Prioridade)
1. Endpoints de reagentes
2. Endpoints de lotes
3. Endpoints de movimentações
4. Endpoints de requisições
5. Endpoints de dashboard e relatórios

## Critérios de Aceitação

### Para cada serializer:
- Testar criação válida
- Testar criação inválida (campos obrigatórios)
- Testar atualização
- Testar validações específicas
- Testar representação (to_representation)

### Para cada service:
- Testar casos de sucesso
- Testar casos de erro
- Testar edge cases
- Testar integração com banco de dados

### Para cada view:
- Testar status codes corretos
- Testar dados retornados
- Testar autenticação
- Testar permissões
- Testar validações

## Ferramentas

- **pytest** - Framework de testes
- **pytest-django** - Integração Django
- **pytest-cov** - Cobertura de código
- **factory-boy** - Criação de dados de teste (se necessário)
- **freezegun** - Mock de datas/horas

## Métricas

- Cobertura total: ≥ 80%
- Testes passando: 100%
- Sem warnings: 100%
- Tempo de execução: < 2 minutos

## Próximos Passos

1. Criar estrutura básica de testes
2. Configurar cobertura de código
3. Começar pelos serializers mais críticos
4. Expandir gradualmente
5. Monitorar métricas