# 🎯 Flujo de Despliegue - Proyecto06

## 1️⃣ FLUJO LOCAL (Docker Compose)

```
┌─────────────────────────────────────────────┐
│         Tu Máquina Local (Windows/Mac/Linux) │
└─────────────────────────────────────────────┘
    ↓
    docker-compose up
    ↓
┌─────────────────────────────────────────────┐
│           DOCKER CONTAINERS                 │
├─────────────────────────────────────────────┤
│ 📦 database-postgres                        │
│    - PostgreSQL 16 Alpine                   │
│    - Port: 5432                             │
│    - Volume: postgres_data/                 │
├─────────────────────────────────────────────┤
│ 📦 backend-fastapi                          │
│    - Python 3.11 + FastAPI                  │
│    - Port: 8000                             │
│    - Connected to: database                 │
├─────────────────────────────────────────────┤
│ 📦 frontend-angular                         │
│    - Node.js + Angular dev server           │
│    - Port: 4200                             │
│    - Connected to: backend                  │
├─────────────────────────────────────────────┤
│ 📦 nginx                                    │
│    - Nginx Alpine                           │
│    - Port: 80                               │
│    - Sirve frontend compilado               │
└─────────────────────────────────────────────┘
    ↓
    Acceso:
    - Frontend: http://localhost:80
    - Backend: http://localhost:8000/docs
    - API: http://localhost:8000/api/*
```

---

## 2️⃣ FLUJO AWS EKS (GitHub Actions)

```
┌──────────────────────────────────┐
│  GitHub Repository (main branch) │
│  └─ push code                    │
└──────────────────┬───────────────┘
                   ↓
            ┌──────────────────┐
            │ GitHub Actions   │
            │ Workflow Trigger │
            └────────┬─────────┘
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
┌──────────────────┐    ┌──────────────────┐
│ Build Images     │    │ Build Images     │
│ - frontend:latest│    │ - backend:latest │
│ - Dockerfile     │    │ - Dockerfile     │
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         ├───────────────┬───────┘
         ↓               ↓
    ┌────────────┬──────────────┐
    │ Build Test │ Build Tests  │
    └────────┬───┴──────────────┘
             ↓
    ┌────────────────────────┐
    │ Login to AWS ECR       │
    │ (123456789012.dkr...) │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────┐
    │ Push Images to ECR     │
    ├────────────────────────┤
    │ proyecto06-frontend    │
    │ proyecto06-backend     │
    │ proyecto06-database    │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────┐
    │ Terraform Init         │
    │ $ terraform init       │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────┐
    │ Terraform Apply        │
    │ $ terraform apply      │
    │                        │
    │ Crea:                  │
    │ - VPC + Subnets        │
    │ - EKS Cluster          │
    │ - Node Groups          │
    │ - IAM Roles            │
    │ - Security Groups      │
    │ - S3 Backend           │
    │ - DynamoDB Lock        │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────┐
    │ Update kubeconfig      │
    │ $ aws eks update-...   │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────┐
    │ Apply K8s Manifests    │
    │                        │
    │ $ kubectl apply -f:    │
    │ 1. namespace.yaml ✓    │
    │ 2. database.yaml       │
    │    [wait 30s]          │
    │ 3. backend.yaml        │
    │    [wait 15s]          │
    │ 4. frontend.yaml       │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────────────┐
    │   AWS EKS CLUSTER              │
    │   (us-east-1)                  │
    ├────────────────────────────────┤
    │ Namespace: proyecto06           │
    │                                 │
    │ 🗄️ StatefulSet: database        │
    │    └─ Pod: database-0           │
    │       Image: proyecto06-db      │
    │       Port: 5432               │
    │       PVC: postgres-pvc (5Gi)  │
    │                                 │
    │ 🔙 Deployment: backend          │
    │    ├─ Pod: backend-XXXXX        │
    │    ├─ Pod: backend-YYYYY        │
    │    └─ Service: ClusterIP:8000  │
    │       Image: proyecto06-backend │
    │                                 │
    │ 🎨 Deployment: frontend         │
    │    ├─ Pod: frontend-AAAAA       │
    │    ├─ Pod: frontend-BBBBB       │
    │    └─ Service: LoadBalancer    │
    │       Image: proyecto06-frontend│
    │                                 │
    │ 📊 Ingress/LB: DNS Público    │
    │    URL: xxx.elb.amazonaws.com  │
    └────────────┬───────────────────┘
                 ↓
    ✅ DEPLOYMENT COMPLETO
    Acceso público: http://[EXTERNAL-IP]
```

---

## 3️⃣ ARQUITECTURA FINAL EN EKS

