# 🚀 Project05: Despliegue Automático en AWS EKS con Terraform y GitHub Actions

Este proyecto es una evolución de la arquitectura anterior, reutilizando la base de red y cómputo para implementar capacidades avanzadas de **Observabilidad** y **AIOps**. Despliega una aplicación web (Flask) en AWS EKS utilizando **Terraform** para la infraestructura y los servicios de monitoreo (Helm), y **GitHub Actions** para el CI/CD.

---

## 📐 Diseño Lógico

El flujo de trabajo automatizado sigue estos pasos:

1.  **Código:** El desarrollador sube cambios a la rama `main` en GitHub.
2.  **CI (Integración Continua):**
    *   GitHub Actions construye la imagen Docker de la aplicación.
    *   Se sube la imagen a **Amazon ECR** (Elastic Container Registry).
3.  **IaC (Infraestructura):**
    *   GitHub Actions ejecuta **Terraform**.
    *   Terraform provisiona la red (VPC, Subnets, NAT Gateway) y el clúster **EKS**.
    *   **Terraform (Helm)** despliega automáticamente el stack de monitoreo (**Prometheus/Grafana**) y el operador de IA (**K8sGPT** con **Ollama**).
    *   El estado de Terraform se guarda en **S3** y se bloquea con **DynamoDB**.
4.  **CD (Despliegue Continuo):**
    *   Se actualizan los manifiestos de Kubernetes con el ID de la cuenta AWS.
    *   Se despliega la aplicación en los nodos del clúster EKS.
    *   Se expone la aplicación mediante un **Load Balancer**.

---

## 📂 Estructura del Proyecto

```text
project05-eks-k8s-aws-terraform-cicd-4/
├── .github/workflows/
│   ├── ci-cd.yaml          # Pipeline de CI/CD (Build, Provision, Deploy)
│   └── destroy-infra.yaml  # Pipeline manual para destrucción de recursos
├── app/
│   ├── Dockerfile          # Definición de la imagen del contenedor
│   ├── app.py              # Código principal de la aplicación Flask
│   └── requirements.txt    # Dependencias de Python
├── k8s/
│   ├── deployment.yaml     # Definición del Deployment (Pods y Réplicas)
│   └── service.yaml        # Definición del Service (LoadBalancer)
├── terraform/
│   ├── modules/
│   │   ├── eks/
│   │   │   ├── main.tf     # Recursos del clúster EKS, IAM Roles, Node Groups
│   │   │   ├── outputs.tf  # Salidas del módulo (Endpoint, Cluster Name)
│   │   │   └── variables.tf # Variables de entrada (VPC ID, Subnets)
│   │   └── vpc/
│   │       ├── main.tf     # Recursos de red (VPC, Subnets, IGW, NAT, Routes)
│   │       ├── outputs.tf  # Salidas del módulo (VPC ID, Subnet IDs)
│   │       └── variables.tf # Variables de entrada (CIDR, Name)
│   ├── backend.tf          # Configuración del backend S3 y DynamoDB (Locking)
│   ├── monitoring.tf       # Configuración de Prometheus y Grafana (Helm)
│   ├── ai-ops.tf           # Configuración del Operador de IA (K8sGPT)
│   ├── main.tf             # Orquestación de módulos (Root Module)
│   ├── outputs.tf          # Salidas principales del proyecto
│   └── variables.tf        # Variables globales (Región, Nombre del proyecto)
└── README.md               # Documentación del proyecto
```

---

## 🛠️ Tecnologías y Conceptos Clave

| Tecnología | Descripción | Uso en el proyecto |
| :--- | :--- | :--- |
| **AWS EKS** | Elastic Kubernetes Service | Orquestador donde corren los contenedores de la app. |
| **Terraform** | Infraestructura como Código | Crea la VPC, el Clúster y los Nodos automáticamente. |
| **Docker** | Contenedorización | Empaqueta la aplicación Flask para que corra igual en todos lados. |
| **Amazon ECR** | Elastic Container Registry | Almacena las imágenes Docker privadas de la aplicación. |
| **GitHub Actions** | CI/CD | Automatiza todo el proceso desde el `git push` hasta el despliegue. |
| **S3 + DynamoDB** | Backend Remoto | Guarda el "estado" de la infraestructura para evitar conflictos. |
| **Prometheus + Grafana** | Monitoreo | Recolección de métricas y visualización de dashboards del clúster. |
| **K8sGPT + OpenAI** | AIOps | Escanea el clúster y usa `gpt-4o-mini` para diagnosticar errores y proponer soluciones. |

