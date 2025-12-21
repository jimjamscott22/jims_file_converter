# Building Windows Executable

This guide explains how to build a standalone Windows executable (.exe) for Jim's File Converter.

## Prerequisites

- Python 3.8 or higher
- All project dependencies installed (`pip install -r requirements.txt`)
- PyInstaller installed (`pip install pyinstaller`)

## Quick Build

1. **Activate your virtual environment:**
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Run the build script:**
   ```bash
   python build_exe.py
   ```

3. **Wait for the build to complete** (may take 2-5 minutes)

4. **Find your executable:**
   ```
   dist/JimsFileConverter.exe
   ```

## Running the Executable

### First Time Setup

1. **Copy the .env file** to the same folder as the executable:
   ```
   dist/
   ├── JimsFileConverter.exe
   └── .env  ← Copy this from your project root
   ```

2. **Double-click `JimsFileConverter.exe`** to run

3. The application will:
   - Start a local web server
   - Automatically open your default browser
   - Display the file converter interface

### What Gets Created

When you run the executable, it will create a `temp/` folder in the same directory for storing temporary conversion files.

```
dist/
├── JimsFileConverter.exe
├── .env
└── temp/  ← Auto-created for temporary files
```

## Distribution

To share the application with others:

1. **Create a distribution folder:**
   ```
   JimsFileConverter/
   ├── JimsFileConverter.exe
   └── .env.example  ← Rename from .env, remove your API key
   ```

2. **Include instructions** for users to:
   - Get their own CloudConvert API key
   - Rename `.env.example` to `.env`
   - Add their API key to the `.env` file

## Troubleshooting

### Build Issues

**"Module not found" errors during build:**
```bash
pip install --no-cache-dir -r requirements.txt
python build_exe.py
```

**Build succeeds but exe crashes:**
- Use `--console` instead of `--windowed` in `build_exe.py` to see error messages
- Check that all dependencies are installed
- Ensure your code works with `python run.py` before building

### Runtime Issues

**".env file not found" error:**
- Make sure `.env` is in the same folder as the executable
- Check that the file is named exactly `.env` (not `.env.txt`)

**"API key invalid" errors:**
- Verify your CloudConvert API key in the `.env` file
- Check you haven't exceeded your API quota

**Port already in use:**
- Change the PORT in your `.env` file to a different number (e.g., 8001, 8080)

**Antivirus blocks the exe:**
- PyInstaller executables can trigger false positives
- Add an exception in your antivirus software
- Alternatively, run the Python script directly with `python run.py`

## Advanced Options

### Build with Console Window (for debugging)

Edit `build_exe.py` and change:
```python
'--windowed',  # Change to '--console'
```

### Build Directory Instead of Single File

For faster startup, build as a directory:
```python
'--onefile',  # Remove this line
```
This creates a `dist/JimsFileConverter/` folder with multiple files.

### Add Custom Icon

1. Create or download an `.ico` file
2. Save it as `static/images/icon.ico`
3. The build script will automatically use it

## Clean Build

To start fresh:
```bash
# Remove build artifacts
rmdir /s /q build dist
del /f /q *.spec

# Rebuild
python build_exe.py
```

## File Size

The executable will be approximately 40-80 MB due to including:
- Python runtime
- All dependencies (FastAPI, uvicorn, cloudconvert, etc.)
- Your application code and assets

This is normal for PyInstaller applications.

## Security Notes

- **Never distribute your .env file with your actual API key**
- The executable contains your code but not your secrets
- Users need their own CloudConvert API keys
- Consider creating an installer for easier distribution

## Creating a Shortcut

For easy access:

1. Right-click `JimsFileConverter.exe`
2. Select "Create shortcut"
3. Move the shortcut to your Desktop or Start Menu
4. Rename it to "Jim's File Converter"

Now you can launch it with a single click!
