# Architecture Overview

Visual guide to understanding Jim's File Converter's architecture.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Frontend (SPA)                         │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │ index.html │  │  style.css │  │   app.js   │         │  │
│  │  │  (UI)      │  │  (Design)  │  │  (Logic)   │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend Server                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     API Layer (routes.py)                 │  │
│  │  • POST /api/convert     • GET /api/health               │  │
│  │  • GET /api/download     • GET /api/formats              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Validation Layer                        │  │
│  │  • File size check    • Format validation                │  │
│  │  • MIME type check    • Filename sanitization            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Service Layer                           │  │
│  │  ┌──────────────────┐    ┌──────────────────┐           │  │
│  │  │  File Handler    │    │  Converter       │           │  │
│  │  │  • Save upload   │    │  • API calls     │           │  │
│  │  │  • Cleanup       │    │  • Job polling   │           │  │
│  │  └──────────────────┘    └──────────────────┘           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Temporary Storage                        │  │
│  │  temp/                                                    │  │
│  │  • Input files (deleted after upload)                    │  │
│  │  • Output files (cleaned up after 2 hours)               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CloudConvert API                             │
│  • Image format conversion                                      │
│  • Free tier: 25 conversions/day                               │
│  • Supports: JPEG, PNG, WebP, GIF, and more                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Request Flow

### File Upload & Conversion Flow

```
1. User Action
   │
   ├─ User drags image onto drop zone
   │  OR clicks "Browse Files"
   │
   ▼
2. Frontend Validation
   │
   ├─ Check file type (image/*)
   ├─ Check file size (< 10MB)
   ├─ Display preview
   │
   ▼
3. User Selects Format
   │
   ├─ Choose output format (JPEG/PNG/WebP/GIF)
   ├─ Click "Convert"
   │
   ▼
4. Frontend Request
   │
   ├─ Create FormData with file + format
   ├─ POST to /api/convert
   ├─ Show progress bar
   │
   ▼
5. Backend Validation
   │
   ├─ Validate file size (validators.py)
   ├─ Validate file format (validators.py)
   ├─ Check MIME type (validators.py)
   ├─ Sanitize filename (validators.py)
   │
   ▼
6. File Storage
   │
   ├─ Generate UUID for unique filename
   ├─ Save to temp/ directory
   │
   ▼
7. CloudConvert Integration
   │
   ├─ Create conversion job
   ├─ Upload file to CloudConvert
   ├─ Poll job status (every 2 seconds)
   ├─ Download converted file
   │
   ▼
8. Response
   │
   ├─ Generate download URL
   ├─ Return success response
   ├─ Delete input file
   │
   ▼
9. Frontend Download
   │
   ├─ Display success message
   ├─ Show download button
   ├─ Trigger automatic download
   │
   ▼
10. Cleanup
    │
    ├─ Output file available for download
    ├─ Background task cleans up after 2 hours
```

---

## 🔄 Data Flow Diagram

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Upload Image
     ▼
┌────────────────┐
│   Frontend     │
│   (app.js)     │
└────┬───────────┘
     │
     │ 2. POST /api/convert
     │    (FormData: file, output_format)
     ▼
┌────────────────────┐
│   API Routes       │
│   (routes.py)      │
└────┬───────────────┘
     │
     │ 3. Validate
     ▼
┌────────────────────┐
│   Validators       │
│   (validators.py)  │
└────┬───────────────┘
     │
     │ 4. Save File
     ▼
┌────────────────────┐
│   File Handler     │
│   (file_handler.py)│
└────┬───────────────┘
     │
     │ 5. Convert
     ▼
┌────────────────────┐
│   Converter        │
│   (converter.py)   │
└────┬───────────────┘
     │
     │ 6. API Request
     ▼
┌────────────────────┐
│  CloudConvert API  │
└────┬───────────────┘
     │
     │ 7. Converted File
     ▼
┌────────────────────┐
│   File Handler     │
│   (save output)    │
└────┬───────────────┘
     │
     │ 8. Download URL
     ▼
┌────────────────────┐
│   API Response     │
└────┬───────────────┘
     │
     │ 9. JSON Response
     ▼
┌────────────────────┐
│   Frontend         │
│   (show download)  │
└────┬───────────────┘
     │
     │ 10. Download File
     ▼
