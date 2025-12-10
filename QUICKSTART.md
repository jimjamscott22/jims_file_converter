# Quick Start Guide

Get Jim's File Converter running in 5 minutes!

## Step 1: Install Python Dependencies

Make sure you have Python 3.8+ installed, then run:

```bash
pip install -r requirements.txt
```

## Step 2: Get Your CloudConvert API Key

1. Go to [CloudConvert](https://cloudconvert.com/)
2. Sign up for a free account
3. Navigate to **Dashboard** > **API** > **API Keys**
4. Click "Create New API Key"
5. Copy your API key

**Free Tier:** 25 conversions per day (perfect for testing!)

## Step 3: Create Your `.env` File

Create a new file called `.env` in the root directory with this content:

```env
CLOUDCONVERT_API_KEY=paste_your_api_key_here
MAX_FILE_SIZE_MB=10
HOST=0.0.0.0
PORT=8000
```

**Important:** Replace `paste_your_api_key_here` with your actual API key from Step 2!

## Step 4: Run the Application

```bash
python run.py
```

You should see:

```
============================================================
🎨 Jim's File Converter
============================================================
Starting server at http://0.0.0.0:8000
Max file size: 10MB
Supported formats: jpg, jpeg, png, webp, gif
============================================================
```

## Step 5: Use the App!

1. Open your browser to `http://localhost:8000`
2. Drag and drop an image or click to browse
3. Select your desired output format
4. Click "Convert Image"
5. Download your converted file!

## Troubleshooting

### "CloudConvert API key not configured"
- Make sure your `.env` file exists in the root directory
- Check that `CLOUDCONVERT_API_KEY` is set correctly
- Restart the server after creating the `.env` file

### "Port 8000 already in use"
- Change the `PORT` in your `.env` file to something else (e.g., 8080)
- Or stop the process using port 8000

### Import Errors
- Make sure you installed all dependencies: `pip install -r requirements.txt`
- Try creating a virtual environment first

### File Upload Fails
- Check that your file is under 10MB
- Ensure it's a supported format (JPEG, PNG, WebP, GIF)
- Look at the browser console for detailed error messages

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize the `MAX_FILE_SIZE_MB` in your `.env` file
- Explore the code in the `app/` directory
- Modify the UI in `templates/index.html` and `static/css/style.css`

Enjoy converting your images! 🎨

