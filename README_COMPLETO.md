# 🏗️ Proyecto06 - Arquitectura de 3 Capas en AWS EKS

**Estado**: ✅ Completado | **Versión**: 1.0.0 | **Fecha**: Febrero 2026

Arquitectura **production-ready** de 3 capas (Frontend Angular, Backend FastAPI, PostgreSQL Database) desplegada en **AWS EKS** con **Infrastructure as Code** (Terraform), **CI/CD automático** (GitHub Actions), **Observabilidad** (Prometheus/Grafana) y **AIOps** (K8sGPT).

---

## 📊 Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                   🎨 FRONTEND (Angular 17)                   │
│             Nginx + Static Content + SPA Routing             │
│                  LoadBalancer: puerto 80                     │
└─────────────────────────────────────────────────────────────┘
                        ↓ HTTP REST API
┌─────────────────────────────────────────────────────────────┐
│              🔙 BACKEND (FastAPI + Python 3.11)              │
│      Users API • Products API • Health Check • Docs         │
│                   ClusterIP: puerto 8000                    │
└─────────────────────────────────────────────────────────────┘
                        ↓ SQL Connection
┌─────────────────────────────────────────────────────────────┐
│           🗄️ DATABASE (PostgreSQL 16 + Alpine)              │
│        Users • Products • Audit Logs • Backup Ready         │
│                   Headless: puerto 5432                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Características Principales

### 1️⃣ Frontend Angular
- ✅ Componentes modernos y reutilizables
- ✅ HTTP Client integrado
- ✅ Diseño responsive con CSS avanzado
- ✅ Health checks automáticos
- ✅ Caché de assets (1 año)

### 2️⃣ Backend FastAPI
- ✅ API REST completa con documentación interactiva
- ✅ Endpoints para Users y Products
- ✅ Autenticación y validación con Pydantic
- ✅ Logging integrado
- ✅ CORS habilitado

### 3️⃣ Database PostgreSQL
- ✅ Tablas normalizadas (Users, Products, Audit Logs)
- ✅ Índices para performance
- ✅ Vistas útiles (active_users, available_products)
- ✅ Datos de ejemplo pre-cargados
- ✅ Health checks integrados

### 4️⃣ Infrastructure
- ✅ **Terraform modules**: VPC, EKS, Security avanzada
- ✅ **Kubernetes manifiestos**: Namespace, StatefulSet, Deployments
- ✅ **CI/CD completo**: GitHub Actions para build, push y deploy
- ✅ **Monitoreo**: Prometheus + Grafana (via Helm)
- ✅ **AIOps**: K8sGPT para diagnóstico con IA

---

## 📁 Estructura del Proyecto

