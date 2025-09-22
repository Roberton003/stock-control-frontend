# Guia do Usuário: Analista

Este guia fornece instruções detalhadas sobre como usar o Sistema de Controle de Estoque do Laboratório com o papel de **Analista**. Como Analista, você tem acesso total ao sistema e pode gerenciar todos os aspectos do estoque.

## Visão Geral

Como Analista, você pode:
- Gerenciar reagentes, categorias, fornecedores e localizações
- Adicionar lotes ao estoque
- Realizar retiradas de materiais
- Gerenciar requisições de outros usuários
- Visualizar relatórios e dashboards
- Configurar alertas
- Visualizar logs de auditoria

## Gerenciamento de Reagentes

### Adicionar um Novo Reagente

1. Acesse o menu "Reagentes" no painel lateral
2. Clique no botão "Novo Reagente"
3. Preencha os campos obrigatórios:
   - Nome do reagente
   - Código SKU
   - Categoria
   - Fornecedor
   - Nível mínimo de estoque
4. Clique em "Salvar"

### Editar um Reagente Existente

1. Na lista de reagentes, clique no nome do reagente que deseja editar
2. Na página de detalhes, clique no botão "Editar"
3. Faça as alterações necessárias
4. Clique em "Salvar"

### Anexar Documentos (FISPQ/CoA)

1. Na página de detalhes do reagente, role até a seção "Anexos"
2. Clique no botão "Adicionar Anexo"
3. Selecione o arquivo PDF
4. Adicione uma descrição (opcional)
5. Clique em "Salvar"

## Gerenciamento de Estoque

### Adicionar um Novo Lote ao Estoque

1. Acesse o menu "Lotes" no painel lateral
2. Clique no botão "Novo Lote"
3. Preencha os campos obrigatórios:
   - Reagente
   - Número do lote
   - Localização
   - Data de validade
   - Preço de compra
   - Quantidade inicial
4. Clique em "Salvar"

### Realizar uma Retirada de Material

O sistema implementa a política FEFO (First-Expire, First-Out) automaticamente.

1. Acesse o menu "Movimentações" no painel lateral
2. Clique no botão "Nova Retirada"
3. Selecione o reagente
4. Informe a quantidade a ser retirada
5. Adicione observações (opcional)
6. Clique em "Registrar Retirada"

O sistema automaticamente selecionará o lote com a data de validade mais próxima para a retirada.

## Gerenciamento de Requisições

### Aprovar ou Rejeitar Requisições

1. Acesse o menu "Requisições" no painel lateral
2. Na lista de requisições pendentes, clique na requisição que deseja gerenciar
3. Revise os detalhes da requisição
4. Clique em "Aprovar" para autorizar a retirada ou "Rejeitar" para negar

## Visualização de Relatórios e Dashboards

### Dashboard Principal

O dashboard exibe informações importantes em tempo real:
- Valor total do estoque
- Itens com estoque baixo
- Itens próximos da validade
- Gráficos de consumo
- Distribuição de validades

### Relatórios Avançados

1. Acesse o menu "Relatórios" no painel lateral
2. Escolha o tipo de relatório desejado:
   - Consumo por usuário
   - Desperdício/perda
   - Valor do estoque
   - Validades
3. Configure os filtros de data e outros parâmetros
4. Clique em "Gerar Relatório"

## Configuração de Alertas

### Configurar Alertas de Estoque Baixo

1. Acesse o menu "Configurações" no painel lateral
2. Clique em "Alertas"
3. Configure os parâmetros desejados:
   - Nível mínimo de estoque por reagente
   - Frequência de verificação
4. Clique em "Salvar Configurações"

### Configurar Alertas de Validade Próxima

1. Na mesma página de "Alertas"
2. Configure os parâmetros:
   - Número de dias para alerta de validade
   - Frequência de verificação
3. Clique em "Salvar Configurações"

## Visualização de Logs de Auditoria

1. Acesse o menu "Auditoria" no painel lateral
2. Os logs são exibidos em ordem cronológica, com as seguintes informações:
   - Data e hora da ação
   - Usuário que realizou a ação
   - Tipo de ação
   - Detalhes da ação
3. Use os filtros para buscar logs específicos

## Boas Práticas

1. **Mantenha os dados atualizados**: Sempre que houver mudanças no estoque, registre imediatamente no sistema
2. **Verifique as datas de validade**: Preste atenção aos alertas de validade próxima
3. **Avalie as requisições com cuidado**: Antes de aprovar, verifique se há estoque suficiente
4. **Monitore os relatórios**: Use os relatórios para identificar padrões de consumo e oportunidades de otimização
5. **Mantenha os anexos atualizados**: Certifique-se de que todos os reagentes tenham suas FISPQs e CoAs anexadas

## Suporte

Em caso de dúvidas ou problemas, entre em contato com o administrador do sistema.