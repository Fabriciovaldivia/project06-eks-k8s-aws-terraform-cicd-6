# Stage 1: Build Angular application
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar dependency files
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Construir aplicación
RUN npm run build

# Stage 2: Servidor Nginx para servir la app
FROM nginx:alpine

# Copiar configuración nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar archivos compilados desde stage 1
COPY --from=builder /app/dist/proyecto06-frontend /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
