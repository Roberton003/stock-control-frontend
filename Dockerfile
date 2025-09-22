# Dockerfile para o frontend Vue.js
FROM node:16-alpine

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

# Expor a porta
EXPOSE 3000

# Comando padrão
CMD ["npm", "run", "dev"]