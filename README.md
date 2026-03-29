# Jim's File Converter

A modern web-based image conversion tool that supports converting between JPEG, PNG, WebP, and GIF formats.

## Features

- 🎯 Simple drag-and-drop file upload
- 🔄 Convert between JPEG, PNG, WebP, and GIF
- 📱 Responsive design for mobile and desktop
- ⚡ Fast conversion using CloudConvert API
- 🎨 Clean, modern UI
- 📊 Real-time progress tracking
- 🛠️ Optional quality and resize controls

## Tech Stack

- **Backend:** Python with FastAPI
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **API:** CloudConvert for file conversion
- **File Storage:** Temporary local storage with automatic cleanup

## Setup Instructions

### Option A: Quick Start with Windows Executable (Easiest!)

If you just want to run the app without setting up Python:

1. **Download or build the executable** (see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md))
2. **Create a `.env` file** in the same folder as `JimsFileConverter.exe`:
   ```env
   CLOUDCONVERT_API_KEY=your_api_key_here
   MAX_FILE_SIZE_MB=10
   HOST=127.0.0.1
   PORT=8000
   ```
3. **Get your CloudConvert API key:**
   - Sign up at https://cloudconvert.com/
   - Navigate to Dashboard > API
   - Copy your API key and add it to the `.env` file
4. **Double-click `JimsFileConverter.exe`** - The browser will open automatically!

### Option B: Python Development Setup

If you want to develop or modify the code:

### Prerequisites

- Python 3.8 or higher
- `uv` for Python environment and dependency management
- CloudConvert API key (free tier available)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jims_file_converter
```

2. Install project dependencies with `uv`:
```bash
uv sync
```

   *Optional: Include development dependencies (for building executables):*
   ```bash
   uv sync --group dev
   ```

3. Create a `.env` file in the root directory with the following content:
```env
CLOUDCONVERT_API_KEY=your_api_key_here
MAX_FILE_SIZE_MB=10
HOST=0.0.0.0
PORT=8000
```
   **Note:** Simply create a new file named `.env` (with the dot at the beginning) in the root folder.

4. Get your CloudConvert API key:
   - Sign up at https://cloudconvert.com/
   - Navigate to Dashboard > API
   - Copy your API key and add it to the `.env` file

### Running the Application

**Option 1: Using the quick start script (Easiest!)**
```bash
./start.sh
```
This syncs the environment if needed and starts the server with `uv`.

**Option 2: Run directly with `uv`**
```bash
uv run python run.py
```

**Option 3: Using uvicorn directly**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
jims_file_converter/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── converter.py     # CloudConvert integration
│   │   └── file_handler.py  # File upload/download logic
│   └── utils/
│       ├── __init__.py
│       └── validators.py    # File validation utilities
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   ├── js/
│   │   └── app.js           # Frontend logic
│   └── images/              # UI assets
├── templates/
│   └── index.html           # Main page
├── temp/                    # Temporary file storage (auto-generated)
├── .env                     # Environment variables (create this)
├── .gitignore
├── pyproject.toml
└── README.md
```

## Usage

1. Open the application in your browser
2. Drag and drop an image file or click to browse
3. Select the desired output format (JPEG, PNG, WebP, or GIF)
4. (Optional) Adjust quality or resize settings
5. Click "Convert"
6. Wait for the conversion to complete
7. Download your converted file automatically

## File Size Limits

- Maximum file size: 10MB (configurable)
- Supported formats: JPEG, JPG, PNG, WebP, GIF

## Security Notes

- Never commit your `.env` file or API keys to version control
- The app validates file types and sizes before upload
- Temporary files are automatically cleaned up after conversion
- API keys are stored securely in environment variables

## Development

To run in development mode with auto-reload:
```bash
uv run uvicorn app.main:app --reload
```

## Troubleshooting

**API Key Issues:**
- Make sure your `.env` file exists and contains valid CloudConvert API key
- Check that you haven't exceeded the free tier limit (25 conversions/day)

**File Upload Issues:**
- Check file size is under the limit
- Ensure file format is supported
- Check browser console for error messages

**Server Issues:**
- Ensure port 8000 is not already in use
- Check that all dependencies are installed correctly

**Rust/Cargo build errors on Windows (pydantic-core):**
- If `uv sync` asks for Rust/Cargo (e.g., during `pydantic-core` build), install Rust via https://rustup.rs/ and ensure `cargo` is on your PATH.
- Verify with:
  ```bash
  cargo --version
  ```
- Then re-run:
  ```bash
  uv sync --refresh
  ```
- If `cargo` is still not found, open a new terminal and add Rust to PATH (PowerShell):
  ```powershell
  $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
  ```
  Or persist for the user (PowerShell):
  ```powershell
  setx PATH "$env:USERPROFILE\.cargo\bin;$env:Path"
  ```
  CMD (current session):
  ```cmd
  set PATH=%USERPROFILE%\.cargo\bin;%PATH%
  ```
  Then retry:
  ```bash
  uv sync --refresh
  ```

**Windows MIME detection missing (`python-magic` skipped):**
- If you see `Ignoring python-magic: markers 'platform_system != "Windows"' don't match your environment` and MIME detection fails, install the Windows wheel:
  ```bash
  uv add "python-magic-bin==0.4.14"
  ```

**Virtual environment issues:**
- `uv` manages the project virtual environment automatically in `.venv`.
- Verify `python` comes from the project environment:
  ```bash
  uv run python -c "import sys; print(sys.prefix)"
  ```
- If it does not point to `.../.venv`, re-sync:
  ```bash
  uv sync
  ```

## License

MIT License - See LICENSE file for details
