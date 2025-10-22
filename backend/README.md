# 📚 Document Analyzer API - Backend

API REST completa para análisis inteligente de documentos usando IA local (Ollama) con almacenamiento en Supabase.

## 🌟 Características

- ✅ Análisis de documentos con IA (Ollama - llama3.2)
- ✅ Soporta PDF, DOCX, TXT, MD
- ✅ Almacenamiento persistente en Supabase
- ✅ Análisis comprehensivo: resumen, puntos clave, sentimiento
- ✅ API RESTful con FastAPI
- ✅ Documentación automática (Swagger/ReDoc)
- ✅ Validación de datos con Pydantic
- ✅ Procesamiento de archivos robusto

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.12+
- Ollama instalado y corriendo
- Cuenta en Supabase

### Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd backend

# Crear entorno virtual
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### Configurar Ollama

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo
ollama pull llama3.2

# Verificar
ollama run llama3.2 "Hola"
```

### Configurar Supabase

1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ejecutar SQL para crear tabla:

```sql
CREATE TABLE analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  document_name TEXT NOT NULL,
  analysis_type TEXT,
  summary TEXT,
  key_points TEXT,
  sentiment TEXT,
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
```

3. Copiar credenciales a `.env`

### Ejecutar

```bash
# Método 1: Directo
python main.py

# Método 2: Con uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Servidor disponible en:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 📡 API Endpoints

### Sistema

- `GET /api/v1/system/health` - Health check
- `GET /api/v1/system/models` - Listar modelos de IA
- `GET /api/v1/system/info` - Información del sistema

### Documentos

- `POST /api/v1/documents/upload` - Subir y analizar documento
- `POST /api/v1/documents/analyze-text` - Analizar texto directo
- `GET /api/v1/documents/analyses` - Listar análisis
- `GET /api/v1/documents/analyses/{id}` - Obtener análisis específico
- `DELETE /api/v1/documents/analyses/{id}` - Eliminar análisis
- `GET /api/v1/documents/search` - Buscar análisis
- `GET /api/v1/documents/statistics` - Estadísticas de usuario

## 📖 Ejemplo de Uso

### cURL

```bash
# Subir documento
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@documento.pdf"

# Analizar texto
curl -X POST "http://localhost:8000/api/v1/documents/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Tu texto aquí", "analysis_type": "summary"}'
```

### Python

```python
import requests

# Subir documento
with open("doc.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/documents/upload",
        files={"file": f}
    )
    print(response.json())
```

### JavaScript/Frontend

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/v1/documents/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

## 🏗️ Arquitectura

```
backend/
├── main.py                 # Punto de entrada FastAPI
├── app/
│   ├── api/               # Rutas de la API
│   │   └── routes/
│   │       ├── documents.py
│   │       └── system.py
│   ├── core/              # Configuración
│   │   ├── config.py
│   │   └── security.py
│   ├── models/            # Modelos Pydantic
│   │   └── schemas.py
│   ├── services/          # Lógica de negocio
│   │   ├── ollama_service.py
│   │   └── supabase_service.py
│   └── utils/             # Utilidades
│       ├── text_extraction.py
│       └── file_validation.py
└── uploads/               # Archivos temporales
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Ver `.env.example` para todas las opciones disponibles.

Principales:
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Anon key de Supabase
- `SECRET_KEY`: Clave secreta para JWT (generar con `openssl rand -hex 32`)
- `OLLAMA_MODEL`: Modelo a usar (default: llama3.2)
- `MAX_FILE_SIZE`: Tamaño máximo de archivo en bytes

### Tipos de Análisis

- `general`: Análisis general del documento
- `summary`: Resumen conciso
- `key_points`: Extracción de puntos clave
- `sentiment`: Análisis de sentimiento
- `comprehensive`: Análisis completo (combina todos los anteriores)
- `entities`: Extracción de entidades (personas, lugares, etc.)
- `questions`: Generación de preguntas sobre el contenido

## 🧪 Testing

```bash
# Instalar dependencias de test
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Con coverage
pytest --cov=app tests/
```

## 📝 Documentación Completa

Ver [GUIA_PROYECTO_COMPLETA.md](../GUIA_PROYECTO_COMPLETA.md) para documentación extensa.

## 🐛 Troubleshooting

### Ollama no se conecta
```bash
# Verificar que está corriendo
curl http://localhost:11434/api/tags

# Reiniciar Ollama
ollama serve
```

### Error de Supabase
- Verifica credenciales en `.env`
- Comprueba que la tabla `analyses` existe
- Revisa permisos/políticas RLS

### Error al extraer texto de PDF
```bash
pip uninstall PyPDF2
pip install PyPDF2==3.0.1
```

## 📦 Dependencias Principales

- **FastAPI**: Framework web
- **Ollama**: Cliente para IA local
- **Supabase**: Base de datos y backend
- **PyPDF2**: Procesamiento de PDFs
- **python-docx**: Procesamiento de DOCX
- **Pydantic**: Validación de datos
- **httpx**: Cliente HTTP async

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

MIT License

## 🎯 Próximos Pasos

- [ ] Implementar frontend (React/Vue/Svelte)
- [ ] Añadir autenticación completa (JWT)
- [ ] Implementar rate limiting
- [ ] Añadir cache de respuestas
- [ ] Soporte para más formatos (EPUB, HTML)
- [ ] OCR para PDFs escaneados
- [ ] Deployment con Docker

## 📧 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

---

**¡Gracias por usar Document Analyzer! 🚀**