```
                    INTERNET
                        ↓
            ┌────────────────────────┐
            │  AWS LoadBalancer ALB  │
            │  (Public)              │
            └────────────┬───────────┘
                         ↓
            ┌────────────────────────────┐
            │   EKS Cluster (us-east-1)  │
            │   ┌──────────────────────┐ │
            │   │  AWS VPC (10.0.0/16) │ │
            │   │                      │ │
            │   │ Public Subnets:      │ │
            │   │  - 10.0.0/24         │ │
            │   │  - 10.0.1/24         │ │
            │   │                      │ │
            │   │ Private Subnets:     │ │
            │   │  - 10.0.2/24         │ │
            │   │  - 10.0.3/24         │ │
            │   └──────────┬───────────┘ │
            │              ↓             │
            │   ┌──────────────────────┐ │
            │   │  Namespace: proyecto06 │
            │   │                      │ │
            │   │  ☸️ Worker Node 1    │ │
            │   │    ├─ 🎨 frontend-1 │ │
            │   │    └─ 🔙 backend-1  │ │
            │   │                      │ │
            │   │  ☸️ Worker Node 2    │ │
            │   │    ├─ 🎨 frontend-2 │ │
            │   │    └─ 🔙 backend-2  │ │
            │   │                      │ │
            │   │  ☸️ Worker Node 3    │ │
            │   │    └─ 🗄️ database-0 │ │
            │   │                      │ │
            │   └──────────────────────┘ │
            │                            │
            │   ┌──────────────────────┐ │
            │   │  AWS EBS Storage     │ │
            │   │  └─ PVC: 5Gi        │ │
            │   │     └─ PostgreSQL   │ │
            │   └──────────────────────┘ │
            └────────────────────────────┘
                         ↓
            ┌────────────────────────────┐
            │  AWS ECR Repository        │
            │  (123456789012.dkr...)     │
            │  ├─ proyecto06-frontend    │
            │  ├─ proyecto06-backend     │
            │  └─ proyecto06-database    │
            └────────────────────────────┘
                         ↓
            ┌────────────────────────────┐
            │  AWS S3 Bucket             │
            │  proyecto06-terraform...   │
            │  └─ terraform.tfstate      │
            └────────────────────────────┘
```

---

## 4️⃣ FLUJO DE COMUNICACIÓN

```
User en Navegador (Internet)
    ↓ HTTP Request (port 80)
    ↓
AWS ALB (LoadBalancer)
    ↓ Route to NodePort
    ↓
EKS Node
    ↓
Kubernetes Service (frontend-service:80)
    ↓ Port Forward
    ↓
Frontend Pod (Nginx:80)
    ↓ JavaScript Fetch
    ↓ http://backend-service:8000/api/...
    ↓
Backend Service (backend-service:8000)
    ↓ Load Balance entre replicas
    ↓
Backend Pod 1 (FastAPI:8000)
Backend Pod 2 (FastAPI:8000)
    ↓ Connection String
    ↓ postgresql://proyecto06:@database-service:5432/proyecto06_db
    ↓
Database Service (database-service:5432)
    ↓ Headless Service
    ↓
Database Pod (PostgreSQL:5432)
    ↓ Mount Point
    ↓
PersistentVolume (EBS 5Gi)
    ↓
Data persisted ✅
```

---

## 5️⃣ PIPELINE CI/CD COMPLETO

```
DEVELOPER
    ↓ git push origin main
GitHub Repository
    ↓ Webhook
GitHub Actions
    │
    ├─→ Job: build-and-push
    │   ├─→ Matrix: frontend
    │   │   ├─ docker build
    │   │   ├─ docker tag
    │   │   └─ docker push
    │   │
    │   ├─→ Matrix: backend
    │   │   └─ (same as frontend)
    │   │
    │   └─→ Matrix: database
    │       └─ (same as frontend)
    │
    └─→ Job: deploy-to-eks (needs: build-and-push)
        ├─ Terraform init
        ├─ Terraform apply
        ├─ Update kubeconfig
        ├─ Apply manifests:
        │  ├─ 00-namespace.yaml
        │  ├─ 01-database.yaml [wait]
        │  ├─ 02-backend.yaml [wait]
        │  └─ 03-frontend.yaml [wait]
        └─ Get External IPs ✅

    ↓ Result
PUBLIC URL READY FOR ACCESS
```

---

## 6️⃣ ESCENARIOS DE AUTO-RECUPERACIÓN

```
Scenario 1: Pod Crash (Backend)
┌─────────────────────────┐
│ Backend Pod crashes     │
└────────────┬────────────┘
             ↓
┌─────────────────────────────────┐
│ Kubernetes detects unhealthy   │
│ liveness probe fails            │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ Pod removed, new one scheduled │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ New Pod pulled from ECR        │
│ Started on available node       │
└────────────┬────────────────────┘
             ↓
✅ Service continues with 1 replica
   (otro backend sigue corriendo)

Scenario 2: High Traffic
┌─────────────────────────┐
│ Load increases          │
└────────────┬────────────┘
             ↓
┌─────────────────────────────────┐
│ Pod CPU/Memory usage increases  │
│ HPA would scale (if configured) │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ kubectl scale deployment backend │
│ --replicas=5                     │
└────────────┬────────────────────┘
             ↓
✅ 5 backend pods share load

Scenario 3: Database Failure
┌──────────────────────────────┐
│ Database Pod fails           │
└────────────┬─────────────────┘
             ↓
┌──────────────────────────────────┐
│ StatefulSet ensures Pod restart  │
│ PersistentVolume PERSISTS data   │
└────────────┬─────────────────────┘
             ↓
✅ New Database Pod mounts same PV
   Data is SAFE
```

