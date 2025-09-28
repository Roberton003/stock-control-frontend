# Quickstart: Testando a API de Controle de Estoque

Este guia fornece exemplos de comandos `curl` para interagir com os principais endpoints da API, simulando os cenários de usuário definidos na especificação.

**Nota**: Assuma que `YOUR_AUTH_TOKEN` é um token de autenticação válido obtido previamente.

## Cenário 1: Adicionar um Novo Reagente e um Lote

### 1.1 Criar uma Categoria
```bash
curl -X POST -H "Authorization: Bearer YOUR_AUTH_TOKEN" -H "Content-Type: application/json" -d '{
  "name": "Ácidos",
  "description": "Ácidos fortes e fracos"
}' http://127.0.0.1:8000/api/v1/categories/
```

### 1.2 Criar um Reagente
```bash
curl -X POST -H "Authorization: Bearer YOUR_AUTH_TOKEN" -H "Content-Type: application/json" -d '{
  "name": "Ácido Sulfúrico",
  "sku": "H2SO4-98P",
  "category": 1, # ID da Categoria criada acima
  "supplier": 1, # ID de um Fornecedor existente
  "storage_conditions": "Armazenar em local ventilado, longe de bases."
}' http://127.0.0.1:8000/api/v1/reagents/
```

### 1.3 Adicionar um Lote ao Estoque (Entrada)
```bash
curl -X POST -H "Authorization: Bearer YOUR_AUTH_TOKEN" -H "Content-Type: application/json" -d '{
  "reagent": 1, # ID do Reagente criado acima
  "lot_number": "A20250917",
  "location": 1, # ID de uma Localização existente
  "expiry_date": "2026-09-17",
  "purchase_price": "150.75",
  "initial_quantity": "1000",
  "current_quantity": "1000"
}' http://127.0.0.1:8000/api/v1/stock-lots/
```

## Cenário 2: Registrar uma Retirada de Material

Este endpoint aplicará a lógica FEFO (First-Expire, First-Out) no backend para determinar de qual lote a retirada será feita.

```bash
curl -X POST -H "Authorization: Bearer YOUR_AUTH_TOKEN" -H "Content-Type: application/json" -d '{
  "reagent_id": 1, # ID do Reagente a ser retirado
  "quantity": "50",
  "move_type": "Retirada",
  "notes": "Para análise de amostra B-12"
}' http://127.0.0.1:8000/api/v1/stock-movements/
```

## Cenário 3: Visualizar o Dashboard

Este endpoint retorna os dados consolidados para os gráficos e alertas da interface.

```bash
curl -X GET -H "Authorization: Bearer YOUR_AUTH_TOKEN" http://127.0.0.1:8000/api/v1/dashboard/summary/
```

## Cenário 4: Gerar Relatório Financeiro

Este endpoint calcula o total gasto em compras no período especificado.

```bash
curl -X GET -H "Authorization: Bearer YOUR_AUTH_TOKEN" "http://127.0.0.1:8000/api/v1/reports/financial/?start_date=2025-01-01&end_date=2025-03-31"
```
