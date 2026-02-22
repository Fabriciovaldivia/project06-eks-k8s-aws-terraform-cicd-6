# PostgreSQL Database para Proyecto06

Este es el servicio de base de datos PostgreSQL para el proyecto.

## Características

- PostgreSQL 16 Alpine (lightweight)
- Usuario: `proyecto06`
- Base de datos: `proyecto06_db`
- Contraseña: `proyecto06` (cambiar en producción)

## Tablas incluidas

- **users**: Almacena información de usuarios
- **products**: Almacena catálogo de productos
- **audit_logs**: Registro de cambios en la base de datos

## Health Check

El contenedor incluye health check automático para verificar que PostgreSQL está en línea.

## Volúmenes

Para persistencia de datos en Kubernetes, se recomienda usar:
```yaml
persistentVolumeClaim:
  claimName: postgres-pvc
```
