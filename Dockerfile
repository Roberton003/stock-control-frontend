# Dockerfile para o frontend Vue.js
FROM node:18-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o código do projeto
COPY . .

# Build do projeto
RUN npm run build

# Instalar servidor de produção para arquivos estáticos
RUN npm install -g serve

# Expor a porta
EXPOSE 3000

# Comando padrão
CMD ["serve", "-s", "dist", "-l", "3000"]