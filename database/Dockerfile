FROM postgres:16-alpine

ENV POSTGRES_USER=proyecto06
ENV POSTGRES_PASSWORD=proyecto06
ENV POSTGRES_DB=proyecto06_db

# Copiar script de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD pg_isready -U proyecto06 -d proyecto06_db

EXPOSE 5432