---

## ⚙️ Configuración Previa (Requisitos)

Para que este proyecto funcione en tu cuenta, debes configurar los **Secretos** en tu repositorio de GitHub:

Ve a: `Settings` > `Secrets and variables` > `Actions` > `New repository secret`.

1.  **`AWS_ACCESS_KEY`**: Tu ID de clave de acceso (IAM).
2.  **`AWS_SECRET_KEY`**: Tu clave secreta de acceso (IAM).
3.  **`AWS_ACCOUNT_ID`**: Tu número de cuenta de AWS (ej. `123456789012`).

> **Nota:** El usuario IAM debe tener permisos de Administrador o permisos suficientes para crear VPCs, EKS, ECR, S3 y DynamoDB.

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Despliegue Automático
Simplemente haz un cambio en el código y súbelo a la rama principal:

```bash
git add .
git commit -m "Desplegando nueva versión"
git push origin main
```

Ve a la pestaña **Actions** en GitHub y verás el flujo `CI-CD-EKS` ejecutándose. Este proceso:
1.  Creará el repositorio ECR (si no existe).
2.  Creará el Bucket S3 y la tabla DynamoDB para Terraform (si no existen).
3.  Creará el Clúster EKS (tarda aprox. 15 min).
4.  Desplegará la aplicación.

### 2. Validación del Despliegue
Una vez finalizado el pipeline, verifica que la aplicación esté corriendo.

**Desde tu terminal local (requiere AWS CLI y Kubectl configurados):**

1.  **Conectarse al clúster:**
    ```bash
    aws eks update-kubeconfig --region us-east-1 --name project05-eks
    ```

2.  **Verificar Nodos:**
    ```bash
    kubectl get nodes
    # Deberías ver los nodos en estado "Ready"
    ```

3.  **Obtener la URL de la aplicación:**
    ```bash
    kubectl get svc
    ```
    Copia la dirección que aparece bajo **EXTERNAL-IP** (ej. `a184...us-east-1.elb.amazonaws.com`) y pégala en tu navegador.

### 3. Acceso a Grafana (Monitoreo)
Para acceder al dashboard de Grafana:

1.  **Obtén la contraseña del usuario `admin`:**

    *   **En Linux/macOS (o Git Bash en Windows):**
        ```bash
        kubectl get secret --namespace monitoring prometheus-community-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
        ```
    *   **En Windows (PowerShell):**
        ```powershell
        $secret = kubectl get secret --namespace monitoring prometheus-community-grafana -o jsonpath='{.data.admin-password}'
        [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($secret))
        ```

2.  **Crea un túnel de acceso (port-forwarding):**
    *Mantén esta terminal abierta mientras usas Grafana.*
    ```bash
    kubectl port-forward --namespace monitoring svc/prometheus-community-grafana 3000:80
    ```
3.  **Entra al dashboard:**
    Abre en tu navegador: `http://localhost:3000` (Usuario: `admin`, Contraseña: la que obtuviste en el paso 1).

### 4. Acceso a Prometheus (Métricas)
Para acceder directamente a la interfaz de Prometheus y hacer consultas:

1.  **Crea un túnel de acceso:**
    ```bash
    kubectl port-forward --namespace monitoring svc/prometheus-community-prometheus 9090:9090
    ```
2.  **Entra a la interfaz:**
    Abre en tu navegador: `http://localhost:9090`

### 5. Diagnóstico con IA (K8sGPT + OpenAI)
Hemos configurado K8sGPT para usar el backend de **OpenAI** con el modelo `gpt-4o-mini`, lo que proporciona análisis rápidos y precisos.

**Flujo de Validación:**

1.  **Crear el Secreto de OpenAI:**
    K8sGPT necesita tu API Key para funcionar. Ejecuta este comando sustituyendo `<TU_API_KEY>`:
    ```bash
    kubectl create secret generic openai-secret \
      --from-literal=api-key=<TU_API_KEY> \
      -n k8sgpt-operator-system
    ```
    Verifica que el secreto se creó correctamente:
    ```bash
    kubectl get secrets -n k8sgpt-operator-system
    ```

