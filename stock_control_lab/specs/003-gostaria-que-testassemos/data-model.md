# Data Model: Testes de Controle de Estoque na Web

**Feature Number**: 003  
**Feature Branch**: `003-gostaria-que-testassemos`  
**Created**: 27 de setembro de 2025

## Overview
Esta documentação descreve os modelos de dados relevantes para testes completos do sistema de controle de estoque, incluindo estrutura, relacionamentos e regras de negócio.

## Core Data Models

### 1. Reagent (Reagente/Item de Estoque)
- **Descrição**: Representa um item no sistema de controle de estoque
- **Campos**:
  - `id` (Integer): Identificador único (auto-incrementado)
  - `name` (String, max 200): Nome do reagente
  - `description` (Text, optional): Descrição detalhada do reagente
  - `sku` (String, max 100): Código SKU do reagente
  - `category` (String, max 100): Categoria do reagente
  - `location` (String, max 200): Localização física do reagente
  - `quantity` (Integer): Quantidade atual em estoque
  - `min_quantity` (Integer): Quantidade mínima antes de alerta
  - `unit` (String, max 50): Unidade de medida (ml, g, kg, etc.)
  - `supplier` (String, max 200): Fornecedor do reagente
  - `purchase_date` (Date): Data de compra do reagente
  - `expiration_date` (Date, optional): Data de expiração (se aplicável)
  - `batch_number` (String, max 100): Número do lote
  - `storage_conditions` (String, max 500): Condições especiais de armazenamento
  - `created_at` (DateTime): Timestamp de criação
  - `updated_at` (DateTime): Timestamp da última atualização
  - `is_active` (Boolean): Status de ativação do item

### 2. Stock Movement (Movimentação de Estoque)
- **Descrição**: Representa uma movimentação de entrada ou saída de estoque
- **Campos**:
  - `id` (Integer): Identificador único (auto-incrementado)
  - `reagent` (ForeignKey para Reagent): Referência ao reagente movimentado
  - `movement_type` (Enum): Tipo da movimentação ('entry', 'withdrawal')
  - `quantity` (Integer): Quantidade movimentada
  - `movement_date` (DateTime): Data e hora da movimentação
  - `responsible_user` (ForeignKey para User): Usuário responsável pela movimentação
  - `reason` (String, max 500): Motivo da movimentação
  - `notes` (Text, optional): Notas adicionais sobre a movimentação
  - `created_at` (DateTime): Timestamp de criação
  - `updated_at` (DateTime): Timestamp da última atualização

### 3. User (Usuário)
- **Descrição**: Representa um usuário do sistema com permissões específicas
- **Campos**:
  - `id` (Integer): Identificador único (auto-incrementado)
  - `username` (String, max 150): Nome de usuário
  - `email` (String, max 254): Endereço de email
  - `first_name` (String, max 150): Primeiro nome
  - `last_name` (String, max 150): Último nome
  - `role` (String, max 100): Papel do usuário (analyst, admin, guest)
  - `department` (String, max 100): Departamento do usuário
  - `is_active` (Boolean): Status do usuário
  - `date_joined` (DateTime): Data de cadastro
  - `last_login` (DateTime): Último login (opcional)

### 4. Category (Categoria)
- **Descrição**: Categorização de reagentes para organização
- **Campos**:
  - `id` (Integer): Identificador único (auto-incrementado)
  - `name` (String, max 100): Nome da categoria
  - `description` (Text, optional): Descrição da categoria
  - `color_hex` (String, max 7): Código hexadecimal para cor de identificação
  - `created_at` (DateTime): Timestamp de criação
  - `updated_at` (DateTime): Timestamp da última atualização

### 5. Location (Localização)
- **Descrição**: Localização física onde os reagentes são armazenados
- **Campos**:
  - `id` (Integer): Identificador único (auto-incrementado)
  - `name` (String, max 200): Nome da localização
  - `description` (Text, optional): Descrição da localização
  - `building` (String, max 100): Nome do prédio
  - `floor` (String, max 50): Andar
  - `room_number` (String, max 50): Número da sala
  - `is_active` (Boolean): Status da localização
  - `created_at` (DateTime): Timestamp de criação
  - `updated_at` (DateTime): Timestamp da última atualização

### 6. Audit Log (Registro de Auditoria)
- **Descrição**: Histórico de todas as alterações realizadas no sistema
- **Campos**:
  - `id` (Integer): Identificador único (auto-incrementado)
  - `action_user` (ForeignKey para User): Usuário que realizou a ação
  - `action_type` (String, max 50): Tipo de ação (create, update, delete)
  - `target_model` (String, max 100): Modelo afetado pela ação
  - `target_id` (Integer): ID do objeto afetado
  - `old_values` (JSON, optional): Valores anteriores (se aplicável)
  - `new_values` (JSON, optional): Novos valores (se aplicável)
  - `timestamp` (DateTime): Momento da ação
  - `notes` (Text, optional): Notas adicionais sobre a ação

## Relationships

### Reagent
- Possui relacionamento com `Category` (muitos para um)
- Possui relacionamento com `Location` (muitos para um)
- Possui relacionamento com `User` (criador)
- Tem muitas `StockMovement` (um para muitos)

### Stock Movement
- Possui relacionamento com `Reagent` (muitos para um)
- Possui relacionamento com `User` (muitos para um)

### User
- Pode ter muitas `StockMovement` (um para muitos)
- Pode ter muitos `AuditLog` (um para muitos)

## Business Rules

### 1. Regras de Estoque
- A quantidade em estoque nunca pode ser negativa
- Alerta é gerado quando a quantidade atinge o valor mínimo configurado
- A data de expiração, quando definida, não pode ser anterior à data atual

### 2. Regras de Movimentação
- Toda movimentação de saída deve ter quantidade suficiente em estoque
- Movimentações de saída devem ter um motivo justificado
- Movimentações não podem ser feitas em itens desativados

### 3. Regras de Reagente
- O nome do reagente deve ser único dentro do sistema
- O SKU deve ser único (se definido)
- Reagentes desativados não aparecem em listagens regulares

## Validation Constraints

### Reagent Model
- `name`: Obrigatório, máximo de 200 caracteres
- `quantity`: Inteiro não negativo
- `min_quantity`: Inteiro não negativo, deve ser menor ou igual a quantidade atual
- `expiration_date`: Se informado, deve ser posterior à data de compra

### Stock Movement Model
- `movement_type`: Deve ser 'entry' ou 'withdrawal'
- `quantity`: Inteiro positivo
- `reason`: Obrigatório para movimentações de saída
- `movement_date`: Não pode ser uma data futura

## Test Scenarios Based on Data Model

### 1. Reagente Creation (Criação de Reagente)
- Validar criação com todos os campos obrigatórios
- Validar regras de unicidade (nome, SKU)
- Validar regras de validação (datas, quantidades)

### 2. Movimentação de Estoque
- Validar movimentação de entrada aumentando estoque
- Validar movimentação de saída reduzindo estoque
- Validar que saída não excede quantidade disponível
- Validar geração de alerta quando quantidade atinge mínimo

### 3. Auditoria
- Validar registro de todas as operações no log de auditoria
- Validar informações corretas no log (usuário, ação, dados)