┌──────────┐
│   User   │
└──────────┘
```

---

## 🗂️ File Organization

### Backend Structure

```
app/
│
├── main.py                    # Application entry point
│   ├── FastAPI app setup
│   ├── CORS middleware
│   ├── Static file serving
│   ├── Template rendering
│   └── Background cleanup task
│
├── config.py                  # Configuration management
│   ├── Settings class (Pydantic)
│   ├── Environment variables
│   ├── API configuration
│   └── Directory paths
│
├── api/
│   └── routes.py             # HTTP endpoints
│       ├── POST /api/convert
│       ├── GET /api/download/{filename}
│       ├── GET /api/health
│       └── GET /api/formats
│
├── services/
│   ├── converter.py          # CloudConvert integration
│   │   ├── CloudConvertService class
│   │   ├── convert_image()
│   │   ├── _create_job()
│   │   ├── _upload_file()
│   │   ├── _wait_for_job()
│   │   └── _download_file()
│   │
│   └── file_handler.py       # File operations
│       ├── FileHandler class
│       ├── save_upload()
│       ├── delete_file()
│       ├── cleanup_old_files()
│       └── generate_output_filename()
│
└── utils/
    └── validators.py         # Input validation
        ├── validate_file_size()
        ├── validate_file_format()
        ├── validate_output_format()
        └── sanitize_filename()
```

### Frontend Structure

```
templates/
└── index.html                # Main HTML page
    ├── Drop zone
    ├── File preview
    ├── Format selection
    ├── Progress bar
    ├── Result display
    └── Error handling

