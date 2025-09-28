# Feature Specification: Sistema Avançado de Controle de Estoque para Laboratório

**Feature Branch**: `001-sistema-de-controle`  
**Created**: 2025-09-17  
**Status**: Final Draft  
**Input**: User description: "Sistema de controle de estoques para produtos químicos e reagentes, com múltiplas linhas de produto, controle de validade, papéis de usuário, funcionalidades financeiras e de rastreabilidade completa."

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
Como **Gestor de Laboratório (Analista)**, eu quero um sistema completo para gerenciar o ciclo de vida dos reagentes, desde a compra até o descarte, incluindo rastreabilidade de lotes, localização física, controle de validade, documentação (FISPQ/CoA), e análise financeira, para garantir conformidade, segurança, eficiência operacional e otimização de custos.

### Acceptance Scenarios
1.  **Given** que um Analista cadastra um novo lote de "Ácido Sulfúrico" com validade para 90 dias, **When** ele salva o formulário, **Then** o sistema deve gerar uma etiqueta com QR Code para o lote e registrar a `localização` e o `preço de compra` no log de auditoria.
2.  **Given** que existem dois lotes do mesmo reagente (Lote A vence em 30 dias, Lote B em 90), **When** um usuário faz uma requisição de material, **Then** o sistema deve aprovar a retirada e indicar que o Lote A deve ser utilizado (política FEFO).
3.  **Given** que um usuário "Convidado" está logado, **When** ele tenta acessar a URL para editar um produto, **Then** o sistema deve bloqueá-lo e registrar a tentativa de acesso não autorizado no log de auditoria.
4.  **Given** que o sistema processou várias compras e consumos, **When** um Gestor acessa o dashboard financeiro, **Then** ele deve conseguir visualizar o valor total do estoque atual e o total gasto em reagentes no último trimestre.
5.  **Given** que um Analista anexa o PDF da FISPQ a um reagente, **When** qualquer usuário visualiza os detalhes daquele reagente, **Then** ele deve encontrar um link para baixar a FISPQ.

### Edge Cases
- Como o sistema lida com o descarte de um produto vencido? (Deve haver uma ação de "Descartar" que zera o estoque do lote e registra no log de auditoria).
- O que acontece se um lote for perdido/contaminado? (Deve haver uma ação de "Ajuste de Estoque" que requer aprovação ou assinatura eletrônica).
- Como o sistema lida com um QR Code que não é reconhecido? (Deve permitir a busca manual do lote).

---

## Requirements *(mandatory)*

### Functional Requirements

#### Gestão de Itens e Estoque
- **FR-001**: O sistema DEVE permitir a gestão de **Categorias** (ex: "Químicos", "Reagentes").
- **FR-002**: O sistema DEVE permitir a gestão de **Reagentes**, associados a uma Categoria e com campos para anexos (FISPQ, CoA).
- **FR-003**: O sistema DEVE permitir a gestão de **Localizações Físicas** (ex: "Prateleira A-3").
- **FR-004**: O sistema DEVE permitir o registro de **Lotes de Estoque** para cada reagente, com `número de lote`, `data de validade`, `quantidade inicial`, `preço de compra` e `localização`.
- **FR-005**: O sistema DEVE implementar uma política de retirada **"Primeiro a Vencer, Primeiro a Sair" (FEFO)**.
- **FR-006**: O sistema DEVE gerar um **QR Code** único para cada lote para facilitar a movimentação.

#### Papéis e Permissões
- **FR-007**: O sistema DEVE definir os seguintes papéis de usuário:
    - **Analista**: Acesso total de gestão.
    - **Convidado**: Acesso somente para visualização.
- **FR-008**: O sistema DEVE implementar um fluxo de **Requisição de Materiais**, onde um usuário solicita e um Analista aprova a retirada.

#### Inteligência e Relatórios
- **FR-009**: O sistema DEVE fornecer um **dashboard visual** com gráficos de níveis de estoque, consumo, validades próximas e valor total do estoque.
- **FR-010**: O sistema DEVE permitir a configuração de **alertas** para estoque baixo e validade próxima.
- **FR-011**: O sistema DEVE gerar **relatórios avançados**: consumo por usuário, taxa de desperdício e gastos por período.
- **FR-012**: O sistema DEVE **estimar o consumo futuro** e **sugerir cronogramas de compra**.

#### Rastreabilidade e Financeiro
- **FR-013**: O sistema DEVE manter um **Log de Auditoria** imutável para todas as ações críticas.
- **FR-014**: O sistema DEVE calcular e exibir o **valor total do estoque** com base no preço de compra de cada lote.

### Key Entities *(include if feature involves data)*
- **Categoria**: Linha do produto (ex: "Químicos").
- **Localização**: Local físico no laboratório (ex: "Geladeira 2").
- **Reagente**: O tipo de produto. Atributos: nome, SKU, categoria (FK), fornecedor (FK), anexos.
- **Lote de Estoque**: Remessa específica de um Reagente. Atributos: reagente (FK), lote, validade, quantidade, localização (FK), preço de compra.
- **Fornecedor**: Quem fornece os reagentes.
- **Movimentação**: Transação de estoque. Atributos: lote (FK), quantidade, tipo, data, usuário.
- **Requisição**: Pedido de material. Atributos: requisitante (FK), reagente (FK), quantidade, status, aprovador (FK).
- **Usuário**: Usuário do sistema. Atributos: nome, email, papel ('Analista' ou 'Convidado').
- **Log de Auditoria**: Registro de ações. Atributos: usuário (FK), ação, detalhes, data/hora.
- **Anexo**: Documento associado a um Reagente/Lote. Atributos: arquivo, descrição.

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [X] No implementation details
- [X] Focused on user value
- [X] Written for non-technical stakeholders
- [X] All mandatory sections completed

### Requirement Completeness
- [X] No [NEEDS CLARIFICATION] markers remain
- [X] Requirements are testable and unambiguous  
- [X] Success criteria are measurable
- [X] Scope is clearly bounded
- [X] Dependencies and assumptions identified

---
