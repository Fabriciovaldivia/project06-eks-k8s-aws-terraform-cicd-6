# 📋 Documentación de Arquitectura - Proyecto06

## 1. FRONTEND (Capa de Presentación)

### Tecnología
- **Angular 17** - Framework frontend moderno
- **Nginx** - Servidor web optimizado para contenedores
- **Docker** - Build multistage (Node.js → Nginx)

### Características
- Componentes Angular reutilizables
- HTTP Client para comunicación con Backend
- Página responsive con CSS moderno
- Health check en `/health`
- Cache de archivos estáticos (1 año)

### Endpoints
- `/` - Página principal
- `/docs` - Documentación Swagger (si aplica)
- `/health` - Health check

### Despliegue en K8s
```bash
kubectl apply -f k8s/03-frontend.yaml
```

**Servicio**: `frontend-service` (LoadBalancer)
**Puerto**: 80
**Replicas**: 2 (con anti-afinidad de pods)

---

## 2. BACKEND (Capa de Lógica de Negocio)

### Tecnología
- **FastAPI** - Framework API moderno y rápido
- **Python 3.11** - Versión reciente y estable
- **SQLAlchemy** - ORM para acceso a BD
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Endpoints Principales

#### Health & Info
- `GET /health` - Verificar servidor en línea
- `GET /` - Info general del API
- `GET /api/data` - Datos de test

#### Users
- `POST /api/users` - Crear usuario
- `GET /api/users` - Listar usuarios
- `GET /api/users/{user_id}` - Obtener usuario

#### Products
- `POST /api/products` - Crear producto
- `GET /api/products` - Listar productos
- `GET /api/products/{product_id}` - Obtener producto
- `PUT /api/products/{product_id}` - Actualizar producto
- `DELETE /api/products/{product_id}` - Eliminar producto (soft delete)

### Variables de Entorno
```bash
DATABASE_URL=postgresql://usuario:password@host:5432/base_datos
DEBUG=false
API_ENV=production
```

### Despliegue en K8s
```bash
kubectl apply -f k8s/02-backend.yaml
```

**Servicio**: `backend-service` (ClusterIP)
**Puerto**: 8000
**Replicas**: 2 (con anti-afinidad de pods)

### Documentación Interactiva
Una vez desplegado, accede a:
- `http://backend-service:8000/docs` (Swagger UI)
- `http://backend-service:8000/redoc` (ReDoc)

---

## 3. DATABASE (Capa de Persistencia)

### Tecnología
- **PostgreSQL 16** - Base de datos SQL robusta
- **Alpine Linux** - Imagen ligera (~170MB)
- **StatefulSet** - Manejo de estado en K8s

### Tablas
- **users** - Información de usuarios
- **products** - Catálogo de productos
- **audit_logs** - Auditoría de cambios

### Inicialización
```sql
-- El script init.sql se ejecuta automáticamente
-- Crea:
-- - Esquema proyecto06
-- - Tablas (users, products, audit_logs)
-- - Índices para performance
-- - Vistas útiles
-- - Datos de ejemplo
```

### Credenciales
```
Usuario: proyecto06
Contraseña: proyecto06 (CAMBIAR EN PRODUCCIÓN)
Base de Datos: proyecto06_db
```

### Despliegue en K8s
```bash
kubectl apply -f k8s/01-database.yaml
```

**Servicio**: `database-service` (Headless ClusterIP)
**Puerto**: 5432
**Almacenamiento**: PersistentVolumeClaim (5Gi)

### Backup & Restore
```bash
# Backup
kubectl exec -it database-0 -n proyecto06 -- \
  pg_dump -U proyecto06 proyecto06_db > backup.sql

# Restore
kubectl exec -i database-0 -n proyecto06 -- \
  psql -U proyecto06 proyecto06_db < backup.sql
```

---

## 4. COMUNICACIÓN ENTRE CAPAS

```
Frontend (Nginx:80)
  ↓ HTTP REST
Backend (FastAPI:8000)
  ↓ SQL/JDBC
Database (PostgreSQL:5432)
```

