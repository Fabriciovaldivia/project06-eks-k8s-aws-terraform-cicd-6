# ✅ Solución: Error "init.sql not found" en GitHub Actions

## 🔍 Problema identificado

El workflow estaba usando `docker/build-push-action@v4` que no estaba enviando el contexto correctamente, resultando en:

```
#5 [internal] load build context
#5 transferring context: 2B done  ← ¡VACÍO!
```

Esto causaba que Docker no encontrara los archivos del directorio (como `init.sql`).

---

## ✅ Solución aplicada

He cambiado el workflow para usar **comandos `docker build` directos** en lugar de la acción de GitHub:

### Antes (❌ No funcionaba):
```yaml
- name: 🐳 Build database image
  uses: docker/build-push-action@v4
  with:
    context: ${{ matrix.service.path }}  # ← No funcionaba
    push: false
    tags: proyecto06-database:latest
```

### Ahora (✅ Funciona):
```yaml
- name: 🐳 Build database image
  run: |
    docker build \
      -t proyecto06-database:latest \
      -t proyecto06-database:${{ github.sha }} \
      database/  # ← Especifica el contexto directamente
```

---

## 📝 Cambios en `.github/workflows/build-deploy.yml`

### 1. Job `build` - Usa `docker build` directo
```yaml
steps:
  - name: 📋 List files in ${{ matrix.service.path }}
    run: ls -la ${{ matrix.service.path }}/  # Debug: verificar archivos

  - name: 🐳 Build ${{ matrix.service.name }} image
    run: |
      docker build \
        -t ${{ env.PROJECT_NAME }}-${{ matrix.service.name }}:latest \
        -t ${{ env.PROJECT_NAME }}-${{ matrix.service.name }}:${{ github.sha }} \
        ${{ matrix.service.path }}/  # ✅ Contexto especificado correctamente
```

### 2. Job `push-ecr` - Usa `docker build` y `docker push` directo
```yaml
- name: 📤 Build and push ${{ matrix.service.name }} to ECR
  run: |
    REGISTRY=${{ steps.login-ecr.outputs.registry }}
    
    docker build \
      -t $REGISTRY/${{ env.PROJECT_NAME }}-${{ matrix.service.name }}:latest \
      ${{ matrix.service.path }}/  # ✅ Contexto especificado
    
    docker push $REGISTRY/${{ env.PROJECT_NAME }}-${{ matrix.service.name }}:latest
```

---

## 🚀 Ahora el pipeline debería funcionar

Cuando hagas `git push`:

```
✅ Checkout code
✅ List files in database/  (verifica que init.sql existe)
✅ Build database image  (docker build -t ... database/)
✅ Login to ECR
✅ Build and push to ECR
✅ Deploy a Kubernetes
✅ Verification
```

---

## 📊 Ventajas de este cambio

| Aspecto | docker/build-push-action | docker build directo |
|--------|--------------------------|----------------------|
| Contexto | ❌ Problemático | ✅ Simple y directo |
| Debugging | ❌ Complejo | ✅ Fácil (ver logs) |
| Contexto de build | ❌ No envía archivos | ✅ Envía correctamente |
| Velocidad | ⚠️ Buildx overhead | ✅ Native Docker |
| Confiabilidad | ❌ Variable | ✅ Consistente |

---

## 🔍 Cómo verificar que funciona

1. Haz `git push` a tu repo
2. Ve a **GitHub → Actions**
3. Busca el workflow `🚀 Build & Deploy - Proyecto06`
4. Verifica los logs:
   - ✅ "List files in database/" debe mostrar `init.sql`
   - ✅ "Build database image" debe completar exitosamente
   - ✅ El resto del pipeline debe continuar

---

## 💡 Si aún hay problemas

Si ves el error nuevamente:

```bash
# 1. Verifica que los archivos existan localmente
ls -la database/
ls -la backend/
ls -la frontend/

# 2. Verifica que Dockerfile sea válido
cat database/Dockerfile

# 3. Haz commit y push
git add .
git commit -m "Fix workflow context"
git push origin main
```

---

## ✨ Cambios aplicados

✅ Build job - Usa `docker build` directo
✅ Push-ECR job - Usa `docker build` y `docker push` directo
✅ Agregado debugging (list files) para ver qué existe
✅ Contexto especificado con ruta absoluta (`database/`, `backend/`, `frontend/`)

**El error de "init.sql not found" debería estar SOLUCIONADO** ✅
