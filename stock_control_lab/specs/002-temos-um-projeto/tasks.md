# Tasks: Finalizar Projeto de Controle de Estoque

**Feature**: Finalizar um projeto de controle de estoque existente, garantindo que ele funcione localmente com uma interface web.

## Seção 1: Configuração do Ambiente

- [X] **T001**: Configurar o ambiente de desenvolvimento do backend.
  - **Arquivo**: `README.md` (para referência), `requirements.txt`
  - **Descrição**: Crie e ative um ambiente virtual Python. Instale todas as dependências do backend listadas em `requirements.txt` usando `pip install -r requirements.txt`.
  - **Depende de**: N/A

- [X] **T002**: Configurar o ambiente de desenvolvimento do frontend.
  - **Arquivo**: `stock-control-lab/package.json`
  - **Descrição**: Navegue até o diretório `stock-control-lab` e instale todas as dependências do Node.js usando `npm install`.
  - **Depende de**: N/A

- [X] **T003**: Configurar o banco de dados inicial.
  - **Arquivo**: `manage.py`
  - **Descrição**: Execute as migrações do Django para criar as tabelas do banco de dados com o comando `python manage.py migrate`.
  - **Depende de**: T001

## Seção 2: Desenvolvimento do Backend (Django)

### Sub-seção 2.1: Modelos e Lógica de Negócio

- [X] **T004** [P]: Implementar o modelo `User`.
  - **Arquivo**: `inventory/models.py`
  - **Descrição**: Crie o modelo `User` conforme especificado em `data-model.md`, incluindo os campos `username`, `password` e `role`.
  - **Depende de**: T003

- [X] **T005** [P]: Implementar o modelo `Produto`.
  - **Arquivo**: `inventory/models.py`
  - **Descrição**: Crie o modelo `Produto` conforme especificado em `data-model.md`, incluindo os campos `nome`, `descricao`, `sku`, `quantidade`, `fornecedor` e `data_validade`.
  - **Depende de**: T003

- [X] **T006**: Implementar o modelo `MovimentacaoEstoque`.
  - **Arquivo**: `inventory/models.py`
  - **Descrição**: Crie o modelo `MovimentacaoEstoque` conforme especificado em `data-model.md`, com chaves estrangeiras para `Produto` and `User`.
  - **Depende de**: T004, T005

- [X] **T007**: Escrever testes para os modelos.
  - **Arquivo**: `inventory/tests/test_models.py`
  - **Descrição**: Crie testes unitários para validar os modelos `Produto`, `MovimentacaoEstoque` e `User`, incluindo validações de campo e relacionamentos.
  - **Depende de**: T006

### Sub-seção 2.2: API (Django REST Framework)

- [X] **T008** [P]: Criar serializers para os modelos.
  - **Arquivo**: `inventory/serializers.py`
  - **Descrição**: Implemente serializers do DRF para os modelos `Produto`, `MovimentacaoEstoque` e `User`.
  - **Depende de**: T006

- [X] **T009**: Implementar os endpoints da API para `Produto`.
  - **Arquivo**: `inventory/views.py`
  - **Descrição**: Crie as `ViewSets` do DRF para as operações de CRUD da entidade `Produto`, conforme definido em `contracts/openapi.json`.
  - **Depende de**: T008

- [X] **T010**: Implementar os endpoints da API para `MovimentacaoEstoque`.
  - **Arquivo**: `inventory/views.py`
  - **Descrição**: Crie as `ViewSets` do DRF para as operações de listagem e criação de `MovimentacaoEstoque`.
  - **Depende de**: T008

- [X] **T011**: Configurar as URLs da API.
  - **Arquivo**: `inventory/urls.py` e `config/urls.py`
  - **Descrição**: Registre as `ViewSets` no roteador do DRF para expor os endpoints da API.
  - **Depende de**: T009, T010

- [X] **T012**: Escrever testes para a API.
  - **Arquivo**: `inventory/tests/test_api.py`
  - **Descrição**: Crie testes de integração para os endpoints da API, cobrindo as operações de CRUD, validação de entrada e autenticação/permissão.
  - **Depende de**: T011

## Seção 3: Desenvolvimento do Frontend (Vue.js)

### Sub-seção 3.1: Serviços e Gerenciamento de Estado

- **T013** [P]: Configurar o serviço da API.
  - **Arquivo**: `stock-control-lab/src/services/api.js`
  - **Descrição**: Crie um cliente Axios para se comunicar com o backend Django. Configure a URL base e os interceptors necessários.
  - **Depende de**: T011

- **T014**: Implementar o store Pinia para `Produto`.
  - **Arquivo**: `stock-control-lab/src/stores/productStore.js`
  - **Descrição**: Crie um store Pinia para gerenciar o estado dos produtos, incluindo actions para buscar, criar, atualizar e deletar produtos através do serviço da API.
  - **Depende de**: T013

### Sub-seção 3.2: Componentes e UI

- **T015**: Criar componente `ProductList`.
  - **Arquivo**: `stock-control-lab/src/components/ProductList.vue`
  - **Descrição**: Desenvolva um componente para listar os produtos, consumindo os dados do `productStore`.
  - **Depende de**: T014

- **T016**: Criar componente `ProductForm`.
  - **Arquivo**: `stock-control-lab/src/components/ProductForm.vue`
  - **Descrição**: Desenvolva um formulário para criar e editar produtos, utilizando o `productStore` para persistir as alterações.
  - **Depende de**: T014

- **T017**: Desenvolver a página principal de Produtos.
  - **Arquivo**: `stock-control-lab/src/views/ProductsView.vue`
  - **Descrição**: Crie a página que integra os componentes `ProductList` e `ProductForm` para fornecer a funcionalidade completa de gerenciamento de produtos.
  - **Depende de**: T015, T016

- **T018**: Escrever testes para os componentes Vue.
  - **Arquivo**: `stock-control-lab/tests/unit/`
  - **Descrição**: Crie testes unitários para os componentes `ProductList` e `ProductForm` usando Vitest e Vue Test Utils.
  - **Depende de**: T017

## Seção 4: Integração e Finalização

- **T019**: Teste de integração End-to-End (E2E).
  - **Arquivo**: `stock-control-lab/tests/e2e/`
  - **Descrição**: Crie um teste E2E com Playwright que simule o fluxo completo do usuário: login, visualização da lista de produtos, adição de um novo produto e verificação se ele aparece na lista.
  - **Depende de**: T012, T018

- **T020**: Documentação final.
  - **Arquivo**: `README.md`, `docs/`
  - **Descrição**: Atualize o `README.md` com as instruções finais de setup e execução. Crie ou atualize a documentação do usuário e da API na pasta `docs/`.
  - **Depende de**: T019

## Execução Paralela

As seguintes tarefas podem ser executadas em paralelo para acelerar o desenvolvimento:

- **Backend Core (após T003)**:
  - `/implement T004`
  - `/implement T005`

- **API e Frontend Services (após T006 e T008)**:
  - `/implement T009`
  - `/implement T010`
  - `/implement T013`

- **Componentes de UI (após T014)**:
  - `/implement T015`
  - `/implement T016`
