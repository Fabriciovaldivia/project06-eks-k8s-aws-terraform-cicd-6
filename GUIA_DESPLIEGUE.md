# 🚀 Guía Completa de Despliegue - Proyecto06

## Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Configuración Local](#configuración-local)
3. [Despliegue Local con Docker Compose](#despliegue-local-con-docker-compose)
4. [Despliegue en AWS EKS](#despliegue-en-aws-eks)
5. [Verificación y Testing](#verificación-y-testing)
6. [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

### Herramientas necesarias
```bash
# Verificar versiones instaladas
git --version
docker --version
docker-compose --version
node --version
npm --version
python --version

# Herramientas para AWS/K8s
aws --version
terraform -version
kubectl version
```

### Versiones recomendadas
- Docker: >= 24.0
- Docker Compose: >= 2.20
- Node.js: >= 18
- Python: >= 3.11
- AWS CLI: >= 2.13
- Terraform: >= 1.6
- kubectl: >= 1.27

### Credenciales AWS
```bash
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
```

---

## Configuración Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/usuario/proyecto06-eks-k8s.git
cd proyecto06-eks-k8s-aws-terraform-cicd-6
```

### 2. Crear archivo .env
```bash
cp .env.example .env

# Editar .env con tus valores
# - AWS_ACCOUNT_ID: Tu cuenta de AWS
# - AWS_ACCESS_KEY_ID: Tu clave de acceso
# - AWS_SECRET_ACCESS_KEY: Tu clave secreta
```

### 3. Instalar dependencias (si desarrollarás localmente)
```bash
# Frontend
cd frontend
npm install
cd ..

# Backend
cd backend
pip install -r requirements.txt
cd ..
```

---

## Despliegue Local con Docker Compose

### Paso 1: Construir imágenes
```bash
docker-compose build --no-cache
```

### Paso 2: Iniciar servicios
```bash
docker-compose up -d
```

### Paso 3: Verificar estado
```bash
docker-compose ps
# Debería mostrar 4 servicios corriendo: database, backend, frontend, nginx

docker-compose logs -f
```

### Paso 4: Acceder a la aplicación
```
Frontend: http://localhost:80
Backend Swagger: http://localhost:8000/docs
Backend ReDoc: http://localhost:8000/redoc
Database: localhost:5432
```

### Paso 5: Testing local
```bash
# Test Health Check
curl http://localhost:8000/health

# Test API
curl http://localhost:8000/api/data

# Test GET Users
curl http://localhost:8000/api/users

# Test POST Usuario
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@ejemplo.com"}'
```

### Paso 6: Detener servicios
```bash
docker-compose down

# Con limpieza de volúmenes
docker-compose down -v
```

---

## Despliegue en AWS EKS

### Fase 1: Requisitos en AWS

#### 1. Configurar credenciales
```bash
aws configure
# O establecer variables de entorno:
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

#### 2. Crear usuario IAM (si es necesario)
El usuario IAM necesita permisos para:
- EC2, EKS, VPC, ECR, S3, DynamoDB, IAM

Política recomendada: `AdministratorAccess` para testing

#### 3. Crear repositorio S3 (opcional, Terraform lo puede crear)
```bash
aws s3api create-bucket \
  --bucket proyecto06-terraform-state-eks \
  --region us-east-1 \
  --create-bucket-configuration LocationConstraint=us-east-1
```

### Fase 2: Despliegue via GitHub Actions

#### 1. Código en GitHub
```bash
git add .
git commit -m "🚀 Arquitectura de 3 capas lista"
git push origin main
```

#### 2. Configurar Secrets en GitHub
Ve a: Settings → Secrets and variables → Actions

Agregar:
- `AWS_ACCESS_KEY`: Tu clave de acceso IAM
- `AWS_SECRET_KEY`: Tu clave secreta IAM
- `AWS_ACCOUNT_ID`: Tu número de cuenta (ej: 123456789012)

#### 3. Ejecutar workflow
```
GitHub → Actions → 📋 CI-CD-Proyecto06-3Capas → Run workflow
```

El pipeline automaticamente:
1. ✅ Construye 3 imágenes Docker
2. ✅ Las pushea a ECR
3. ✅ Crea el cluster EKS con Terraform
4. ✅ Despliega los 3 servicios en K8s

**Tiempo estimado**: ~15-20 minutos

#### 4. Monitorear progreso
```bash
# En terminal local
aws eks update-kubeconfig --name proyecto06-eks --region us-east-1
kubectl get pods -n proyecto06 -w
```

### Fase 3: Despliegue Manual (Alternativa)

Si prefieres hacerlo manualmente en CLI:

#### 1. Construir imágenes
```bash
ACCOUNT_ID=123456789012
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Frontend
docker build -t proyecto06-frontend ./frontend
docker tag proyecto06-frontend:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-frontend:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-frontend:latest

# Backend
docker build -t proyecto06-backend ./backend
docker tag proyecto06-backend:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-backend:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-backend:latest

# Database
docker build -t proyecto06-database ./database
docker tag proyecto06-database:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-database:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/proyecto06-database:latest
```

#### 2. Aplicar Terraform
```bash
cd terraform

# Inicializar
terraform init

# Planificar
terraform plan

# Aplicar
terraform apply -auto-approve

cd ..
```

#### 3. Conectar a EKS
```bash
aws eks update-kubeconfig --name proyecto06-eks --region us-east-1
```

#### 4. Desplegar manifiestos
```bash
# Reemplazar Account ID
sed -i "s|<ACCOUNT_ID>|$ACCOUNT_ID|g" k8s/*.yaml

# Aplicar en orden
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-database.yaml
sleep 30  # Esperar a que BD esté lista
kubectl apply -f k8s/02-backend.yaml
sleep 15
kubectl apply -f k8s/03-frontend.yaml
```

---

## Verificación y Testing

### 1. Verificar pods
```bash
kubectl get pods -n proyecto06
kubectl get pvc -n proyecto06
kubectl get svc -n proyecto06
```

### 2. Obtener URL de acceso
```bash
# Frontend LoadBalancer
kubectl get svc frontend-service -n proyecto06
# Copiar EXTERNAL-IP y acceder en navegador

# Backend (solo interno)
kubectl port-forward -n proyecto06 svc/backend-service 8001:8000
# http://localhost:8001/docs
```

### 3. Testing de conectividad
```bash
# Test desde pod de frontend
kubectl exec -it deployment/frontend -n proyecto06 -- curl backend-service:8000/health

# Test desde pod de backend
kubectl exec -it deployment/backend -n proyecto06 -- curl database-service:5432 || true

# Conectar a la BD
kubectl exec -it database-0 -n proyecto06 -- \
  psql -U proyecto06 -d proyecto06_db -c "SELECT * FROM proyecto06.users;"
```

### 4. Ver logs
```bash
# Frontend
kubectl logs -f -n proyecto06 deployment/frontend --tail=50

# Backend
kubectl logs -f -n proyecto06 deployment/backend --tail=50

# Database
kubectl logs -f -n proyecto06 statefulset/database --tail=50
```

### 5. Testing de API
```bash
# Port forward
kubectl port-forward -n proyecto06 svc/backend-service 8001:8000

# En otra terminal:
curl http://localhost:8001/api/data
curl http://localhost:8001/api/users
curl -X POST http://localhost:8001/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","description":"Producto test","price":99}'
```

---

## Troubleshooting

### Pod no inicia
```bash
# Ver descripción detallada
kubectl describe pod <pod-name> -n proyecto06

# Ver logs completos
kubectl logs <pod-name> -n proyecto06 --previous
```

### Database no conecta
```bash
# Verificar que database-0 esté corriendo
kubectl get statefulset -n proyecto06

# Test manual de conexión
kubectl port-forward -n proyecto06 svc/database-service 5432:5432
psql -h localhost -U proyecto06 -d proyecto06_db

# Ver logs de BD
kubectl logs -f database-0 -n proyecto06
```

### Backend obtiene error 503
```bash
# Verificar que backend pueda conectar a BD
kubectl exec -it deployment/backend -n proyecto06 -- \
  python -c "from database import get_db; list(get_db())"

# Revisar variable DATABASE_URL
kubectl get deployment backend -n proyecto06 -o yaml | grep DATABASE_URL
```

### Frontend no carga
```bash
# Verificar health check
curl -v http://<EXTERNAL-IP>/health

# Ver configuración Nginx
kubectl exec -it deployment/frontend -n proyecto06 -- cat /etc/nginx/nginx.conf
```

### Problemas de permisos
```bash
# Verificar roles de IAM
aws iam list-user-policies --user-name <tu-usuario>

# Verificar roles de K8s
kubectl get rolebindings -n proyecto06
kubectl get clusterrolebindings | grep proyecto06
```

---

## Limpieza

### Destruir todo via GitHub Actions
1. GitHub → Actions → 🧨 Destroy Infraestructura → Run workflow

O manualmente:
```bash
# Eliminar namespace (borra todos los recursos)
kubectl delete namespace proyecto06

# Destruir infraestructura con Terraform
cd terraform
terraform destroy -auto-approve
cd ..

# Eliminar repositorios ECR
for service in frontend backend database; do
  aws ecr delete-repository \
    --repository-name proyecto06-$service \
    --region us-east-1 \
    --force
done
```

---

## Próximos pasos

- [ ] Implementar CI/CD con pruebas automatizadas
- [ ] Agregar autenticación JWT
- [ ] Implementar logging centralizado (ELK)
- [ ] Agregar HTTPS/TLS
- [ ] Implementar auto-scaling
- [ ] Backup automatizado de BD
- [ ] Alertas por métricas
- [ ] Disaster recovery

---

**¿Preguntas?** Revisar ARQUITECTURA.md para documentación detallada.
