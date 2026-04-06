"""
Convenient startup script for Jim's File Converter.
Run this file to start the application.
"""

import socket
import sys
try:
    import uvicorn
except ImportError:
    print("The 'uvicorn' package is not installed. Install project dependencies with: uv sync")
    sys.exit(1)
from app.config import settings


def _find_available_port(host: str, preferred_port: int, max_attempts: int = 20) -> int:
    """Find an available port, starting with preferred_port."""
    for offset in range(max_attempts):
        candidate = preferred_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, candidate))
                return candidate
            except OSError:
                continue

    raise RuntimeError(
        f"Could not find an available port in range {preferred_port}-{preferred_port + max_attempts - 1}."
    )

if __name__ == "__main__":
    selected_port = _find_available_port(settings.host, settings.port)

    if selected_port != settings.port:
        print(
            f"Configured port {settings.port} is in use. Falling back to available port {selected_port}."
        )

    print("=" * 60)
    print("🎨 Jim's File Converter")
    print("=" * 60)
    print(f"Starting server at http://{settings.host}:{selected_port}")
    print(f"Max file size: {settings.max_file_size_mb}MB")
    print(f"Supported formats: {', '.join(settings.supported_formats)}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=selected_port,
        reload=True
    )
