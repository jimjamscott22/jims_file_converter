# Troubleshooting Guide

Common issues and their solutions for Jim's File Converter.

## Setup Issues

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Problem**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

If that doesn't work, try:
```bash
python -m pip install -r requirements.txt
```

---

### ❌ "CloudConvert API key not configured"

**Problem**: `.env` file missing or API key not set

**Solution**:
1. Create a file named `.env` in the root directory
2. Add this content:
```env
CLOUDCONVERT_API_KEY=your_actual_api_key_here
MAX_FILE_SIZE_MB=10
HOST=0.0.0.0
PORT=8000
```
3. Get your API key from: https://cloudconvert.com/dashboard/api/v2/keys
4. Replace `your_actual_api_key_here` with your real key
5. Restart the server

---

### ❌ "Address already in use" or "Port 8000 is already in use"

**Problem**: Another application is using port 8000

**Solution 1** - Change the port:
Edit `.env` file:
```env
PORT=8080
```

**Solution 2** - Stop the other process:

**Windows**:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Mac/Linux**:
```bash
lsof -ti:8000 | xargs kill -9
```

---

### ❌ "python: command not found"

**Problem**: Python not in PATH or not installed

**Solution**:
- **Windows**: Try `py` instead of `python`
  ```bash
  py run.py
  ```
- **Mac/Linux**: Try `python3`
  ```bash
  python3 run.py
  ```
- If still not working, reinstall Python from python.org

---

## Runtime Issues

### ❌ File Upload Fails with "File too large"

**Problem**: File exceeds size limit

**Solution**:
1. Check your file size (right-click → Properties)
2. Default limit is 10MB
3. To increase, edit `.env`:
```env
MAX_FILE_SIZE_MB=20
```
4. Restart the server

**Note**: CloudConvert free tier may have its own limits

---

### ❌ "Unsupported file format"

**Problem**: File type not supported

**Solution**:
- Supported formats: JPEG, JPG, PNG, WebP, GIF
- Check file extension is correct
- Try opening the file in an image viewer to verify it's valid
- Some files may have wrong extensions (e.g., .jpg but actually .png)

---

### ❌ Conversion Fails with "Conversion failed: ..."

**Problem**: CloudConvert API error

**Common Causes**:

1. **API Key Invalid**
   - Verify your API key in `.env`
   - Check it's copied correctly (no extra spaces)
   - Try generating a new key

2. **Free Tier Limit Reached**
   - Free tier: 25 conversions/day
   - Wait 24 hours or upgrade plan
   - Check usage at: https://cloudconvert.com/dashboard

3. **Network Issues**
   - Check internet connection
   - Try again in a few minutes
   - Check CloudConvert status page

4. **Invalid Image File**
   - File may be corrupted
   - Try opening in image editor first
   - Try a different image

---

### ❌ "File not found" when downloading

**Problem**: Converted file was deleted or expired

**Solution**:
- Files are automatically cleaned up after 2 hours
- Download immediately after conversion
- If this happens frequently, increase cleanup time in `app/services/file_handler.py`:
```python
await file_handler.cleanup_old_files(max_age_hours=4)  # Change from 2 to 4
```

---

### ❌ Page doesn't load / "Connection refused"

**Problem**: Server not running or wrong URL

**Solution**:
1. Check server is running (look for startup message in terminal)
2. Verify URL: `http://localhost:8000` (not https)
3. Check the port in `.env` matches the URL
4. Try `http://127.0.0.1:8000` instead

---

## Browser Issues

### ❌ Drag and Drop Not Working

**Problem**: Browser compatibility or JavaScript disabled

**Solution**:
1. Try a modern browser (Chrome, Firefox, Edge, Safari)
2. Check JavaScript is enabled
3. Try clicking "Browse Files" instead
4. Check browser console for errors (F12 → Console tab)

---

### ❌ "Nothing happens" when clicking Convert

**Problem**: JavaScript error or network issue

**Solution**:
1. Open browser console (F12 → Console tab)
2. Look for error messages
3. Check network tab for failed requests
4. Try refreshing the page (Ctrl+F5)
5. Clear browser cache

---

### ❌ Progress bar stuck at 90%

**Problem**: Conversion taking longer than expected

