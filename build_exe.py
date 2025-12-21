"""
Build script for creating Windows executable with PyInstaller.
Run this script to build the executable: python build_exe.py
"""

import PyInstaller.__main__
import shutil
from pathlib import Path

# Clean previous builds
if Path("build").exists():
    shutil.rmtree("build")
if Path("dist").exists():
    shutil.rmtree("dist")

print("Building Jim's File Converter executable...")
print("This may take a few minutes...")

# Build PyInstaller arguments
pyinstaller_args = [
    'launcher.py',                       # Main script
    '--name=JimsFileConverter',          # Name of the executable
    '--onefile',                         # Single executable file
    '--windowed',                        # No console window (use --console for debugging)
    '--add-data=static;static',          # Include static folder
    '--add-data=templates;templates',    # Include templates folder
    '--add-data=app;app',                # Include app folder
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.protocols.websockets',
    '--hidden-import=uvicorn.protocols.websockets.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    '--collect-all=cloudconvert',
    '--collect-all=fastapi',
    '--collect-all=pydantic',
    '--collect-all=starlette',
    '--noconfirm',
]

# Add icon if it exists
icon_path = Path('static/images/icon.ico')
if icon_path.exists():
    pyinstaller_args.append(f'--icon={icon_path}')
    print(f"✓ Using custom icon: {icon_path}")
else:
    print("ℹ Using default icon (no custom icon found)")

# Add .env if it exists (but don't include in production builds)
if Path('.env').exists():
    print("⚠️  Note: .env file will NOT be included in the executable")
    print("   You'll need to create a .env file next to the .exe")

# PyInstaller command
PyInstaller.__main__.run(pyinstaller_args)

print("\n" + "="*60)
print("✅ Build complete!")
print("="*60)
print("Your executable is in the 'dist' folder:")
print("  dist/JimsFileConverter.exe")
print("\nTo run the application, double-click JimsFileConverter.exe")
print("="*60)
