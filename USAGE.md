# 🚀 Guía de Uso del Backend

## 📋 Flujo Completo de Documentación

### 1️⃣ Crear un Proyecto

```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sistema E-commerce",
    "description": "Plataforma de ventas online",
    "created_by": "analista@empresa.com",
    "metadata": {
      "repository": "https://github.com/empresa/ecommerce",
      "technology": "Python + FastAPI + React"
    }
  }'
```

**Respuesta:**
```json
{
  "id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "name": "Sistema E-commerce",
  "description": "Plataforma de ventas online",
  "created_by": "analista@empresa.com",
  "status": "active",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z",
  "metadata": {
    "repository": "https://github.com/empresa/ecommerce",
    "technology": "Python + FastAPI + React"
  }
}
```

---

### 2️⃣ Iniciar Sesión de Análisis

El analista pega el YAML generado por Copilot:

```bash
curl -X POST http://localhost:8000/api/projects/65a1b2c3d4e5f6g7h8i9j0k1/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "analysis_type": "deployment",
    "created_by": "analista@empresa.com",
    "assigned_to": "devops@empresa.com",
    "yaml_config": {
      "title": "🚀 Deployment - E-commerce",
      "description": "Completa este formulario...",
      "sections": [
        {
          "icon": "☁️",
          "title": "Cloud Provider",
          "questions": [
            {
              "id": "cloudProvider",
              "type": "checkbox",
              "label": "¿Qué cloud providers usa?",
              "options": [
                {"value": "aws", "label": "AWS"},
                {"value": "gcp", "label": "GCP"}
              ]
            }
          ]
        }
      ]
    }
  }'
```

**Respuesta:**
```json
{
  "id": "75b2c3d4e5f6g7h8i9j0k1l2",
  "project_id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "project_name": "Sistema E-commerce",
  "analysis_type": "deployment",
  "status": "pending_answers",
  "iteration": 1,
  "share_token": "a7B3kD9mP2qR5wX8",
  "share_url": "http://localhost:8000/answer/a7B3kD9mP2qR5wX8",
  "created_by": "analista@empresa.com",
  "assigned_to": "devops@empresa.com"
}
```

**El analista envía la URL al experto:** `http://localhost:8000/answer/a7B3kD9mP2qR5wX8`

---

### 3️⃣ El Experto Ve las Preguntas (URL Pública)

```bash
curl http://localhost:8000/api/answer/a7B3kD9mP2qR5wX8
```

**Respuesta:**
```json
{
  "project_name": "Sistema E-commerce",
  "analysis_type": "deployment",
  "iteration": 1,
  "yaml_config": {
    "title": "🚀 Deployment - E-commerce",
    "sections": [...]
  },
  "answers": {}
}
```

---

### 4️⃣ El Experto Responde (URL Pública)

```bash
curl -X POST http://localhost:8000/api/answer/a7B3kD9mP2qR5wX8 \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "cloudProvider": ["aws", "gcp"],
      "hasDocker": "si",
      "environments": ["dev", "staging", "prod"]
    }
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Respuestas guardadas correctamente"
}
```

---

### 5️⃣ El Analista Revisa Respuestas

```bash
curl http://localhost:8000/api/analysis/75b2c3d4e5f6g7h8i9j0k1l2
```

**Respuesta:**
```json
{
  "id": "75b2c3d4e5f6g7h8i9j0k1l2",
  "answers": {
    "cloudProvider": ["aws", "gcp"],
    "hasDocker": "si",
    "environments": ["dev", "staging", "prod"]
  },
  "status": "pending_answers",
  "iteration": 1
}
```

---

### 6️⃣ Copilot Necesita Más Info (Nueva Iteración)

El analista pega las respuestas en Copilot. Si Copilot genera un nuevo YAML:

```bash
curl -X PUT http://localhost:8000/api/analysis/75b2c3d4e5f6g7h8i9j0k1l2/iteration \
  -H "Content-Type: application/json" \
  -d '{
    "yaml_config": {
      "title": "🚀 Deployment - Iteración 2",
      "sections": [
        {
          "icon": "📊",
          "title": "Monitoreo",
          "questions": [
            {
              "id": "monitoringTool",
              "type": "select",
              "label": "¿Qué herramienta de monitoreo usan?",
              "options": [
                {"value": "datadog", "label": "Datadog"},
                {"value": "newrelic", "label": "New Relic"}
              ]
            }
          ]
        }
      ]
    },
    "needs_more_info": true
  }'
```

**Respuesta:**
```json
{
  "id": "75b2c3d4e5f6g7h8i9j0k1l2",
  "iteration": 2,
  "share_token": "x9Y4nE2vQ8rT6aZ3",
  "share_url": "http://localhost:8000/answer/x9Y4nE2vQ8rT6aZ3"
}
```

**Nueva URL para el experto:** `http://localhost:8000/answer/x9Y4nE2vQ8rT6aZ3`

---

### 7️⃣ Copilot Confirma "todo ok"

```bash
curl -X PUT http://localhost:8000/api/analysis/75b2c3d4e5f6g7h8i9j0k1l2/complete
```

**Respuesta:**
```json
{
  "status": "completed",
  "needs_more_info": false
}
```

---

### 8️⃣ Guardar Documentos Generados

El analista pega los archivos .md generados por Copilot:

```bash
curl -X POST http://localhost:8000/api/projects/65a1b2c3d4e5f6g7h8i9j0k1/generate-docs \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_session_id": "75b2c3d4e5f6g7h8i9j0k1l2",
    "generated_by": "analista@empresa.com",
    "files": [
      {
        "path": "ai_docs/06-infraestructura/01-deployment.md",
        "content": "# Deployment\n\n## Cloud Providers\n\n- AWS\n- GCP\n\n..."
      },
      {
        "path": "ai_docs/06-infraestructura/02-ci-cd.md",
        "content": "# CI/CD Pipeline\n\n..."
      },
      {
        "path": "ai_docs/06-infraestructura/03-monitoreo.md",
        "content": "# Monitoreo\n\n..."
      }
    ]
  }'
```

**Respuesta:**
```json
{
  "id": "85c3d4e5f6g7h8i9j0k1l2m3",
  "project_id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "project_name": "Sistema E-commerce",
  "files": [
    {
      "path": "ai_docs/06-infraestructura/01-deployment.md",
      "content": "# Deployment\n\n...",
      "generated_at": "2025-01-15T15:30:00Z"
    },
    ...
  ],
  "generated_at": "2025-01-15T15:30:00Z",
  "generated_by": "analista@empresa.com"
}
```

---

### 9️⃣ Consultar Documentos del Proyecto

```bash
curl http://localhost:8000/api/projects/65a1b2c3d4e5f6g7h8i9j0k1/docs
```

---

## 🎨 Ejemplos con Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Crear proyecto
response = requests.post(f"{BASE_URL}/api/projects", json={
    "name": "Mi Proyecto",
    "description": "Descripción",
    "created_by": "yo@empresa.com"
})
project = response.json()
project_id = project["id"]

# 2. Crear análisis
response = requests.post(
    f"{BASE_URL}/api/projects/{project_id}/analysis",
    json={
        "project_id": project_id,
        "analysis_type": "deployment",
        "created_by": "yo@empresa.com",
        "yaml_config": {...}
    }
)
analysis = response.json()
share_url = analysis["share_url"]

print(f"Envía esta URL al experto: {share_url}")
```

---

## 📚 Swagger UI

Visita http://localhost:8000/docs para la documentación interactiva completa.
