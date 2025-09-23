# 📖 Guia de Desenvolvimento para Novos Contribuidores

## 🎯 **Objetivo**
Este guia tem como objetivo ajudar novos contribuidores a entenderem a estrutura do projeto, configurarem seus ambientes de desenvolvimento e começarem a contribuir com o Stock Control Lab.

## 📋 **Índice**
1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Execução do Projeto](#execução-do-projeto)
5. [Estratégia de Branches](#estratégia-de-branches)
6. [Fluxo de Trabalho](#fluxo-de-trabalho)
7. [Padrões de Codificação](#padrões-de-codificação)
8. [Testes](#testes)
9. [Documentação](#documentação)
10. [Pull Requests](#pull-requests)

## 🏗️ **Estrutura do Projeto**

```
stock-control-lab/
├── backend/             # Código do backend Django
│   ├── config/          # Configurações do projeto
│   ├── inventory/       # App principal com modelos e APIs
│   ├── static/          # Arquivos estáticos
│   ├── manage.py        # Script de gerenciamento do Django
│   └── requirements.txt # Dependências do backend
├── src/                 # Código do frontend Vue.js
│   ├── assets/          # Imagens, fonts, ícones
│   ├── components/      # Componentes reutilizáveis
│   ├── views/           # Telas principais da aplicação
│   ├── services/        # Integração com a API
│   ├── stores/          # Gerenciamento de estado (Pinia)
│   ├── router/          # Configuração de rotas
│   ├── utils/           # Funções auxiliares
│   └── styles/          # Estilos globais e temas
├── tests/               # Testes end-to-end
├── e2e_tests/           # Testes de integração frontend/backend
├── docker-compose.yml   # Configuração do Docker Compose (planejado)
└── README.md            # Documentação geral
```

## ⚙️ **Pré-requisitos**

Antes de começar, certifique-se de ter instalado:

- **Node.js** >= 16.x
- **Python** >= 3.8
- **Git**
- **Docker e Docker Compose** (opcional, para produção)
- **Editor de código** (VS Code recomendado)

## 🛠️ **Configuração do Ambiente**

### Backend (Django)

```bash
# Navegue para o diretório do backend
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações do banco de dados
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser
```

### Frontend (Vue.js)

```bash
# Na raiz do projeto, instale as dependências
npm install
```

## ▶️ **Execução do Projeto**

### Backend

```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
# venv\Scripts\activate    # Windows

# Inicie o servidor Django
python manage.py runserver
```

O backend estará disponível em `http://localhost:8000`

### Frontend

```bash
# Na raiz do projeto
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

## 🌿 **Estratégia de Branches**

Seguimos uma estratégia de branches baseada no GitFlow:

- `master` - Branch principal, contém código pronto para produção
- `develop` - Branch de desenvolvimento, contém código em desenvolvimento
- `feature/*` - Branches para desenvolvimento de novas funcionalidades
- `bugfix/*` - Branches para correção de bugs
- `hotfix/*` - Branches para correções urgentes em produção
- `release/*` - Branches para preparação de releases

## 🔄 **Fluxo de Trabalho**

1. **Fork do repositório**
2. **Clone seu fork**
3. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```
4. **Desenvolva sua feature**
5. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "Adicionar nova feature"
   ```
6. **Push para sua branch**
   ```bash
   git push origin feature/nome-da-sua-feature
   ```
7. **Abra um Pull Request**

## 💻 **Padrões de Codificação**

### Backend (Python/Django)

- Seguimos o PEP 8 para estilo de código Python
- Usamos type hints quando possível
- Nomes de variáveis e funções em snake_case
- Nomes de classes em PascalCase
- Docstrings para todas as funções e classes

### Frontend (Vue.js/JavaScript)

- Seguimos o ESLint com regras padrão
- Usamos componentes Vue 3 com Composition API
- Nomes de componentes em PascalCase
- Nomes de variáveis e funções em camelCase
- Props devem ser tipadas quando possível

## 🧪 **Testes**

### Backend

```bash
# Execute todos os testes
cd backend
python -m pytest

# Execute testes específicos
python -m pytest inventory/tests/test_models.py
```

### Frontend

```bash
# Execute testes unitários
npm test

# Execute testes end-to-end
npm run test:e2e
```

### Cobertura de Testes

- Backend: > 80%
- Frontend: > 70%

## 📚 **Documentação**

Sempre que adicionar ou modificar funcionalidades:

1. **Atualize a documentação da API** em `backend/inventory/docs/api.md`
2. **Adicione comentários no código** para explicar decisões importantes
3. **Atualize o README.md** se necessário
4. **Crie documentação para novas funcionalidades**

## 📥 **Pull Requests**

### Checklist Antes de Abrir um PR

- [ ] Todos os testes estão passando
- [ ] A cobertura de testes é adequada
- [ ] O código segue os padrões de codificação
- [ ] A documentação foi atualizada
- [ ] Commits estão bem descritos e organizados
- [ ] Branch está atualizada com a develop

### Template de PR

```markdown
## Descrição
Breve descrição do que foi implementado ou corrigido.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação
- [ ] Outro

## Como Testar
Passos para testar as mudanças:
1. ...
2. ...
3. ...

## Screenshots (se relevante)
...

## Checklist
- [ ] Testes unitários adicionados/modificados
- [ ] Documentação atualizada
- [ ] Commits bem descritos
```

## 🤝 **Comunidade**

- Participe das discussões no GitHub Issues
- Siga o código de conduta do projeto
- Seja respeitoso com outros contribuidores
- Ajude outros contribuidores quando possível

## 🎉 **Bem-vindo!**

Obrigado por contribuir com o Stock Control Lab! Sua ajuda é muito importante para o crescimento e melhoria do projeto.