**Solution**:
- Large files take longer
- Wait up to 2 minutes
- Check server terminal for errors
- If stuck >2 minutes, refresh and try again
- Try a smaller file to test

---

## Development Issues

### ❌ Changes to Python code not reflecting

**Problem**: Server not reloading

**Solution**:
1. Stop server (Ctrl+C)
2. Restart: `python run.py`
3. If using `--reload` flag, check for syntax errors preventing reload

---

### ❌ Changes to CSS/JS not reflecting

**Problem**: Browser cache

**Solution**:
1. Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear browser cache
3. Open DevTools (F12) → Network tab → Check "Disable cache"
4. Try incognito/private window

---

### ❌ "temp/" directory fills up

**Problem**: Cleanup not running or too many conversions

**Solution**:
1. Manually delete files in `temp/` folder
2. Check background cleanup task is running
3. Reduce cleanup interval in `app/main.py`:
```python
await asyncio.sleep(1800)  # 30 minutes instead of 1 hour
```

---

## API Issues

### ❌ "Network error during conversion"

**Problem**: Cannot reach CloudConvert API

**Solution**:
1. Check internet connection
2. Verify CloudConvert is up: https://status.cloudconvert.com/
3. Check firewall isn't blocking requests
4. Try again in a few minutes

---

### ❌ "Failed to create job: Unauthorized"

**Problem**: Invalid API key

**Solution**:
1. Verify API key in `.env` file
2. Check for extra spaces or quotes
3. Generate new API key at CloudConvert dashboard
4. Make sure you're using API v2 key (not v1)

---

### ❌ "Failed to create job: Payment Required"

**Problem**: Free tier exceeded or expired

**Solution**:
1. Check your CloudConvert dashboard for usage
2. Free tier: 25 conversions/day
3. Wait 24 hours for reset
4. Or upgrade to paid plan

---

## Windows-Specific Issues

### ❌ "python-magic" installation fails

**Problem**: python-magic-bin not installing correctly

**Solution**:
```bash
pip install python-magic-bin --force-reinstall
```

Or remove from `requirements.txt` temporarily (MIME validation will be skipped)

---

### ❌ Virtual environment activation fails

**Problem**: PowerShell execution policy

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```bash
venv\Scripts\activate
```

---

## Mac/Linux-Specific Issues

### ❌ "Permission denied" when running scripts

**Problem**: File not executable

**Solution**:
```bash
chmod +x run.py
python3 run.py
```

---

### ❌ "python-magic" not working

**Problem**: libmagic not installed

**Solution**:

**Mac**:
```bash
brew install libmagic
```

**Ubuntu/Debian**:
```bash
sudo apt-get install libmagic1
```

---

## Still Having Issues?

### Debug Checklist

1. ✅ Python 3.8+ installed?
2. ✅ All dependencies installed? (`pip install -r requirements.txt`)
3. ✅ `.env` file created with valid API key?
4. ✅ Server running without errors?
5. ✅ Correct URL? (`http://localhost:8000`)
6. ✅ Modern browser with JavaScript enabled?
7. ✅ Internet connection working?
8. ✅ CloudConvert API key valid and within limits?

### Getting Help

1. **Check server terminal** for error messages
2. **Check browser console** (F12 → Console) for errors
3. **Test with a small, simple image** (e.g., 100KB PNG)
4. **Try the health check**: `http://localhost:8000/api/health`
5. **Review the logs** in the terminal where you started the server

### Useful Commands for Debugging

**Check if server is running**:
```bash
curl http://localhost:8000/ping
```

**Check API health**:
```bash
curl http://localhost:8000/api/health
```

**Check supported formats**:
```bash
curl http://localhost:8000/api/formats
```

**View Python version**:
```bash
python --version
```

**View installed packages**:
```bash
pip list
```

---

## Prevention Tips

1. **Always use a virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Monitor CloudConvert usage**
   - Check dashboard regularly
   - Set up usage alerts

4. **Regular cleanup**
   - Clear `temp/` folder occasionally
   - Monitor disk space

5. **Test after changes**
   - Test with a simple file after any code changes
   - Check both success and error cases

---

## Contact & Resources

- **CloudConvert Support**: https://cloudconvert.com/support
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Python Docs**: https://docs.python.org/3/

---

**Remember**: Most issues are simple configuration problems. Check your `.env` file and API key first! 🔑