```
proyecto06-eks-k8s-aws-terraform-cicd-6/
│
├── 📁 frontend/                    # CAPA 1: Angular SPA
│   ├── Dockerfile                  # Build multistage (Node → Nginx)
│   ├── nginx.conf                  # Config servidor web
│   ├── package.json               # Dependencias npm
│   ├── app.component.ts           # Componente principal
│   ├── app.component.html         # Template
│   ├── app.component.css          # Estilos
│   ├── app.module.ts              # Módulo raíz
│   └── main.ts                    # Entry point
│
├── 📁 backend/                     # CAPA 2: FastAPI
│   ├── Dockerfile                  # Python 3.11 slim
│   ├── requirements.txt           # Deps: fastapi, sqlalchemy, psycopg2
│   ├── main.py                    # Aplicación FastAPI
│   ├── config.py                  # Configuración
│   ├── database.py                # Pool de conexiones
│   ├── models.py                  # Modelos SQLAlchemy
│   └── schemas.py                 # Schemas Pydantic
│
├── 📁 database/                    # CAPA 3: PostgreSQL
│   ├── Dockerfile                  # PostgreSQL 16 Alpine
│   ├── init.sql                   # Schema + datos iniciales
│   └── README.md                  # Documentación BD
│
├── 📁 k8s/                         # Manifiestos Kubernetes
│   ├── 00-namespace.yaml          # Namespace + ConfigMap
│   ├── 01-database.yaml           # StatefulSet + PVC
│   ├── 02-backend.yaml            # Deployment + Service
│   ├── 03-frontend.yaml           # Deployment + LoadBalancer
│   └── k8sgpt.yaml               # Operador de IA
│
├── 📁 terraform/                   # Infrastructure as Code
│   ├── modules/
│   │   ├── eks/                   # Clúster EKS + Node Groups
│   │   ├── security/              # IAM Roles + Policies
│   │   └── vpc/                   # VPC + Subnets + NAT
│   ├── ai-ops.tf                 # K8sGPT config
│   ├── backend.tf                # S3 + DynamoDB
│   ├── main.tf                   # Orquestación
│   ├── monitoring.tf             # Prometheus + Grafana
│   ├── outputs.tf                # Salidas
│   ├── providers.tf              # AWS Provider
│   └── variables.tf              # Variables
│
├── 📁 .github/workflows/           # GitHub Actions CI/CD
│   ├── ci-cd-3capas.yaml         # Build + Push + Deploy 3 servicios
│   ├── destroy-infra-3capas.yaml # Destrucción completa
│   ├── ci-cd.yaml                # (Legacy)
│   └── destroy-infra.yaml        # (Legacy)
│
├── 📋 Documentación
│   ├── README.md                  # Este archivo
│   ├── ARQUITECTURA.md            # Documentación técnica detallada
│   ├── GUIA_DESPLIEGUE.md        # Paso a paso completo
│   └── CHEAT_SHEET.md            # Comandos rápidos
│
├── 🐳 docker-compose.yml          # Desarrollo local
├── 📝 .env.example               # Variables de ejemplo
└── 📄 Otros archivos...
```

---

## 🚀 Despliegue Rápido

### Opción 1: Local con Docker Compose
```bash
docker-compose up -d
# Acceder: http://localhost
```

### Opción 2: AWS EKS Automático
```bash
# 1. Configurar secrets en GitHub
# 2. Hacer push a main
# 3. GitHub Actions automaticamente:
#    - Construye 3 imágenes
#    - Las pushea a ECR
#    - Crea EKS cluster
#    - Despliega servicios
```

### Opción 3: Manual en CLI
```bash
# Configurar
export AWS_ACCOUNT_ID=123456789012
export AWS_REGION=us-east-1

# Construir imágenes
docker build -t proyecto06-frontend ./frontend
docker build -t proyecto06-backend ./backend
docker build -t proyecto06-database ./database

# Push a ECR (ver GUIA_DESPLIEGUE.md)

# Infraestructura
cd terraform && terraform apply -auto-approve && cd ..

# Kubernetes
kubectl apply -f k8s/

# Acceder
kubectl port-forward -n proyecto06 svc/frontend-service 8080:80
# http://localhost:8080
```

---

## 📚 Documentación

| Documento | Propósito |
|-----------|-----------|
| **[ARQUITECTURA.md](ARQUITECTURA.md)** | Explicación detallada de cada capa |
| **[GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)** | Paso a paso completo (local + AWS) |
| **[CHEAT_SHEET.md](CHEAT_SHEET.md)** | Comandos útiles y troubleshooting |

---

## 📦 Stack Tecnológico

### Frontend
```
Angular 17 • Typescript • Nginx • Docker • Kubernetes
```

### Backend
```
FastAPI • Python 3.11 • SQLAlchemy • Uvicorn • Docker
```

### Database
```
PostgreSQL 16 • Alpine • StatefulSet • PersistentVolume
```

### Infrastructure
```
AWS EKS • Terraform • VPC • IAM • ECR • S3 + DynamoDB
```

### Observabilidad
```
Prometheus • Grafana • Helm • K8sGPT • OpenAI
```

### CI/CD
```
GitHub Actions • Docker Registry • Terraform
```

---

## 🔌 Endpoints de la API

### Health & Info
- `GET /` - Info general
- `GET /health` - Health check
- `GET /api/data` - Datos de ejemplo

