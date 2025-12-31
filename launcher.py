"""
Launcher script for the executable version of Jim's File Converter.
This script starts the web server and opens the browser.
"""

import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

# Handle PyInstaller bundled resources
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
    ORIGINAL_DIR = Path(os.path.dirname(sys.executable))
else:
    # Running as script
    BASE_DIR = Path(__file__).resolve().parent
    ORIGINAL_DIR = BASE_DIR

# Add the base directory to Python path
sys.path.insert(0, str(BASE_DIR))

# Set environment variables for the bundled app
os.environ['BASE_DIR'] = str(BASE_DIR)

# Import after path setup
import uvicorn
from app.config import settings
from app.main import app

def open_browser(url, delay=2):
    """Open browser after a short delay."""
    time.sleep(delay)
    webbrowser.open(url)

def main():
    """Main entry point for the launcher."""
    print("=" * 60)
    print("[*] Jim's File Converter")
    print("=" * 60)
    
    # Check for .env file
    env_file = ORIGINAL_DIR / ".env"
    if not env_file.exists():
        print("\n[!] WARNING: .env file not found!")
        print(f"Please create a .env file in: {ORIGINAL_DIR}")
        print("\nThe .env file should contain:")
        print("CLOUDCONVERT_API_KEY=your_api_key_here")
        print("MAX_FILE_SIZE_MB=10")
        print("HOST=127.0.0.1")
        print("PORT=8000")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
    
    # Create temp directory in the original location
    temp_dir = ORIGINAL_DIR / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    # Override settings to use the original directory for temp files
    settings.temp_dir = temp_dir
    
    url = f"http://127.0.0.1:{settings.port}"
    
    print(f"[>] Starting server at {url}")
    print(f"[>] Temp directory: {temp_dir}")
    print(f"[>] Max file size: {settings.max_file_size_mb}MB")
    print(f"[>] Supported formats: {', '.join(settings.supported_formats)}")
    print("=" * 60)
    print("\n[+] Browser will open automatically...")
    print("[x] Close this window to stop the server\n")
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, args=(url,))
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the server
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",  # Use localhost for exe
            port=settings.port,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n[*] Shutting down...")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)

if __name__ == "__main__":
    main()
