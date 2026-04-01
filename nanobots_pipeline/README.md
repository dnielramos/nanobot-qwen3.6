# Enterprise-Grade NanoBot Agent Pipeline

Este proyecto implementa una arquitectura avanzada de agentes de Inteligencia Artificial utilizando Python, FastAPI y el modelo **Qwen 3.6** a través de **OpenRouter**. Está diseñado siguiendo los principios de **Clean Architecture**, asegurando que el código sea modular, escalable y mantenible.

## ¿Qué hacemos y qué valor aportamos?

En la actualidad, las aplicaciones basadas en IA suelen sufrir de código monolítico y difícil de escalar. Este proyecto aporta valor entregando un **pipeline de agentes de nivel empresarial** listo para integrarse en producción.

Nuestras principales ventajas son:

1. **Orquestación de Subagentes**: Un Agente Orquestador principal analiza los *prompts* del usuario y delega las tareas a agentes trabajadores especializados (Ej. *Data Processor*, *Code Reviewer*).
2. **Memoria de Doble Capa**:
   - *Corto Plazo*: Mantiene el contexto de la sesión actual en memoria.
   - *Largo Plazo*: Utiliza **ChromaDB** (una base de datos vectorial) para recordar interacciones pasadas y el resultado de los procesos en segundo plano.
3. **Uso Avanzado de Herramientas (Tool Calling)**: Los agentes pueden utilizar habilidades predefinidas con esquemas fuertemente tipados (Pydantic), como `web_search` o `file_reader` (protegido contra vulnerabilidades de path traversal).
4. **Tareas en Segundo Plano (Cron Jobs)**: Integra `APScheduler` para ejecutar procesos automáticos (como revisiones de código) sin intervención del usuario, guardando los resultados en la memoria a largo plazo.
5. **Robustez y Estabilidad**: Implementa manejo automático de errores y *exponential backoff* para los límites de tasa (HTTP 429) de la API de OpenRouter.
6. **API Limpia (FastAPI)**: Expone todas estas funcionalidades a través de una API RESTful moderna, lista para ser consumida por cualquier frontend.

---

## 🚀 Requisitos Previos

- Python 3.9 o superior.
- Una API Key de [OpenRouter](https://openrouter.ai/).

---

## ⚙️ Instalación

1. **Clona el repositorio** y entra en la carpeta del proyecto:
   `cd nanobots_pipeline`

2. **Crea y activa un entorno virtual** (opcional pero recomendado):
   - Crea el entorno: `python3 -m venv venv`
   - Activa el entorno en Linux/Mac: `source venv/bin/activate`
   - Activa el entorno en Windows: `venv\Scripts\activate`

3. **Instala las dependencias**:
   `pip install -r requirements.txt`

4. **Configura tus variables de entorno**:
   Crea un archivo llamado `.env` en la raíz del proyecto y añade tu API Key de OpenRouter:
   `OPENROUTER_API_KEY=tu_api_key_aqui`
   `(Opcional) Puedes cambiar el modelo si lo deseas: MODEL_ID=qwen/qwen3.6-plus-preview:free`

---

## 🏃‍♂️ Uso y Ejecución

Para iniciar el servidor de la API, ejecuta el siguiente comando en la raíz del proyecto (`nanobots_pipeline/`):

`uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

Una vez iniciado, verás en la consola que el backend y el programador de tareas (Cron scheduler) han comenzado con éxito.

### Explorar la API (Swagger UI)

FastAPI genera documentación interactiva automáticamente. Abre tu navegador y visita:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Ejemplo de Petición

Puedes interactuar con el pipeline enviando una petición `POST` al endpoint `/api/v1/chat`:

**Petición (cURL):**
`curl -X 'POST' 'http://localhost:8000/api/v1/chat' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"prompt": "Por favor revisa el código en skills/file_reader.py y dame sugerencias."}'`

**Respuesta Esperada:**
`{"session_id": "uuid-generado-automaticamente", "reply": "Code Reviewer Output:\n[Sugerencias de mejora del código...]"}`

Para mantener la conversación con el contexto actual, simplemente incluye el `session_id` devuelto en tus siguientes peticiones.

---

## 🏗️ Estructura del Proyecto

```text
nanobots_pipeline/
├── agents/             # Lógica de Orquestación y Subagentes trabajadores
├── api/                # Endpoints y rutas de FastAPI
├── config/             # Configuraciones y manejo de variables de entorno (.env)
├── memory/             # Sistema de memoria (Corto plazo y ChromaDB para largo plazo)
├── scheduler/          # Trabajos Cron y automatización (APScheduler)
├── services/           # Integración con proveedores externos (OpenRouter LLM)
├── skills/             # Herramientas modulares y tipadas (Web Search, File Reader)
├── main.py             # Punto de entrada de la aplicación FastAPI
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Este archivo
```