### URLs Internas
- Frontend → Backend: `http://backend-service:8000/api/...`
- Backend → Database: `postgresql://proyecto06:PASSWORD@database-service:5432/proyecto06_db`

---

## 5. DESPLIEGUE COMPLETO

### Pasos
1. **Build de imágenes**
   ```bash
   docker build -t proyecto06-frontend:latest ./frontend
   docker build -t proyecto06-backend:latest ./backend
   docker build -t proyecto06-database:latest ./database
   ```

2. **Push a ECR**
   ```bash
   # Las imágenes se tagean y pushean automáticamente por el workflow
   ```

3. **Despliegue en EKS**
   ```bash
   # Manualmente en GitHub Actions → "Run workflow" → ci-cd-3capas.yaml
   # O desde CLI:
   kubectl apply -f k8s/00-namespace.yaml
   kubectl apply -f k8s/01-database.yaml
   kubectl apply -f k8s/02-backend.yaml
   kubectl apply -f k8s/03-frontend.yaml
   ```

4. **Verificar estado**
   ```bash
   kubectl get pods -n proyecto06
   kubectl get svc -n proyecto06
   ```

---

## 6. MONITOREO Y OBSERVABILIDAD

### Prometheus
- Métrica del backend: `/metrics`
- Almacenamiento: 15 días

### Grafana
- Dashboard de clúster
- Dashboard de aplicación
- Alertas personalizadas

### K8sGPT
- Análisis automático de errores
- Explicaciones con IA
- Ver: [K8sGPT Documentation](https://docs.k8sgpt.ai/)

---

## 7. ESCALABILIDAD

### Horizontal Scaling
```bash
# Escalar Frontend
kubectl scale deployment frontend -n proyecto06 --replicas=5

# Escalar Backend
kubectl scale deployment backend -n proyecto06 --replicas=3
```

### Vertical Scaling (Recursos)
Editar límites de CPU/Memoria en los manifiestos YAML.

---

## 8. TROUBLESHOOTING

### Ver logs
```bash
# Frontend
kubectl logs -f deployment/frontend -n proyecto06

# Backend
kubectl logs -f deployment/backend -n proyecto06

# Database
kubectl logs -f statefulset/database -n proyecto06
```

### Ejecutar comandos en contenedores
```bash
# En backend
kubectl exec -it deployment/backend -n proyecto06 -- /bin/bash

# En database
kubectl exec -it database-0 -n proyecto06 -- psql -U proyecto06 -d proyecto06_db
```

### Port-forward para debug
```bash
# Frontend
kubectl port-forward -n proyecto06 svc/frontend-service 8080:80

# Backend
kubectl port-forward -n proyecto06 svc/backend-service 8001:8000

# Database
kubectl port-forward -n proyecto06 svc/database-service 5433:5432
```

---

## 9. SEGURIDAD

- ✅ Secrets para credenciales de DB
- ✅ RBAC con ServiceAccounts
- ✅ Resources limits (CPU/Memory)
- ✅ Health checks (liveness & readiness)
- ✅ Pod Security Standards

### Mejorar Seguridad
- [ ] Usar TLS/HTTPS en todos los servicios
- [ ] Agregar Network Policies
- [ ] Implementar autenticación OAuth2/JWT
- [ ] Usar secrets encriptados en Terraform
- [ ] Implementar RBAC más restrictivo

---

## 10. CICLO DE VIDA

### Desarrollo
1. Hacer cambios en el código
2. Pushear a rama main
3. GitHub Actions construye imágenes
4. Pushea a ECR
5. Despliega automáticamente en EKS

### Testing
```bash
# Local
docker-compose up -d

# En EKS (staging)
kubectl apply -f k8s/ -n proyecto06-staging
```

### Destrucción
```bash
# Vía GitHub Actions
# Actions → "Destroy Infraestructura" → Run workflow

# Vía CLI
terraform destroy -auto-approve
```

---

## Documentación Adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Angular Docs](https://angular.io/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
