# Guia de Desenvolvimento para Novos Contribuidores - Stock Control Lab

## Bem-vindo ao Projeto!

Obrigado por demonstrar interesse em contribuir para o Stock Control Lab! Este guia irá ajudá-lo a entender o projeto, configurar seu ambiente de desenvolvimento e começar a contribuir de forma eficaz.

## Sobre o Projeto

O Stock Control Lab é um sistema de controle de estoque desenvolvido especificamente para laboratórios químicos. O sistema permite gerenciar reagentes, lotes de estoque, movimentações, requisições e gerar relatórios, tudo com uma interface amigável e funcionalidades robustas.

### Objetivo do Projeto
- Fornecer uma solução eficiente para controle de estoque em laboratórios químicos
- Permitir rastreamento preciso de reagentes, incluindo datas de validade
- Facilitar o processo de requisição e aprovação de materiais
- Gerar relatórios financeiros e estatísticos sobre o estoque

## Tecnologias Utilizadas

### Stack Principal
- **Backend**: Django + Django REST Framework
- **Frontend**: Vue.js 3 com Composition API
- **Bundler**: Vite
- **Estilização**: Tailwind CSS
- **Gerenciamento de Estado**: Pinia
- **Roteamento**: Vue Router
- **Cliente HTTP**: Axios
- **Testes Backend**: Pytest
- **Testes Frontend**: Vitest + Playwright
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL (produção)

### Infraestrutura
- GitHub para controle de versão
- Previsão de Docker para ambiente de produção
- CI/CD com GitHub Actions (planejado)

## Configuração do Ambiente de Desenvolvimento

Siga os passos descritos no arquivo [DEVELOPMENT_ENVIRONMENT_SETUP.md](DEVELOPMENT_ENVIRONMENT_SETUP.md) para configurar seu ambiente de desenvolvimento completo.

## Estrutura do Código

```
stock-control-lab/                 # Diretório raiz do monorepo
├── backend/                       # Código do backend Django
│   ├── config/                    # Configurações do projeto Django
│   ├── inventory/                 # App principal do sistema
│   │   ├── models.py              # Modelos de dados
│   │   ├── views.py               # Views e APIs
│   │   ├── serializers.py         # Serializers para APIs
│   │   ├── services.py            # Lógica de negócio
│   │   ├── urls.py                # Rotas do app
│   │   ├── admin.py               # Interface admin Django
│   │   ├── tests/                 # Testes do backend
│   │   └── migrations/            # Migrações do banco de dados
│   ├── templates/                 # Templates HTML (futuro)
│   ├── static/                    # Arquivos estáticos
│   ├── manage.py                  # Script de gerenciamento Django
│   └── requirements.txt           # Dependências Python
├── src/                           # Código do frontend Vue.js
│   ├── assets/                    # Imagens, fonts, ícones
│   ├── components/                # Componentes reutilizáveis
│   │   ├── layout/                # Header, Sidebar, Footer
│   │   ├── ui/                    # Botões, cards, inputs, tabelas
│   │   └── dashboard/             # Componentes específicos do dashboard
│   ├── views/                     # Telas principais da aplicação
│   ├── services/                  # Integração com a API
│   ├── stores/                    # Gerenciamento de estado (Pinia)
│   ├── router/                    # Configuração de rotas
│   ├── utils/                     # Funções auxiliares
│   └── styles/                    # Estilos globais e temas
├── tests/                         # Testes unitários do frontend
├── e2e_tests/                     # Testes de integração
├── package.json                   # Configuração do frontend
├── README.md                      # Documentação geral
└── CONTRIBUTING.md                # Este arquivo
```

## Padrões de Desenvolvimento

### Backend (Django)

#### Modelos
- Use nomes descritivos para classes e campos
- Adicione docstrings para explicar a finalidade de modelos e métodos complexos
- Utilize métodos manager personalizados quando necessário
- Siga convenções de nomenclatura do Django

#### APIs e Serializers
- Use Django REST Framework para criar APIs RESTful
- Implemente serializers com validação apropriada
- Organize views em classes que herdam de ViewSets ou APIViews
- Use permissões e autenticação conforme necessário

#### Lógica de Negócio
- Mantenha a lógica de negócio nos arquivos `services.py`
- Escreva testes unitários para funções críticas de negócio
- Use docstrings para funções complexas
- Prefira funções puras quando possível

#### Testes
- Escreva testes para todos os endpoints da API
- Teste a lógica de negócios nos services
- Use fixtures para dados de teste
- Mantenha cobertura de testes acima de 80%

### Frontend (Vue.js)

#### Componentes
- Use nomes descritivos e em PascalCase
- Mantenha componentes pequenos e focados em uma única responsabilidade
- Documente props com tipos e validações apropriadas
- Use Composition API para gerenciamento de estado local

#### Serviços de API
- Centralize chamadas à API em arquivos de serviço
- Use o axios configurado em `src/plugins/axios.js`
- Implemente tratamento de erros consistente
- Use tipagem forte (TypeScript futuro) ou JSDoc para funções

