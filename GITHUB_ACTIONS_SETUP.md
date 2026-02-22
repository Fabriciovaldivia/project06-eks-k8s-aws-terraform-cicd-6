# ⚙️ Configuración del Pipeline GitHub Actions

## 🎯 Lo que hace el pipeline automáticamente

Cada vez que haces `git push` a `main`, el pipeline:

```
1️⃣ VALIDACIÓN (validate)
   ├─ Valida Dockerfiles
   ├─ Valida manifiestos Kubernetes
   └─ Valida Terraform

2️⃣ BUILD (build)
   ├─ docker build -t proyecto06-database:latest database/
   ├─ docker build -t proyecto06-backend:latest backend/
   └─ docker build -t proyecto06-frontend:latest frontend/

3️⃣ TESTS (test)
   ├─ Tests del backend
   └─ Tests del frontend

4️⃣ PUSH A ECR (push-ecr)
   ├─ Autentica en AWS ECR
   └─ Envía las 3 imágenes a ECR

5️⃣ DEPLOY A KUBERNETES (deploy)
   ├─ Actualiza kubeconfig
   ├─ Aplica manifiestos K8s
   ├─ Espera a que los servicios estén listos
   └─ Verifica que todo funcionó

6️⃣ VERIFICACIÓN FINAL (verify)
   └─ Muestra estado del deployment
```

---

## 📋 Requisitos previos

### 1. Crear rol IAM en AWS

Necesitas un rol que GitHub Actions pueda asumir:

```bash
# 1. En AWS Console o CLI, crear un rol con:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
        "ecr:DescribeImages",
        "ecr:DescribeRepositories",
        "ecr:ListImages",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetLifecyclePolicy",
        "ecr:DescribeLifecyclePolicy",
        "ecr:ListTagsForResource",
        "ecr:DescribeImageScanFindings",
        "ecr-public:GetAuthorizationToken",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:*:ACCOUNT_ID:repository/proyecto06-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "eks:UpdateClusterConfig",
        "eks:DescribeCluster",
        "eks:ListClusters"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🔐 Configurar GitHub Secrets

Este es el **paso más importante**:

### En GitHub:
1. Ve a tu repositorio
2. **Settings** → **Secrets and variables** → **Actions**
3. Haz click en **"New repository secret"**
4. Agrega estos secretos:

| Variable | Valor |
|----------|-------|
| `AWS_ROLE_TO_ASSUME` | `arn:aws:iam::ACCOUNT_ID:role/github-actions-role` |
| `AWS_REGION` | `us-east-1` |

**Ejemplo de AWS_ROLE_TO_ASSUME:**
```
arn:aws:iam::123456789012:role/proyecto06-github-actions
```

---

## 🚀 Cómo funciona

### Flujo automático (sin hacer nada especial):

```bash
# 1. Haz cambios en tu código
git add .
git commit -m "Update proyecto06"

# 2. Push a main
git push origin main

# 3. GitHub Actions se ejecuta automáticamente
#    → Ve a "Actions" en tu repo para ver el progreso
```

### Ver el estado del pipeline:

1. Ve a tu repositorio en GitHub
2. Haz click en **"Actions"**
3. Verás el workflow `🚀 Build & Deploy - Proyecto06` ejecutándose
4. Haz click para ver detalles en tiempo real

---

## 📝 Archivo del workflow

El archivo `.github/workflows/build-deploy.yml` contiene:

- ✅ Validación de Dockerfiles
- ✅ Build con contexto correcto: `context: database/` 
- ✅ Tests automáticos
- ✅ Push a ECR
- ✅ Deploy a EKS
- ✅ Verificación final

**Puntos clave que FIX el error anterior:**

```yaml
strategy:
  matrix:
    service:
      - { name: "database", path: "database" }    # ← Especifica el contexto
      - { name: "backend", path: "backend" }
      - { name: "frontend", path: "frontend" }

uses: docker/build-push-action@v4
with:
  context: ${{ matrix.service.path }}  # ← IMPORTANTE: contexto especificado
  push: false
  tags: proyecto06-${{ matrix.service.name }}:latest
```

---

## ✅ Verificación

Después de hacer `git push`:

1. **En GitHub Actions:**
   - Ver progreso en tiempo real
   - Verificar que cada job complete exitosamente

2. **En AWS ECR:**
   ```bash
   aws ecr describe-images --repository-name proyecto06-database
   aws ecr describe-images --repository-name proyecto06-backend
   aws ecr describe-images --repository-name proyecto06-frontend
   ```

3. **En EKS:**
   ```bash
   kubectl get pods -n proyecto06
   kubectl get svc -n proyecto06
   ```

---

## 🛠️ Troubleshooting

### Error: "AWS credentials not found"
→ Verifica que `AWS_ROLE_TO_ASSUME` esté configurado correctamente en GitHub Secrets

### Error: "ECR repository not found"
→ Crea los repositorios en ECR primero:
```bash
aws ecr create-repository --repository-name proyecto06-database
aws ecr create-repository --repository-name proyecto06-backend
aws ecr create-repository --repository-name proyecto06-frontend
```

### Error: "EKS cluster not found"
→ Verifica que el cluster `proyecto06-eks` exista en AWS:
```bash
aws eks list-clusters --region us-east-1
```

### Error: "init.sql not found"
→ **FIXED** ✓ El workflow ahora especifica el contexto correctamente

---

## 📚 Próximos pasos

1. ✅ Configurar `AWS_ROLE_TO_ASSUME` en GitHub Secrets
2. ✅ Crear repositorios en ECR (si no existen)
3. ✅ Hacer `git push` a `main`
4. ✅ Ver el pipeline ejecutarse en Actions tab

---

## 💡 Comandos útiles

```bash
# Ver logs del workflow localmente (si necesitas debug)
gh workflows list
gh run list
gh run view <run-id>

# Ejecutar manualmente (opción alternativa)
gh workflow run build-deploy.yml
```

---

## 📖 Documentación de referencia

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker build-push-action](https://github.com/docker/build-push-action)
- [AWS ECR Login](https://github.com/aws-actions/amazon-ecr-login)
- [AWS Credentials](https://github.com/aws-actions/configure-aws-credentials)

---

## ✨ Resultado esperado

Después de `git push`:

```
✅ Validación completada
✅ Build database completado  
✅ Build backend completado
✅ Build frontend completado
✅ Tests completados
✅ Push a ECR completado
✅ Deploy a EKS completado
✅ Verificación completada

🎉 Proyecto06 desplegado en EKS automáticamente!
```
