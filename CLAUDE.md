# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Jim's File Converter is a web-based image format converter. Users upload images (JPG, PNG, WebP, GIF, ICO) and convert them to other supported formats with optional quality and resize controls. The backend is FastAPI (Python), the frontend is vanilla JavaScript, and conversion uses Pillow locally with CloudConvert API as a fallback.

## Running the App

```bash
# Development (auto-reload)
python run.py
# or
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Quick start (uses start.sh which activates venv)
./start.sh
```

The app runs at `http://localhost:8000`. Requires a `.env` file:
```
CLOUDCONVERT_API_KEY=your_api_key_here
MAX_FILE_SIZE_MB=10
HOST=0.0.0.0
PORT=8000
```

## Building the Windows Executable

```bash
python build_exe.py
# Output: dist/JimsFileConverter.exe
```

## Testing the API

```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/formats
```

No automated test suite is configured. `requirements-dev.txt` lists pytest as optional (commented out).

## Architecture

### Conversion Strategy (Hybrid)

1. **Local first** — `local_converter.py` uses Pillow (fast, no API calls, supports all formats including ICO)
2. **Cloud fallback** — `converter.py` calls the CloudConvert v2 REST API if local conversion fails

### Request Flow

```
Browser (app.js) → POST /api/convert → routes.py → validators.py
→ file_handler.py (save with UUID) → local_converter.py or converter.py
→ file_handler.py (save result) → JSON response with filename
→ GET /api/download/{filename} → browser download
```

Background task in `main.py` runs hourly to delete temp files older than 2 hours.

### Key Modules

| File | Role |
|------|------|
| `app/main.py` | FastAPI setup, lifespan, mounts static/templates, starts cleanup task |
| `app/config.py` | Pydantic `Settings` class reads from `.env`; `settings` is the singleton |
| `app/api/routes.py` | Four endpoints: `POST /api/convert`, `GET /api/download/{filename}`, `GET /api/health`, `GET /api/formats` |
| `app/services/local_converter.py` | Pillow-based conversion; runs in thread pool to avoid blocking event loop |
| `app/services/converter.py` | CloudConvert async integration; polls job status every 2s (max 120s) |
| `app/services/file_handler.py` | Saves uploads with UUID prefix, handles cleanup |
| `app/utils/validators.py` | Extension whitelist, MIME type check, size enforcement, filename sanitization |
| `templates/index.html` | Jinja2 template; receives `max_file_size_mb` and `supported_formats` from the backend |
| `static/js/app.js` | Drag-drop, FormData, fetch, progress bar, download trigger |

### Supported Formats

`jpg`, `jpeg`, `png`, `webp`, `gif`, `ico` — both input and output. Quality (1–100) applies to JPEG/WebP. Resize preserves aspect ratio when only one dimension is given.
