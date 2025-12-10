# Setup Checklist ✅

Follow this checklist to get Jim's File Converter up and running.

## Prerequisites

### Step 1: Verify Python Installation
```bash
python --version
```
✅ Should show Python 3.8 or higher

If not installed:
- Windows: Download from [python.org](https://www.python.org/downloads/)
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3`

---

## Installation

### Step 2: Create Virtual Environment (Recommended)

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ You should see `(venv)` in your terminal prompt

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

✅ Should install without errors

**Common Issues**:
- If `pip` not found, try `python -m pip install -r requirements.txt`
- If permission errors, add `--user` flag
- If Windows errors with python-magic, it should auto-install `python-magic-bin`

---

## Configuration

### Step 4: Get CloudConvert API Key

1. ✅ Go to [cloudconvert.com](https://cloudconvert.com/)
2. ✅ Sign up for free account
3. ✅ Navigate to Dashboard → API → API Keys
4. ✅ Click "Create New API Key"
5. ✅ Copy the key (starts with "eyJ...")

**Free Tier**: 25 conversions per day

---

### Step 5: Create `.env` File

1. ✅ Create a new file named `.env` in the root directory
2. ✅ Add this content:

```env
CLOUDCONVERT_API_KEY=paste_your_key_here
MAX_FILE_SIZE_MB=10
HOST=0.0.0.0
PORT=8000
```

3. ✅ Replace `paste_your_key_here` with your actual API key
4. ✅ Save the file

**Important Notes**:
- File must be named exactly `.env` (with the dot at the start)
- No spaces around the `=` sign
- No quotes around the values
- Keep this file secret (never commit to git)

---

## Testing

### Step 6: Start the Server

```bash
python run.py
```

✅ You should see:
```
============================================================
🎨 Jim's File Converter
============================================================
Starting server at http://0.0.0.0:8000
Max file size: 10MB
Supported formats: jpg, jpeg, png, webp, gif
============================================================
```

❌ If you see "CloudConvert API key not configured", check your `.env` file

---

### Step 7: Test in Browser

1. ✅ Open browser to `http://localhost:8000`
2. ✅ You should see the Jim's File Converter homepage
3. ✅ Page should have a drag-and-drop area

---

### Step 8: Test API Health

Open in browser: `http://localhost:8000/api/health`

✅ Should show:
```json
{
  "status": "healthy",
  "api_configured": true,
  "supported_formats": ["jpg", "jpeg", "png", "webp", "gif"],
  "max_file_size_mb": 10
}
```

❌ If `"api_configured": false`, check your `.env` file

---

### Step 9: Test File Conversion

1. ✅ Find a small test image (JPEG, PNG, etc.)
2. ✅ Drag and drop it onto the upload area
3. ✅ You should see a preview of the image
4. ✅ Select an output format (e.g., PNG)
5. ✅ Click "Convert Image"
6. ✅ Wait for conversion (should take 5-30 seconds)
7. ✅ Download button should appear
8. ✅ Click download and verify the converted file

---

## Verification Checklist

### ✅ All Systems Go!

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] CloudConvert account created
- [ ] API key obtained
- [ ] `.env` file created with valid API key
- [ ] Server starts without errors
- [ ] Homepage loads in browser
- [ ] API health check shows `"api_configured": true`
- [ ] Test file conversion works end-to-end
- [ ] Downloaded file opens correctly

---

## Project Structure Verification

Your directory should look like this:

```
jims_file_converter/
├── app/                    ✅ Backend code
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── services/
│   └── utils/
├── static/                 ✅ Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              ✅ HTML templates
│   └── index.html
├── venv/                   ✅ Virtual environment (if created)
├── temp/                   ✅ Auto-created on first run
├── .env                    ✅ YOUR CONFIG (create this!)
├── .gitignore             ✅ Git ignore rules
├── requirements.txt        ✅ Dependencies
├── run.py                  ✅ Startup script
├── README.md              ✅ Full documentation
├── QUICKSTART.md          ✅ Quick start guide
├── TECHNICAL_DECISIONS.md ✅ Architecture docs
├── PROJECT_SUMMARY.md     ✅ Project overview
├── TROUBLESHOOTING.md     ✅ Common issues
├── SETUP_CHECKLIST.md     ✅ This file
└── LICENSE                ✅ MIT License
```

---

## Quick Test Commands

### Test Server is Running
```bash
curl http://localhost:8000/ping
```
Expected: `{"message":"pong"}`

### Test API Health
```bash
curl http://localhost:8000/api/health
```
Expected: JSON with `"status": "healthy"`

### Test Supported Formats
```bash
curl http://localhost:8000/api/formats
```
Expected: JSON with list of formats

---

## Common Setup Issues

### ❌ "Module not found" errors
**Fix**: `pip install -r requirements.txt`

### ❌ "Port already in use"
**Fix**: Change `PORT=8080` in `.env`

### ❌ "API key not configured"
**Fix**: Check `.env` file exists and has correct key

### ❌ "Permission denied"
**Fix**: Use virtual environment or add `--user` to pip install

### ❌ Page doesn't load
**Fix**: Check server is running and URL is `http://localhost:8000`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help.

---

## Next Steps

Once everything is working:

1. 📖 Read [README.md](README.md) for full documentation
2. 🔧 Read [TECHNICAL_DECISIONS.md](TECHNICAL_DECISIONS.md) to understand the architecture
3. 🎨 Customize the UI in `static/css/style.css`
4. 🚀 Add new features or improvements
5. 📝 Consider adding tests
6. 🌐 Deploy to production (Heroku, Railway, etc.)

---

## Getting Help

If you're stuck:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Look at server terminal for error messages
3. Check browser console (F12 → Console)
4. Verify all checklist items above
5. Try with a fresh virtual environment

---

## Success! 🎉

If all checklist items are complete, you're ready to start converting images!

**Enjoy your new file converter!** 🚀

---

## Development Mode

For development with auto-reload:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python run.py
```

The `run.py` script includes `--reload` by default.

---

## Production Deployment

For production, see the deployment section in [TECHNICAL_DECISIONS.md](TECHNICAL_DECISIONS.md).

Quick options:
- **Railway**: `railway up`
- **Heroku**: Add `Procfile` and `git push heroku main`
- **Docker**: Build and run container
- **VPS**: Use Gunicorn + Nginx

---

**Remember**: Never commit your `.env` file or API keys to version control! 🔒