2.  **Aplicar Configuración K8sGPT:**
    Esto despliega el analizador configurado para usar el secreto anterior:
    ```bash
    kubectl apply -f k8s/k8sgpt.yaml
    ```

3.  **🧪 Prueba de Fuego (Chaos Testing):**
    Vamos a romper algo intencionalmente para ver a la IA en acción.

    *   **Paso A: Crear un error:**
        ```bash
        kubectl run prueba-error --image=nginx:tag-inexistente
        ```
    *   **Paso B: Esperar análisis:**
        K8sGPT escanea cada pocos minutos. Puedes ver los resultados con:
        ```bash
        kubectl get results -n k8sgpt-operator-system
        ```
    *   **Paso C: Leer la explicación de la IA (Comando Universal):**
        ```bash
        kubectl get result -n k8sgpt-operator-system -o custom-columns="RECURSO:.metadata.name,DIAGNÓSTICO:.spec.details"
        ```

    *   **Paso D: Limpieza:**
        ```bash
        kubectl delete pod prueba-error
        ```

    #### Análisis Manual con la CLI de K8sGPT (Alternativo)

    Además del modo Operador automático, puedes realizar análisis manuales bajo demanda usando la CLI de `k8sgpt`. Esto es útil para depuraciones rápidas si tienes un shell dentro del clúster o la CLI instalada localmente.

    **Requisitos:**
    *   Tener la CLI de `k8sgpt` instalada en tu entorno.
    *   Tener una API Key de OpenAI configurada.

    **Ejemplo de uso:**

    Para analizar un tipo de recurso (como los Pods) y obtener una explicación de la IA, usa el flag `--explain`:

    ```bash
    # Analiza todos los Pods con problemas y pide una explicación a OpenAI
    k8sgpt analyze --filter Pod --explain --backend openai
    ```

    **Salida de ejemplo:**
    ```
    AI Provider: openai

    0: Pod default/prueba-error()
    - Error: Back-off pulling image "nginx:tag-inexistente": ErrImagePull...
    The error message "ErrImagePull" indicates that Kubernetes could not pull the specified Docker image... To fix this, you should verify the image name and tag...
    ```

    **Nota sobre los filtros:**

    `k8sGPT` utiliza una lista predefinida de filtros. Si intentas usar un filtro que no existe, como `node`, `cluster` o `svc` (el alias correcto es `Service`), verás una advertencia. Para ver la lista de todos los filtros válidos que puedes usar, ejecuta:

    ```bash
    k8sgpt filters list
    ```

---

## 🧨 Destrucción de la Infraestructura

Para evitar costos innecesarios, puedes destruir toda la infraestructura creada.

1.  Ve a la pestaña **Actions** en GitHub.
2.  Selecciona el flujo **"🧨 Destroy Infrastructure"** en la barra lateral izquierda.
3.  Haz clic en **Run workflow**.

Esto ejecutará `terraform destroy` y eliminará:
*   El Clúster EKS y sus nodos.
*   La VPC, Subnets y Gateways.
*   El repositorio ECR.

*(El bucket S3 de estado se conserva por seguridad, puedes borrarlo manualmente en la consola de AWS si lo deseas).*

---

## 📝 Comandos Útiles (Cheat Sheet)

### Terraform (Localmente)
```bash
# Inicializar directorio y descargar proveedores
terraform init

# Ver qué cambios se van a aplicar
terraform plan

# Aplicar cambios (Crear infraestructura)
terraform apply -auto-approve

# Destruir infraestructura
terraform destroy -auto-approve
```

### Kubernetes (Kubectl)
```bash
# Ver pods (contenedores)
kubectl get pods

# Ver servicios (Load Balancers)
kubectl get svc

# Ver logs de un pod específico
kubectl logs <nombre-del-pod>

# Describir un pod para ver errores
kubectl describe pod <nombre-del-pod>
```

---

**Autor:** [Tu Nombre]
**Proyecto:** CloudCamp - Kubernetes & Terraformaaaaa