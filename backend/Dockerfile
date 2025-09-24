# Dockerfile para o backend Django
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        postgresql-client \\
        build-essential \\
        libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY ./backend/requirements.txt /app/requirements.txt

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY ./backend /app

# Criar diretório para arquivos estáticos
RUN mkdir -p /app/staticfiles

# Coletar arquivos estáticos (necessário para produção)
RUN python manage.py collectstatic --noinput

# Expor a porta
EXPOSE 8000

# Comando padrão
CMD [\"gunicorn\", \"config.wsgi:application\", \"--bind\", \"0.0.0.0:8000\"]