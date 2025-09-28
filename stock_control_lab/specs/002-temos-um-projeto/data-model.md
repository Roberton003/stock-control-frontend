# Modelo de Dados

Este documento descreve as principais entidades de dados para a funcionalidade de controle de estoque.

## Entidades

### Produto
Representa um item no inventário.

- **Atributos**:
  - `id`: `integer` (Chave Primária, Auto-incremento)
  - `nome`: `string` (Obrigatório, Máx 255 caracteres)
  - `descricao`: `text` (Opcional)
  - `sku`: `string` (Obrigatório, Único, Máx 100 caracteres) - *SKU (Unidade de Manutenção de Estoque)*
  - `quantidade`: `integer` (Obrigatório, Padrão: 0)
  - `fornecedor`: `string` (Opcional, Máx 255 caracteres)
  - `data_validade`: `date` (Opcional)
  - `created_at`: `datetime` (Auto-gerado na criação)
  - `updated_at`: `datetime` (Auto-gerado na atualização)

### Movimentação de Estoque
Registra a entrada ou saída de um produto do estoque.

- **Atributos**:
  - `id`: `integer` (Chave Primária, Auto-incremento)
  - `produto`: `ForeignKey` para `Produto` (Obrigatório)
  - `quantidade`: `integer` (Obrigatório)
  - `tipo`: `string` (Obrigatório, Escolhas: 'ENTRADA', 'SAIDA')
  - `data`: `datetime` (Auto-gerado, Padrão: Agora)
  - `usuario`: `ForeignKey` para `User` (Obrigatório)

### User (Usuário)
Representa um usuário do sistema com permissões específicas.

- **Atributos**:
  - `id`: `integer` (Chave Primária, Auto-incremento)
  - `username`: `string` (Obrigatório, Único)
  - `password`: `string` (Obrigatório, Hash)
  - `role`: `string` (Obrigatório, Escolhas: 'ADMIN', 'USER')
