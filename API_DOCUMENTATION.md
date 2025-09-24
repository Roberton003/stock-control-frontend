# Documentação da API - Stock Control Lab

## Visão Geral

A API do Stock Control Lab fornece endpoints RESTful para gerenciar reagentes, lotes de estoque, movimentações, requisições e outros recursos do sistema de controle de estoque para laboratórios químicos.

**Base URL**: `http://localhost:8000/api/v1/` (durante desenvolvimento)

## Autenticação

A autenticação é feita usando tokens JWT. Para acessar endpoints protegidos, inclua o header:

```
Authorization: Bearer <seu-token-aqui>
```

## Endpoints

### Autenticação

#### `POST /api/v1/login/`
Autentica um usuário e retorna um token de acesso.

**Corpo da requisição:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Resposta:**
```json
{
  "token": "string"
}
```

#### `POST /api/v1/logout/`
Realiza logout do usuário (invalida o token).

**Headers:**
```
Authorization: Bearer <token>
```

### Reagentes

#### `GET /api/v1/reagents/`
Lista todos os reagentes.

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "name": "Ácido Clorídrico",
    "description": "Solução de HCl 37%",
    "category": 1,
    "minimum_stock": 10.0,
    "unit_of_measure": "L",
    "supplier": 1,
    "location": 1,
    "created_at": "2025-09-24T10:00:00Z",
    "updated_at": "2025-09-24T10:00:00Z"
  }
]
```

#### `POST /api/v1/reagents/`
Cria um novo reagente.

**Corpo da requisição:**
```json
{
  "name": "Hidróxido de Sódio",
  "description": "Pallets de NaOH",
  "category": 2,
  "minimum_stock": 5.0,
  "unit_of_measure": "kg",
  "supplier": 1,
  "location": 2
}
```

#### `GET /api/v1/reagents/{id}/`
Obtém detalhes de um reagente específico.

#### `PUT /api/v1/reagents/{id}/`
Atualiza um reagente existente.

#### `DELETE /api/v1/reagents/{id}/`
Exclui um reagente.

### Lotes de Estoque

#### `GET /api/v1/stock-lots/`
Lista todos os lotes de estoque.

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "reagent": 1,
    "lot_number": "L001",
    "location": 1,
    "expiry_date": "2026-12-31",
    "purchase_price": 150.00,
    "initial_quantity": 100.0,
    "current_quantity": 85.0,
    "entry_date": "2025-09-01",
    "qr_code_image": "data:image/png;base64,..."
  }
]
```

#### `POST /api/v1/stock-lots/`
Cria um novo lote de estoque.

**Corpo da requisição:**
```json
{
  "reagent": 1,
  "lot_number": "L002",
  "location": 2,
  "expiry_date": "2027-06-30",
  "purchase_price": 200.00,
  "initial_quantity": 50.0,
  "entry_date": "2025-09-24"
}
```

#### `GET /api/v1/stock-lots/{id}/`
Obtém detalhes de um lote específico.

#### `PUT /api/v1/stock-lots/{id}/`
Atualiza um lote existente.

#### `DELETE /api/v1/stock-lots/{id}/`
Exclui um lote.

### Movimentações de Estoque

#### `GET /api/v1/stock-movements/`
Lista todas as movimentações de estoque.

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "stock_lot": 1,
    "user": 1,
    "quantity": 10.0,
    "move_type": "Entrada",
    "timestamp": "2025-09-24T10:00:00Z",
    "notes": "Recebimento de material"
  }
]
```

#### `POST /api/v1/stock-movements/`
Registra uma nova movimentação de estoque.

**Corpo da requisição:**
```json
{
  "stock_lot": 1,
  "user": 2,
  "quantity": 5.0,
  "move_type": "Retirada",
  "notes": "Utilizado em experimento"
}
```

#### `POST /api/v1/stock-movements/withdraw/`
Registra uma retirada de estoque com validação de quantidade.

**Corpo da requisição:**
```json
{
  "stock_lot": 1,
  "reagent_id": 1,
  "quantity": 5.0,
  "notes": "Retirada para experimento"
}
```

### Requisições

#### `GET /api/v1/requisitions/`
Lista todas as requisições.

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "requester": 1,
    "reagent": 1,
    "quantity": 2.0,
    "status": "pendente",
    "approved_by": null,
    "approved_at": null,
    "created_at": "2025-09-24T10:00:00Z",
    "updated_at": "2025-09-24T10:00:00Z"
  }
]
```

#### `POST /api/v1/requisitions/`
Cria uma nova requisição.

**Corpo da requisição:**
```json
{
  "reagent": 1,
  "quantity": 3.0,
  "notes": "Necessário para experimento X"
}
```

#### `POST /api/v1/requisitions/{id}/action/`
Aprova ou rejeita uma requisição.

**Corpo da requisição:**
```json
{
  "action": "approve" // ou "reject"
}
```

### Categorias

#### `GET /api/v1/categories/`
Lista todas as categorias.

#### `POST /api/v1/categories/`
Cria uma nova categoria.

**Exemplo de corpo:**
```json
{
  "name": "Ácidos",
  "description": "Reagentes ácidos"
}
```

### Fornecedores

#### `GET /api/v1/suppliers/`
Lista todos os fornecedores.

#### `POST /api/v1/suppliers/`
Cria um novo fornecedor.

### Localizações

#### `GET /api/v1/locations/`
Lista todas as localizações.

#### `POST /api/v1/locations/`
Cria uma nova localização.

### Relatórios e Dashboard

#### `GET /api/v1/dashboard/summary/`
Obtém resumo do dashboard com estatísticas do sistema.

**Exemplo de resposta:**
```json
{
  "total_reagents": 25,
  "total_stock_value": 5000.00,
  "low_stock_items": 3,
  "expiring_soon": 5
}
```

#### `GET /api/v1/reports/financial/`
Gera relatório financeiro de estoque.

### Relatórios Específicos

#### `GET /api/v1/reports/consumption-by-user/`
Relatório de consumo por usuário.

#### `GET /api/v1/reports/waste-loss/`
Relatório de perdas/desperdícios.

#### `GET /api/v1/reports/stock-value/`
Relatório de valor de estoque.

#### `GET /api/v1/reports/expiry/`
Relatório de produtos próximos ao vencimento.

## Tipos de Movimentação

- `Entrada`: Adição de estoque
- `Retirada`: Retirada de estoque
- `Descarte`: Descarte de material
- `Ajuste`: Ajuste de quantidade (pode ser positivo ou negativo)

## Status de Requisições

- `pendente`: Requisição aguardando aprovação
- `aprovado`: Requisição aprovada
- `rejeitado`: Requisição rejeitada

## Tratamento de Erros

Erros são retornados com códigos HTTP apropriados e mensagens descritivas:

```json
{
  "error": "Mensagem de erro explicativa",
  "details": {
    "campo": ["Mensagem de erro específica para o campo"]
  }
}
```

## Exemplo de Requisição Completa

```javascript
// Exemplo de requisição para criar um reagente
fetch('http://localhost:8000/api/v1/reagents/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer seu-token-aqui'
  },
  body: JSON.stringify({
    "name": "Sulfato de Cobre",
    "description": "Pó cristalino azul",
    "category": 1,
    "minimum_stock": 2.0,
    "unit_of_measure": "kg",
    "supplier": 1,
    "location": 2
  })
})
.then(response => response.json())
.then(data => console.log(data));
```