# ⚡ Cheat Sheet - Proyecto06

## Comandos Rápidos

### Docker Compose
```bash
# Iniciar
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Rebuild
docker-compose build --no-cache
```

### Kubectl - Ver Recursos
```bash
# Pods
kubectl get pods -n proyecto06
kubectl get pods -n proyecto06 -w  # Watch

# Servicios
kubectl get svc -n proyecto06

# Deployments
kubectl get deployments -n proyecto06

# Logs
kubectl logs -f deployment/frontend -n proyecto06
kubectl logs -f deployment/backend -n proyecto06
kubectl logs -f statefulset/database -n proyecto06

# Describir
kubectl describe pod <name> -n proyecto06
kubectl describe deployment frontend -n proyecto06
```

### Kubectl - Acceder
```bash
# Shell en contenedor
kubectl exec -it deployment/frontend -n proyecto06 -- /bin/sh
kubectl exec -it deployment/backend -n proyecto06 -- /bin/bash
kubectl exec -it database-0 -n proyecto06 -- psql -U proyecto06 -d proyecto06_db

# Port Forward
kubectl port-forward -n proyecto06 svc/frontend-service 8080:80
kubectl port-forward -n proyecto06 svc/backend-service 8001:8000
kubectl port-forward -n proyecto06 svc/database-service 5433:5432
```

### Testing
```bash
# Health Check
curl http://localhost:8000/health

# API Data
curl http://localhost:8000/api/data

# Listar usuarios
curl http://localhost:8000/api/users

# Crear usuario
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com"}'

# Documentación Swagger
# http://localhost:8000/docs
```

### AWS CLI
```bash
# Actualizar kubeconfig
aws eks update-kubeconfig --name proyecto06-eks --region us-east-1

# Listar clusters EKS
aws eks list-clusters --region us-east-1

# Describir cluster
aws eks describe-cluster --name proyecto06-eks --region us-east-1

# Listar repositorios ECR
aws ecr describe-repositories --region us-east-1

# Ver imágenes en ECR
aws ecr list-images --repository-name proyecto06-frontend --region us-east-1
```

### Terraform
```bash
# Inicializar
cd terraform
terraform init

# Validar
terraform validate

# Planificar
terraform plan

# Aplicar
terraform apply -auto-approve

# Destruir
terraform destroy -auto-approve

# Ver outputs
terraform output

# Ver state
terraform state list
```

### Docker
```bash
# Construir imagen
docker build -t proyecto06-frontend:latest ./frontend

# Listar imágenes
docker images | grep proyecto06

# Eliminar imagen
docker rmi proyecto06-frontend:latest

# Login a ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag y push
docker tag proyecto06-frontend:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-frontend:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-frontend:latest
```

### Database
```bash
# Conectar a PostgreSQL
kubectl exec -it database-0 -n proyecto06 -- \
  psql -U proyecto06 -d proyecto06_db

# Ver tablas
SELECT * FROM información_tables WHERE table_schema = 'proyecto06';

# Ver usuarios
SELECT * FROM proyecto06.users;

# Ver productos
SELECT * FROM proyecto06.products;

# Ver logs de auditoría
SELECT * FROM proyecto06.audit_logs;

# Backup
kubectl exec -it database-0 -n proyecto06 -- \
  pg_dump -U proyecto06 proyecto06_db > backup.sql

# Restore
kubectl exec -i database-0 -n proyecto06 -- \
  psql -U proyecto06 proyecto06_db < backup.sql
```

### Scaling
```bash
# Escalar frontend a 5 replicas
kubectl scale deployment frontend --replicas=5 -n proyecto06

# Escalar backend a 3 replicas
kubectl scale deployment backend --replicas=3 -n proyecto06

# Ver réplicas
kubectl get deployment -n proyecto06
```

### Limpieza
```bash
# Eliminar namespace completo
kubectl delete namespace proyecto06

# Eliminar deployment específico
kubectl delete deployment frontend -n proyecto06

# Eliminar pvc (datos)
kubectl delete pvc postgres-pvc -n proyecto06

# Destruir con Terraform
cd terraform && terraform destroy -auto-approve && cd ..
```

### Monitoreo
```bash
# Top de recursos
kubectl top pods -n proyecto06
kubectl top nodes

# Eventos
kubectl get events -n proyecto06

# Describe cluster
kubectl cluster-info

# Validar YAML
kubectl apply --dry-run=client -f k8s/02-backend.yaml
```

### Diagnostico
```bash
# Ver todas las imágenes en uso
kubectl get pods -n proyecto06 -o jsonpath="{.items[*].spec.containers[*].image}"

# Ver variables de entorno
kubectl exec -it deployment/backend -n proyecto06 -- env | grep DATABASE

# Ver volumenes montados
kubectl get pvc -n proyecto06

# Ver eventos de namespace
kubectl get events -n proyecto06 --sort-by='.lastTimestamp'

# Describir PVC
kubectl describe pvc postgres-pvc -n proyecto06
```

---

## Variables de Entorno Clave

```bash
# Backend
DATABASE_URL=postgresql://usuario:pass@host:5432/db
DEBUG=false
API_ENV=production

# Frontend
BACKEND_URL=http://backend-service:8000

# Database
POSTGRES_USER=proyecto06
POSTGRES_PASSWORD=proyecto06
POSTGRES_DB=proyecto06_db
```

---

## Archivos Importantes

- `ARQUITECTURA.md` - Documentación completa
- `GUIA_DESPLIEGUE.md` - Paso a paso detallado
- `docker-compose.yml` - Desarrollo local
- `k8s/*.yaml` - Manifiestos Kubernetes
- `terraform/*.tf` - Configuración infraestructura
- `.github/workflows/ci-cd-3capas.yaml` - Pipeline CI/CD

---

## URLs Importantes

```
Frontend: http://<EXTERNAL-IP>
Backend Swagger: http://localhost:8001/docs (via port-forward)
Backend ReDoc: http://localhost:8001/redoc
Database: localhost:5433 (via port-forward)
Grafana: http://localhost:3000 (si está instalado)
Prometheus: http://localhost:9090 (si está instalado)
```

---

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Pod no inicia | `kubectl describe pod <name> -n proyecto06` |
| No conecta BD | Verif. DATABASE_URL, revisar logs de database-0 |
| Frontend 503 | Verif. backend-service esté disponible |
| ECR sin imágenes | Ver logs del workflow en GitHub Actions |
| Terraform error | `terraform validate` y revisar .tf files |
| Kubectl timeout | Verif. kubeconfig: `kubectl config current-context` |

---

**Tip**: Guardar este archivo y consultarlo frecuentemente durante desarrollo.
