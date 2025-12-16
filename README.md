# Documentation AI - Backend

Backend API desarrollado con **FastAPI + Beanie + MongoDB** para el sistema de documentación asistido por IA.

## 🚀 Quick Start

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tu configuración:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=documentation_ai
HOST=0.0.0.0
PORT=8000
FRONTEND_URL=http://localhost:8000
```

### 4. Iniciar MongoDB

```bash
# Con Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# O instala MongoDB localmente
```

### 5. Ejecutar el servidor

```bash
python run.py
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación API

Una vez iniciado el servidor, visita:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Arquitectura

```
backend/
├── src/
│   ├── config/
│   │   ├── settings.py         # Configuración con Pydantic
│   │   └── database.py         # Conexión MongoDB + Beanie
│   ├── models/
│   │   ├── project.py          # Modelo de Proyecto
│   │   ├── analysis_session.py # Modelo de Sesión de Análisis
│   │   └── generated_doc.py    # Modelo de Documentos Generados
│   ├── controllers/
│   │   ├── project_controller.py
│   │   ├── analysis_controller.py
│   │   └── generated_doc_controller.py
│   ├── routes/
│   │   ├── projects.py         # Endpoints de proyectos
│   │   ├── analysis.py         # Endpoints de análisis
│   │   ├── generated_docs.py   # Endpoints de docs generados
│   │   └── schemas/            # Schemas Pydantic
│   ├── utils/
│   │   ├── token_generator.py  # Generador de tokens
│   │   └── yaml_validator.py   # Validador de YAML
│   └── main.py                 # Aplicación FastAPI
├── run.py                      # Script para ejecutar
├── requirements.txt
└── .env.example
```

## 🔌 Endpoints Principales

### Proyectos

- `POST /api/projects` - Crear proyecto
- `GET /api/projects` - Listar proyectos
- `GET /api/projects/{id}` - Obtener proyecto
- `PUT /api/projects/{id}` - Actualizar proyecto
- `DELETE /api/projects/{id}` - Eliminar proyecto

### Análisis

- `POST /api/projects/{id}/analysis` - Crear sesión de análisis
- `GET /api/analysis/{id}` - Obtener análisis
- `PUT /api/analysis/{id}/iteration` - Agregar iteración
- `PUT /api/analysis/{id}/complete` - Marcar como completo
- `GET /api/projects/{id}/analyses` - Listar análisis del proyecto

### Responder Preguntas (Público)

- `GET /api/answer/{token}` - Ver formulario de preguntas
- `POST /api/answer/{token}` - Guardar respuestas

### Documentos Generados

- `POST /api/projects/{id}/generate-docs` - Guardar docs generados
- `GET /api/projects/{id}/docs` - Listar docs del proyecto
- `GET /api/docs/{id}` - Obtener documento

## 🧪 Testing

```bash
pytest
```

## 🐳 Docker

```bash
docker build -t documentation-ai-backend .
docker run -p 8000:8000 documentation-ai-backend
```

## 📖 Flujo de Uso

1. **Crear Proyecto** → `POST /api/projects`
2. **Iniciar Análisis** → `POST /api/projects/{id}/analysis`
   - Copilot genera YAML
   - Backend devuelve `share_url`
3. **Experto Responde** → `GET/POST /api/answer/{token}`
   - Abre URL pública
   - Completa formulario
4. **Proceso Iterativo** → `PUT /api/analysis/{id}/iteration`
   - Si Copilot necesita más info, genera nuevo YAML
   - Backend genera nuevo `share_url`
5. **Completar Análisis** → `PUT /api/analysis/{id}/complete`
6. **Guardar Docs** → `POST /api/projects/{id}/generate-docs`

## 🛠️ Tecnologías

- **FastAPI** 0.104+ - Framework web moderno
- **Beanie** 1.23+ - ODM para MongoDB (async)
- **Motor** 3.3+ - Driver async de MongoDB
- **Pydantic** 2.5+ - Validación de datos
- **Uvicorn** - Servidor ASGI

## 📝 Licencia

MIT