---

## 7️⃣ ESCALABILIDAD

```
HORIZONTAL SCALING (Más replicas)
┌────────────────────────────────────┐
│ Frontend                           │
│ Replicas: 2 → kubectl scale --replicas=10 │
└────────┬───────────────────────────┘
         ↓
┌────────────────────────────────────┐
│ 10 Frontend Pods                   │
│ Distributed across nodes           │
│ Load balanced by Service           │
└───────────────────────────────────┘

VERTICAL SCALING (Más CPU/Memory)
┌────────────────────────────────────┐
│ Edit Deployment                    │
│ resources.limits.cpu: 1000m        │
│ resources.limits.memory: 1Gi       │
└────────┬───────────────────────────┘
         ↓
┌────────────────────────────────────┐
│ Pods get more resources             │
│ Better performance                 │
└───────────────────────────────────┘
```

---

## 8️⃣ MONITOREO & OBSERVABILIDAD

```
Prometheus (Metrics Collection)
├─ Scrapes metrics from:
│  ├─ backend:8000/metrics
│  ├─ kubelet + kube-state-metrics
│  └─ node-exporter
└─ Stores time-series data (15 days)
    ↓
Grafana (Visualization)
├─ Dashboards:
│  ├─ Cluster Health
│  ├─ Pod Performance
│  ├─ Resource Usage
│  └─ Custom Metrics
└─ Alerts on thresholds ⚠️
    ↓
K8sGPT (AI Analysis)
├─ Analyzes:
│  ├─ Pod errors
│  ├─ CrashLoopBackOff
│  ├─ ImagePullBackOff
│  └─ etc.
└─ Explains with OpenAI 🤖
```

---

## 9️⃣ DESPLIEGUE EXITOSO - CHECKLIST

```
✅ Docker Images Built
   └─ proyecto06-frontend:latest
   └─ proyecto06-backend:latest
   └─ proyecto06-database:latest

✅ Images Pushed to ECR
   └─ 123456789012.dkr.ecr.us-east-1.amazonaws.com/proyecto06-*

✅ Terraform Infrastructure
   └─ VPC, Subnets, NAT created
   └─ EKS Cluster ready
   └─ Node Groups scaled (2-3 nodes)

✅ Kubernetes Deployment
   └─ Namespace proyecto06 created
   └─ Database StatefulSet running (1/1)
   └─ Backend Deployment running (2/2)
   └─ Frontend Deployment running (2/2)

✅ Services Ready
   └─ frontend-service: LoadBalancer (EXTERNAL-IP: xxx.elb.amazonaws.com)
   └─ backend-service: ClusterIP (proyecto06-backend:8000)
   └─ database-service: Headless (database-0.database-service)

✅ Health Checks
   └─ Database readiness: READY (1/1)
   └─ Backend health: /health ✓
   └─ Frontend health: / ✓

✅ Public Access
   └─ Frontend: http://[EXTERNAL-IP]
   └─ Backend Docs: http://backend-service:8000/docs

🎉 DEPLOYMENT READY FOR PRODUCTION
```

---

## 🔟 DESTRUCCIÓN SEGURA

```
User triggers Destroy
    ↓
GitHub Actions Job: destroy
    ↓
1. Delete Kubernetes Services
   (triggers LoadBalancer removal)
    ↓
2. Delete Pod ReplicaSets
   (gracefully terminates pods)
    ↓
3. Delete PersistentVolumeClaim
   (unmounts EBS volume)
    ↓
4. Terraform Destroy
   ├─ EKS Nodes → EC2 removed
   ├─ EKS Cluster → deleted
   ├─ VPC → deleted
   ├─ Subnets → deleted
   ├─ Security Groups → deleted
   └─ IAM Roles → deleted
    ↓
5. ECR Repositories Deleted
   ├─ proyecto06-frontend → deleted
   ├─ proyecto06-backend → deleted
   └─ proyecto06-database → deleted
    ↓
✅ Infrastructure completely removed
⚠️ NOTE: S3 backend and backups may be retained

COST SAVINGS: 0 AWS charges (except S3 backup)
```

---

**Este flujo demuestra una arquitectura enterprise-grade con auto-recuperación, escalabilidad y observabilidad completa.**

¡Listo para producción! 🚀
