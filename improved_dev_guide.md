# Guia de Desenvolvimento Django - Manual de Operações para Agente IA

Este documento serve como um manual completo de operações para o agente de IA, contendo comandos exatos, workflows e procedimentos para desenvolvimento e manutenção de projetos Django.

> **Nota para Agentes de IA:** Como os comandos são executados de forma não-interativa, não é possível "ativar" um ambiente virtual com `source`. Portanto, todos os comandos que dependem do ambiente virtual (como `python`, `pip`, `pytest`) devem ser prefixados com o caminho completo para o executável dentro do `venv`. Exemplo: `projeto_teste_v2/venv/bin/python manage.py migrate`.

## Índice

1. [Pré-requisitos e Ambiente](#pré-requisitos-e-ambiente)
2. [Workflows Principais](#workflows-principais)
   *   [Workflow: Scaffolding Completo de Projeto Django](#workflow-scaffolding-completo-de-projeto-django)
3. [Desenvolvimento](#desenvolvimento)
4. [Qualidade e Testes](#qualidade-e-testes)
5. [Administração](#administração)
6. [Troubleshooting](#troubleshooting)
7. [Referências Rápidas](#referências-rápidas)

---

## Pré-requisitos e Ambiente

### Verificação do Ambiente
```bash
# Use o caminho completo para o executável do venv
projeto_teste_v2/venv/bin/python --version
projeto_teste_v2/venv/bin/pip --version

# Listar dependências instaladas
projeto_teste_v2/venv/bin/pip list
```

### Configuração do Ambiente Virtual
```bash
# Criar ambiente virtual (se ainda não existir)
# Use 'python3' para garantir que a versão 3 do Python seja utilizada.
python3 -m venv projeto_teste_v2/venv
```

### Variáveis de Ambiente
> **IMPORTANTE:** O arquivo `.env` **NUNCA** deve ser commitado. Certifique-se de que ele está no `.gitignore`. Em vez disso, um arquivo `.env.example` com a estrutura das variáveis (mas sem os valores) deve ser mantido no repositório.

---

## Workflows Principais

> **Regra Geral de Execução de Comandos para Agentes:**
> Todos os comandos listados abaixo devem ser executados a partir do **diretório raiz do projeto Django** (ex: `blog_agentes_v2/`).
> Para comandos que utilizam o Python ou ferramentas instaladas no ambiente virtual (`pip`, `django-admin`, `manage.py`, `pytest`, `isort`, `black`, `flake8`, `coverage`), utilize o executável completo do `venv`.
> 
> **Exemplo:** Em vez de `python manage.py migrate`, use `venv/bin/python manage.py migrate`.
> Para comandos que exigem mudar de diretório antes de executar, o `cd` será explicitamente incluído.

### Workflow: Scaffolding Completo de Projeto Django

Este workflow detalha todos os passos para criar um novo projeto Django do zero, configurando o ambiente, as dependências e a estrutura básica de arquivos.

1.  **Crie o Ambiente Virtual:**
    ```bash
    # Use 'python3' para garantir que a versão 3 do Python seja utilizada.
    1.  **Crie o Ambiente Virtual:**
    ```bash
    # Use 'python3' para garantir que a versão 3 do Python seja utilizada.
    python3 -m venv [caminho_para_o_novo_projeto]/venv
    ```
    *Substitua `[caminho_para_o_novo_projeto]` pelo caminho completo onde você deseja criar o diretório do seu projeto. Exemplo: `/media/Arquivos/DjangoPython/toolkits/v2/blog_agentes_v2`*

2.  **Instale o Django no Ambiente Virtual:**
    ```bash
    pip install django
    ```

3.  **Instale o `pip-tools` no Ambiente Virtual:**
    Este pacote é necessário para compilar os arquivos `requirements.in` e `requirements-dev.in`.
    ```bash
    pip install pip-tools
    ```

4.  **Crie o Projeto Django:**
    Use o `django-admin` que agora está disponível dentro do ambiente virtual. O `.` no final do comando garante que o projeto seja criado no diretório atual, evitando pastas aninhadas.
    ```bash
    django-admin startproject [nome_do_projeto] .
    ```
    *Substitua `[nome_do_projeto]` pelo nome desejado para o seu projeto. Exemplo: `django-admin startproject blog_agentes_v2 .`*

5.  **Crie os Arquivos de Dependências:**
    Crie os arquivos `requirements.in` e `requirements-dev.in` na raiz do seu projeto (`[caminho_para_o_novo_projeto]/`).

    **Conteúdo de `requirements.in` (exemplo):**
    ```
    django
    psycopg2-binary
    pillow
    python-decouple
    ```

    **Conteúdo de `requirements-dev.in` (exemplo):**
    ```
    -r requirements.in

    black
    isort
    flake8
    pytest
    pytest-django
    coverage
    django-extensions
    pip-tools
    ```

6.  **Compile os Arquivos de Dependências:**
    ```bash
    pip-compile requirements.in
    pip-compile requirements-dev.in
    ```

7.  **Instale as Dependências:**
    ```bash
    pip-sync requirements-dev.txt
    ```

8.  **Crie o Primeiro App (ex: `blog`):**
    ```bash
    python manage.py startapp blog
    ```

9.  **Crie os Diretórios de Templates e Estáticos:**
    ```bash
    mkdir -p templates
    mkdir -p static
    ```

10. **Configure `settings.py`:**
    Abra o arquivo `[caminho_para_o_novo_projeto]/[nome_do_projeto]/settings.py` e faça as seguintes modificações:

    *   **Adicione `import os` e `from decouple import config` no topo.**
    *   **Modifique `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` para usar `decouple`:**
        ```python
        # SECURITY WARNING: keep the secret key used in production secret!
        SECRET_KEY = config('SECRET_KEY', default='SUA_SECRET_KEY_GERADA_AQUI') # Use a key gerada pelo django-admin
        # SECURITY WARNING: don't run with debug turned on in production!
        DEBUG = config('DEBUG', default=True, cast=bool)

        ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
        ```
    *   **Adicione seus apps a `INSTALLED_APPS`:**
        ```python
        INSTALLED_APPS = [
            # ... apps padrão do Django ...
            'django.contrib.staticfiles',
            # Meus Apps
            'blog', # Adicione o nome do seu app
            'django_extensions', # Adicione se estiver usando
        ]
        ```
    *   **Configure o diretório de templates:**
        ```python
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [BASE_DIR / 'templates'], # Adicione esta linha
                'APP_DIRS': True,
                # ...
            },
        ]
        ```

11. **Configure `urls.py` (nível do projeto):**
    Abra o arquivo `[caminho_para_o_novo_projeto]/[nome_do_projeto]/urls.py` e inclua as URLs do seu app:
    ```python
    from django.contrib import admin
    from django.urls import path, include # Importe 'include'

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('blog/', include('blog.urls')), # Exemplo para o app 'blog'
    ]
    ```

12. **Crie `urls.py` para o seu app (ex: `blog/urls.py`):**
    ```python
    from django.urls import path
    from .views import HomePageView # Exemplo de view inicial

    app_name = 'blog' # Defina o namespace do app

    urlpatterns = [
        path('', HomePageView.as_view(), name='home'),
    ]
    ```

13. **Crie `views.py` para o seu app (ex: `blog/views.py`):**
    ```python
    from django.views.generic import TemplateView

    class HomePageView(TemplateView):
        template_name = "blog/home.html"
    ```

14. **Crie o template inicial para o seu app (ex: `templates/blog/home.html`):**
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Blog Home</title>
    </head>
    <body>
        <h1>Bem-vindo ao Blog!</h1>
        <p>Esta é a página inicial do seu blog.</p>
    </body>
    </html>
    ```

15. **Crie os Arquivos de Configuração de Ambiente:**
    Crie `.env` e `.env.example` na raiz do seu projeto (`[caminho_para_o_novo_projeto]/`).

    **Conteúdo de `.env` (exemplo - substitua a SECRET_KEY):**
    ```
    SECRET_KEY='SUA_SECRET_KEY_GERADA_PELO_DJANGO_ADMIN'
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```

    **Conteúdo de `.env.example`:**
    ```
    SECRET_KEY=
    DEBUG=
    ALLOWED_HOSTS=
    ```

16. **Crie o `.gitignore`:**
    Crie o arquivo `.gitignore` na raiz do seu projeto (`[caminho_para_o_novo_projeto]/`).

    **Conteúdo de `.gitignore` (exemplo):**
    ```
    venv/
    __pycache__/
    .env
    *.sqlite3
    ```

17. **Execute as Migrações Iniciais:**
    ```bash
    python manage.py migrate
    ```
    ```
    *Substitua `[caminho_para_o_novo_projeto]` pelo caminho completo onde você deseja criar o diretório do seu projeto. Exemplo: `/media/Arquivos/DjangoPython/toolkits/v2/blog_agentes_v2`*

2.  **Instale o Django no Ambiente Virtual:**
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/pip install django
    ```

3.  **Instale o `pip-tools` no Ambiente Virtual:**
    Este pacote é necessário para compilar os arquivos `requirements.in` e `requirements-dev.in`.
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/pip install pip-tools
    ```

4.  **Crie o Projeto Django:**
    Use o `django-admin` que agora está disponível dentro do ambiente virtual. O `.` no final do comando garante que o projeto seja criado no diretório atual, evitando pastas aninhadas.
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/django-admin startproject [nome_do_projeto] .
    ```
    *Substitua `[nome_do_projeto]` pelo nome desejado para o seu projeto. Exemplo: `venv/bin/django-admin startproject blog_agentes_v2 .`*

5.  **Crie os Arquivos de Dependências:**
    Crie os arquivos `requirements.in` e `requirements-dev.in` na raiz do seu projeto (`[caminho_para_o_novo_projeto]/`).

    **Conteúdo de `requirements.in` (exemplo):**
    ```
    django
    psycopg2-binary
    pillow
    python-decouple
    ```

    **Conteúdo de `requirements-dev.in` (exemplo):**
    ```
    -r requirements.in

    black
    isort
    flake8
    pytest
    pytest-django
    coverage
    django-extensions
    pip-tools
    ```

6.  **Compile os Arquivos de Dependências:**
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/pip-compile requirements.in
    venv/bin/pip-compile requirements-dev.in
    ```

7.  **Instale as Dependências:**
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/pip-sync requirements-dev.txt
    ```

8.  **Crie o Primeiro App (ex: `blog`):**
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/python manage.py startapp blog
    ```

9.  **Crie os Diretórios de Templates e Estáticos:**
    ```bash
    mkdir -p [caminho_para_o_novo_projeto]/templates
    mkdir -p [caminho_para_o_novo_projeto]/static
    ```

10. **Configure `settings.py`:**
    Abra o arquivo `[caminho_para_o_novo_projeto]/[nome_do_projeto]/settings.py` e faça as seguintes modificações:

    *   **Adicione `import os` e `from decouple import config` no topo.**
    *   **Modifique `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` para usar `decouple`:**
        ```python
        # SECURITY WARNING: keep the secret key used in production secret!
        SECRET_KEY = config('SECRET_KEY', default='SUA_SECRET_KEY_GERADA_AQUI') # Use a key gerada pelo django-admin
        # SECURITY WARNING: don't run with debug turned on in production!
        DEBUG = config('DEBUG', default=True, cast=bool)

        ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
        ```
    *   **Adicione seus apps a `INSTALLED_APPS`:**
        ```python
        INSTALLED_APPS = [
            # ... apps padrão do Django ...
            'django.contrib.staticfiles',
            # Meus Apps
            'blog', # Adicione o nome do seu app
            'django_extensions', # Adicione se estiver usando
        ]
        ```
    *   **Configure o diretório de templates:**
        ```python
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [BASE_DIR / 'templates'], # Adicione esta linha
                'APP_DIRS': True,
                # ...
            },
        ]
        ```

11. **Configure `urls.py` (nível do projeto):**
    Abra o arquivo `[caminho_para_o_novo_projeto]/[nome_do_projeto]/urls.py` e inclua as URLs do seu app:
    ```python
    from django.contrib import admin
    from django.urls import path, include # Importe 'include'

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('blog/', include('blog.urls')), # Exemplo para o app 'blog'
    ]
    ```

12. **Crie `urls.py` para o seu app (ex: `blog/urls.py`):**
    ```python
    from django.urls import path
    from .views import HomePageView # Exemplo de view inicial

    app_name = 'blog' # Defina o namespace do app

    urlpatterns = [
        path('', HomePageView.as_view(), name='home'),
    ]
    ```

13. **Crie `views.py` para o seu app (ex: `blog/views.py`):**
    ```python
    from django.views.generic import TemplateView

    class HomePageView(TemplateView):
        template_name = "blog/home.html"
    ```

14. **Crie o template inicial para o seu app (ex: `templates/blog/home.html`):**
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Blog Home</title>
    </head>
    <body>
        <h1>Bem-vindo ao Blog!</h1>
        <p>Esta é a página inicial do seu blog.</p>
    </body>
    </html>
    ```

15. **Crie os Arquivos de Configuração de Ambiente:**
    Crie `.env` e `.env.example` na raiz do seu projeto (`[caminho_para_o_novo_projeto]/`).

    **Conteúdo de `.env` (exemplo - substitua a SECRET_KEY):**
    ```
    SECRET_KEY='SUA_SECRET_KEY_GERADA_PELO_DJANGO_ADMIN'
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```

    **Conteúdo de `.env.example`:**
    ```
    SECRET_KEY=
    DEBUG=
    ALLOWED_HOSTS=
    ```

16. **Crie o `.gitignore`:**
    Crie o arquivo `.gitignore` na raiz do seu projeto (`[caminho_para_o_novo_projeto]/`).

    **Conteúdo de `.gitignore` (exemplo):**
    ```
    venv/
    __pycache__/
    .env
    *.sqlite3
    ```

17. **Execute as Migrações Iniciais:**
    ```bash
    cd [caminho_para_o_novo_projeto]
    venv/bin/python manage.py migrate
    ```