### Users
- `POST /api/users` - Crear usuario
- `GET /api/users` - Listar usuarios
- `GET /api/users/{id}` - Obtener usuario

### Products
- `POST /api/products` - Crear producto
- `GET /api/products` - Listar productos
- `GET /api/products/{id}` - Obtener producto
- `PUT /api/products/{id}` - Actualizar
- `DELETE /api/products/{id}` - Eliminar (soft delete)

**Documentación**: `http://backend:8000/docs`

---

## ⚙️ Configuración

### Variables de Entorno
```bash
cp .env.example .env
# Editar con tus valores
```

### Credenciales Database
```
Usuario: proyecto06
Contraseña: proyecto06
Base de Datos: proyecto06_db
```

### AWS Credentials
```bash
aws configure
# O variables de entorno: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
```

---

## 🧪 Testing

### Local
```bash
# Health check
curl http://localhost:8000/health

# API data
curl http://localhost:8000/api/data

# Crear usuario
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com"}'
```

### En EKS
```bash
# Port forward
kubectl port-forward -n proyecto06 svc/backend-service 8001:8000

# Test
curl http://localhost:8001/api/users
```

---

## 📊 Monitoreo

### Prometheus
```bash
kubectl port-forward -n monitoring svc/prometheus-community-prometheus 9090:9090
# http://localhost:9090
```

### Grafana
```bash
kubectl port-forward -n monitoring svc/prometheus-community-grafana 3000:80
# http://localhost:3000 (admin/password)
```

### K8sGPT (AIOps)
```bash
kubectl get results -n k8sgpt-operator-system
kubectl exec -n k8sgpt-operator-system -it pod/k8sgpt -- k8sgpt analyze --explain
```

---

## 🧹 Limpieza

### Eliminar todo
```bash
# Vía GitHub Actions (recomendado)
# Actions → Destroy Infraestructura → Run workflow

# O manualmente
kubectl delete namespace proyecto06
cd terraform && terraform destroy -auto-approve && cd ..
```

---

## 🔒 Seguridad

✅ **Implementado**:
- Secrets para credenciales de BD
- RBAC con ServiceAccounts
- Resource limits (CPU/Memory)
- Health checks
- Pod Security Standards
- CORS configurado

📋 **Por implementar**:
- [ ] TLS/HTTPS
- [ ] Network Policies
- [ ] OAuth2/JWT
- [ ] Secrets encriptados
- [ ] RBAC más restrictivo

---

## 🐛 Troubleshooting

### Pod no inicia
```bash
kubectl describe pod <name> -n proyecto06
kubectl logs <name> -n proyecto06
```

### BD no conecta
```bash
kubectl logs -f database-0 -n proyecto06
```

### Backend error 503
```bash
kubectl port-forward -n proyecto06 svc/backend-service 8001:8000
curl http://localhost:8001/health
```

Ver **[CHEAT_SHEET.md](CHEAT_SHEET.md)** para más comandos.

---

## ✨ Próximos Pasos

1. **Testing**: Agregar pytest para backend, Jest para frontend
2. **Autenticación**: Implementar JWT/OAuth2
3. **Logging**: ELK stack (Elasticsearch, Logstash, Kibana)
4. **Backup**: Automated snapshots de RDS
5. **Scaling**: HPA (Pod Autoscaling)
6. **DNS**: Route53 con dominio personalizado
7. **SSL/TLS**: AWS Certificate Manager + ingress
8. **Disaster Recovery**: Multi-region setup

---

## 📞 Soporte

- 📖 Documentación: [ARQUITECTURA.md](ARQUITECTURA.md)
- 🚀 Despliegue: [GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)
- ⚡ Comandos: [CHEAT_SHEET.md](CHEAT_SHEET.md)
- 🐛 Issues: Revisar troubleshooting en documentación

---

## 📜 Licencia

MIT License - 2026

---

**Proyecto06** - CloudCamp Kubernetes & Terraform | ✅ Production Ready | 🚀 Escalable | 🔒 Seguro