#### Gerenciamento de Estado
- Use Pinia para estado global
- Organize stores por domínio de funcionalidade
- Evite estados redundantes
- Use getters para computações derivadas

#### Estilização
- Utilize Tailwind CSS para estilização
- Evite CSS inline
- Crie componentes UI estilizados reutilizáveis
- Siga o sistema de design definido no projeto

#### Testes
- Escreva testes unitários para componentes
- Teste a lógica de negócios nos composables
- Use mocks apropriados para dependências externas
- Mantenha componentes testáveis

## Processo de Contribuição

### 1. Encontrar Trabalho
- Verifique as Issues abertas para encontrar tarefas disponíveis
- Procure por labels como `good first issue`, `help wanted` ou `beginner friendly`
- Comente na issue para informar que está trabalhando nela

### 2. Fork e Clone
```bash
# Faça fork do repositório
# Clone seu fork
git clone https://github.com/seu-usuario/stock-control-lab.git
cd stock-control-lab
```

### 3. Criar Branch
```bash
# Crie uma branch para sua feature ou correção
git checkout -b feature/sua-feature-nova
# ou
git checkout -b fix/correcao-de-bug
```

### 4. Desenvolver
- Siga os padrões de codificação do projeto
- Escreva testes para seu código
- Use commits semânticos (ex: "feat: add user authentication", "fix: resolve issue with date parsing")

### 5. Testar
- Execute os testes antes de enviar
- Verifique se seu código não quebra funcionalidades existentes
- Seja especialmente cuidadoso com testes de backend

### 6. Submeter
```bash
# Envie sua branch
git push origin feature/sua-feature-nova

# Crie um Pull Request no GitHub
```

## Padrões de Git e Commits

### Mensagens de Commit
Use o formato convencional para mensagens de commit:

```
<tipo>(<escopo opcional>): <descrição curta>

[corpo opcional com detalhes]

[rodapé opcional com referências]
```

**Tipos comuns:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, ponto e vírgula faltando, etc.
- `refactor`: Refatoração que não corrige um bug nem adiciona feature
- `test`: Adicionando ou corrigindo testes
- `chore`: Tarefas de manutenção

**Exemplos:**
- `feat(reagents): add reagent search functionality`
- `fix(dashboard): resolve datetime parsing error in summary`
- `docs: update API documentation with new endpoints`

## Padrões de Codificação

### Backend (Python)
- Siga o estilo PEP 8
- Use nomes de variáveis e funções em inglês
- Use type hints para funções e variáveis importantes
- Mantenha linhas com menos de 88 caracteres
- Adicione docstrings para módulos, classes e funções públicas

### Frontend (JavaScript/HTML/CSS)
- Use camelCase para nomes de variáveis e funções
- Use PascalCase para componentes Vue
- Use nomes de arquivos em kebab-case
- Siga o guia de estilo padrão do Vue.js
- Use aspas duplas para props no template Vue
- Use aspas simples para strings em JavaScript

## Testes

### Backend
- Todos os endpoints da API devem ter testes
- Teste cenários positivos e negativos
- Use fixtures para dados de teste consistentes
- Verifique cobertura de código

### Frontend
- Teste componentes com diferentes estados
- Teste interações do usuário
- Teste serviços de API com mocks
- Verifique renderização correta

## Melhores Práticas

### Segurança
- Nunca faça commit de credenciais ou chaves de API
- Valide e sanitize entradas de usuário
- Use permissões adequadas para endpoints
- Siga práticas de segurança do Django e Vue.js

### Performance
- Otimize consultas ao banco de dados (evite N+1 queries)
- Use paginação para listagens grandes
- Otimize chamadas à API no frontend
- Use lazy loading quando apropriado

### Acessibilidade
- Use atributos ARIA apropriados
- Certifique-se de que o sistema é navegável por teclado
- Verifique contraste de cores adequado
- Use labels descritivos para campos de formulário

## Recursos Úteis

### Documentação
- [Documentação da API](API_DOCUMENTATION.md)
- [Documentação do ambiente de desenvolvimento](DEVELOPMENT_ENVIRONMENT_SETUP.md)
- [Documentação do projeto Django](https://docs.djangoproject.com/)
- [Documentação do Vue.js](https://vuejs.org/)

### Ferramentas
- Django REST Framework
- Vue DevTools
- Django Debug Toolbar
- Chrome DevTools

## Primeiros Passos

Se você é novo no projeto, aqui estão alguns passos sugeridos:

1. Configure seu ambiente de desenvolvimento
2. Execute o sistema localmente
3. Explore os endpoints da API
4. Navegue pela interface do frontend
5. Execute os testes existentes
6. Escolha uma issue adequada para iniciantes
7. Implemente a solução
8. Escreva testes para sua implementação
9. Submeta um Pull Request

## Código de Conduta

Por favor, siga nosso [Código de Conduta](CODE_OF_CONDUCT.md) em todas as interações do projeto.

## Precisa de Ajuda?

Se você tiver dúvidas, sinta-se à vontade para:
- Criar uma issue com a tag `question`
- Comentar em issues existentes
- Falar com os mantenedores do projeto

Obrigado por contribuir para o Stock Control Lab!