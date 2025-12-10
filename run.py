"""
Convenient startup script for Jim's File Converter.
Run this file to start the application.
"""

import sys
try:
    import uvicorn
except ImportError:
    print("The 'uvicorn' package is not installed. Install it with: pip install uvicorn[standard]")
    sys.exit(1)
from app.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Jim's File Converter")
    print("=" * 60)
    print(f"Starting server at http://{settings.host}:{settings.port}")
    print(f"Max file size: {settings.max_file_size_mb}MB")
    print(f"Supported formats: {', '.join(settings.supported_formats)}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

