# Jim's File Converter

A modern web-based image conversion tool that supports converting between JPEG, PNG, WebP, and GIF formats.

## Features

- 🎯 Simple drag-and-drop file upload
- 🔄 Convert between JPEG, PNG, WebP, and GIF
- 📱 Responsive design for mobile and desktop
- ⚡ Fast conversion using CloudConvert API
- 🎨 Clean, modern UI
- 📊 Real-time progress tracking

## Tech Stack

- **Backend:** Python with FastAPI
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **API:** CloudConvert for file conversion
- **File Storage:** Temporary local storage with automatic cleanup

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- CloudConvert API key (free tier available)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jims_file_converter
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```env
CLOUDCONVERT_API_KEY=your_api_key_here
MAX_FILE_SIZE_MB=10
HOST=0.0.0.0
PORT=8000
```
   **Note:** Simply create a new file named `.env` (with the dot at the beginning) in the root folder.

5. Get your CloudConvert API key:
   - Sign up at https://cloudconvert.com/
   - Navigate to Dashboard > API
   - Copy your API key and add it to the `.env` file

### Running the Application

**Option 1: Using the run script (Recommended)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
├── requirements.txt
└── README.md
```

## Usage

1. Open the application in your browser
2. Drag and drop an image file or click to browse
3. Select the desired output format (JPEG, PNG, WebP, or GIF)
4. Click "Convert"
5. Wait for the conversion to complete
6. Download your converted file automatically

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
python -m uvicorn app.main:app --reload
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

## License

MIT License - See LICENSE file for details