static/
├── css/
│   └── style.css            # Styling
│       ├── Dark theme
│       ├── Gradient effects
│       ├── Responsive design
│       └── Animations
│
└── js/
    └── app.js               # Frontend logic
        ├── File handling
        ├── Drag & drop
        ├── API communication
        ├── Progress tracking
        └── Error handling
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: Frontend Validation                          │
│  ├─ File type check (image/*)                         │
│  ├─ File size check (< 10MB)                          │
│  └─ User feedback                                      │
│                                                         │
│  Layer 2: Backend Validation                           │
│  ├─ File size enforcement                              │
│  ├─ Format whitelist (jpg, png, webp, gif)           │
│  ├─ MIME type verification                            │
│  └─ Reject invalid files                              │
│                                                         │
│  Layer 3: Filename Sanitization                        │
│  ├─ Remove path traversal attempts (../)              │
│  ├─ Remove dangerous characters                        │
│  ├─ Limit filename length                             │
│  └─ UUID-based storage names                          │
│                                                         │
│  Layer 4: API Key Protection                           │
│  ├─ Stored in .env file                               │
│  ├─ Never exposed to frontend                         │
│  ├─ Not committed to git                              │
│  └─ Loaded via environment variables                  │
│                                                         │
│  Layer 5: Temporary Storage                            │
│  ├─ Unique UUIDs prevent collisions                   │
│  ├─ Automatic cleanup (2 hours)                       │
│  ├─ Input files deleted immediately                   │
│  └─ No permanent storage                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ Performance Architecture

### Async Operations

```
Traditional Synchronous:
Request 1 ──────────────────────────────> Response 1
                Request 2 ──────────────────────────────> Response 2
                                Request 3 ──────────────────────────────> Response 3

With Async/Await:
Request 1 ────┐
              ├──> CloudConvert API
Request 2 ────┤    (Non-blocking I/O)
              ├──> All processed concurrently
Request 3 ────┘
              │
              ├──> Response 1
              ├──> Response 2
              └──> Response 3
```

### Background Tasks

```
Main Thread:
├─ Handle HTTP requests
├─ Process conversions
└─ Send responses

Background Thread:
└─ Cleanup Task (runs every hour)
   ├─ Scan temp/ directory
   ├─ Check file ages
   └─ Delete files > 2 hours old
```

---

## 🔄 State Management

### Frontend State

```javascript
// Global State
let selectedFile = null;        // Currently selected file
let conversionResult = null;    // Result from conversion

// UI States
- Initial: Drop zone visible
- File Selected: Preview visible, format selection shown
- Converting: Progress bar visible
- Success: Download button visible
- Error: Error message visible
```

### Backend State

```python
# Stateless Design
# Each request is independent
# No session storage
# No user authentication (yet)

# Temporary State
- Files in temp/ directory
- Background cleanup task running
```

---

## 🧩 Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│                   Component Diagram                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐                                      │
│  │   Frontend   │                                      │
│  │   (app.js)   │                                      │
│  └──────┬───────┘                                      │
│         │                                               │
│         │ HTTP Request                                  │
│         ▼                                               │
│  ┌──────────────┐                                      │
│  │ API Routes   │                                      │
│  │ (routes.py)  │                                      │
│  └──────┬───────┘                                      │
│         │                                               │
│         ├──────────────┬──────────────┬────────────┐  │
│         ▼              ▼              ▼            ▼  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │Validators│  │  File    │  │Converter │  │Config│ │
│  │          │  │ Handler  │  │          │  │      │ │
│  └──────────┘  └──────────┘  └────┬─────┘  └──────┘ │
│                                    │                   │
│                                    │ API Call          │
│                                    ▼                   │
│                            ┌──────────────┐           │
│                            │ CloudConvert │           │
│                            │     API      │           │
│                            └──────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Deployment Architecture

### Development

```
Developer Machine
├─ Python virtual environment
├─ Uvicorn dev server (--reload)
├─ Local file storage (temp/)
└─ .env file with API key
```

### Production (Recommended)

```
Cloud Platform (Heroku/Railway/Render)
├─ Gunicorn + Uvicorn workers
├─ Environment variables (no .env file)
├─ Temporary file storage
├─ HTTPS enabled
└─ Auto-scaling (optional)
```

### Production (Advanced)

```
┌─────────────────────────────────────────┐
│              Load Balancer              │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────┐  ┌───────────────┐
│  App Server 1 │  │  App Server 2 │
└───────┬───────┘  └───────┬───────┘
        │                  │
        └────────┬─────────┘
                 ▼
        ┌─────────────────┐
        │  Cloud Storage  │
        │  (S3/Azure)     │
        └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  CloudConvert   │
        │      API        │
        └─────────────────┘
```

---

## 🔍 Error Handling Flow

```
┌─────────────────────────────────────────────────────────┐
│                  Error Handling Layers                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Frontend Errors:                                       │
│  ├─ File too large → Show user-friendly message        │
│  ├─ Invalid format → Show supported formats            │
│  └─ Network error → Show retry option                  │
│                                                         │
│  Backend Validation Errors:                             │
│  ├─ HTTPException(400) → Bad request                   │
│  ├─ HTTPException(413) → File too large                │
│  └─ HTTPException(404) → File not found                │
│                                                         │
│  Service Layer Errors:                                  │
│  ├─ ConversionError → Wrap API errors                  │
│  ├─ Network errors → Retry or fail gracefully          │
│  └─ File I/O errors → Clean up and report              │
│                                                         │
│  API Layer Response:                                    │
│  ├─ 200: Success with data                             │
│  ├─ 400: Client error with detail                      │
│  ├─ 500: Server error with message                     │
│  └─ All errors logged for debugging                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Design Principles

### 1. Separation of Concerns
- **API Layer**: Handle HTTP requests/responses
- **Service Layer**: Business logic and external APIs
- **Utility Layer**: Reusable validation and helpers

### 2. Single Responsibility
- Each module has one clear purpose
- Easy to test and maintain
- Simple to extend

### 3. Async First
- All I/O operations are async
- Non-blocking API calls
- Better performance under load

### 4. Security by Default
- Validate everything
- Sanitize all inputs
- Fail securely

### 5. User Experience
- Clear error messages
- Visual feedback
- Responsive design
- Mobile-friendly

---

## 📈 Scalability Considerations

### Current Limitations
- Single server
- Local file storage
- No caching
- No queue system

### Future Improvements
1. **Horizontal Scaling**: Multiple app servers
2. **Cloud Storage**: S3/Azure for files
3. **Queue System**: Celery/RQ for background jobs
4. **Caching**: Redis for repeated conversions
5. **Database**: Track history and analytics
6. **CDN**: Serve static assets globally

---

## 🔧 Configuration Architecture

```
Environment Variables (.env)
         │
         ▼
┌─────────────────────┐
│   Settings Class    │
│   (Pydantic)        │
└──────────┬──────────┘
           │
           ├──> API Configuration
           ├──> File Size Limits
           ├──> Supported Formats
           ├──> Directory Paths
           └──> Server Settings
                    │
                    ▼
            Used by all modules
```

---

This architecture provides a solid foundation for a production-ready application while remaining simple enough for learning and experimentation.

