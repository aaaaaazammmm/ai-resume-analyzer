# ⚡ Quick Start Guide

Get your AI Resume Analyzer up and running in 5 minutes!

## 🎯 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9 or higher installed
- ✅ pip package manager
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Terminal/Command Prompt access
- ✅ Text editor (VS Code, Sublime, etc.)

## 🚀 Installation Steps

### Step 1: Setup Environment (2 minutes)

```bash
# Navigate to project directory
cd resume_matcher

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 2: Install Dependencies (2 minutes)

```bash
# Install all required packages
pip install -r requirements.txt

# This will install ~20 packages including:
# - FastAPI, Streamlit
# - OpenAI, LangChain
# - SentenceTransformers, FAISS
# - And more...

# Wait for installation to complete
```

### Step 3: Configure API Key (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# On Windows:
notepad .env
# On macOS:
nano .env
# On Linux:
nano .env

# Add your OpenAI API key:
# OPENAI_API_KEY=sk-your-actual-api-key-here
# Save and close the file
```

### Step 4: Test Installation (30 seconds)

```bash
# Run test script
python test_setup.py

# You should see:
# ✅ All packages installed successfully!
# ✅ Environment configured correctly!
# ✅ Embedding model working!
# ✅ FAISS working correctly!
# ✅ OpenAI connection working!
# 🎉 ALL TESTS PASSED! 🎉
```

### Step 5: Start Backend (1 minute)

**Open Terminal/Command Prompt #1:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in prompt

# Start FastAPI backend
python -m backend.main

# Wait for:
# "Loading embedding model..." (first run may take 30 seconds)
# "✓ All services initialized successfully!"
# "Uvicorn running on http://0.0.0.0:8000"

# Leave this terminal running!
```

### Step 6: Start Frontend (30 seconds)

**Open Terminal/Command Prompt #2:**
```bash
# Navigate to project directory
cd resume_matcher

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start Streamlit frontend
streamlit run frontend/app.py

# Browser should open automatically to http://localhost:8501
# If not, open browser and go to that URL
```

## 🎉 You're Ready!

You should now see:
1. **Backend running** in Terminal 1 (http://localhost:8000)
2. **Frontend open** in your browser (http://localhost:8501)
3. **Beautiful UI** with upload button and text area

## 📝 First Test

### Using the Application:

1. **Get a sample resume PDF**
   - Use your own resume
   - Or create a test PDF with skills like: Python, FastAPI, Machine Learning

2. **Find a job description**
   - Copy from any job board (LinkedIn, Indeed, etc.)
   - Should mention skills like: Python, AWS, Docker, etc.

3. **Analyze:**
   - Click "Choose your resume PDF" → Upload file
   - Paste job description in text area
   - Click "🚀 Analyze Resume"
   - Wait 10-20 seconds for analysis

4. **View Results:**
   - Match Score percentage
   - Matched vs Missing skills
   - Strengths and suggestions
   - Full summary

## 🔍 Verify Setup

### Check Backend API:
Open http://localhost:8000/docs in browser
- You should see Swagger UI
- Interactive API documentation

### Check Frontend:
Open http://localhost:8501
- Should see "AI Resume Analyzer & Job Matcher"
- Sidebar with "API Status: ✅ Connected"

## ⚠️ Common Issues

### "Module not found" error
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "OPENAI_API_KEY not found"
```bash
# Solution: Check .env file exists and has correct key
cat .env  # On Windows: type .env
# Should show: OPENAI_API_KEY=sk-...
```

### "API Unavailable" in Streamlit
```bash
# Solution: Make sure backend is running
# Check Terminal 1 - should show "Uvicorn running..."
# If not, restart: python -m backend.main
```

### Port already in use
```bash
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <number> /F

# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

## 📚 Next Steps

Now that it's working:

1. **Read Full Documentation:**
   - `README.md` - Complete guide
   - `DEPLOYMENT.md` - Production setup

2. **Customize:**
   - Change LLM model in `.env` (gpt-4 for better results)
   - Adjust chunk sizes in `backend/rag.py`
   - Modify UI colors in `frontend/app.py`

3. **Test More:**
   - Try different resumes
   - Various job descriptions
   - Check API docs: http://localhost:8000/docs

4. **Deploy:**
   - Follow `DEPLOYMENT.md` for production
   - Set up on AWS, DigitalOcean, or Heroku

## 🆘 Still Having Issues?

1. **Run diagnostic:**
   ```bash
   python test_setup.py
   ```

2. **Check logs:**
   - Backend: Look at Terminal 1 output
   - Frontend: Look at Terminal 2 output

3. **Verify versions:**
   ```bash
   python --version  # Should be 3.9+
   pip --version
   ```

4. **Clean install:**
   ```bash
   # Remove virtual environment
   rm -rf venv  # On Windows: rmdir /s venv
   
   # Start over from Step 1
   ```

## 💡 Pro Tips

1. **Keep both terminals open** - Backend and Frontend must run simultaneously

2. **Use good quality PDFs** - Text-based, not scanned images

3. **Detailed job descriptions work better** - More keywords = better analysis

4. **First run is slower** - Downloads embedding model (~80MB)

5. **Check API status** - Green checkmark in sidebar = all good

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://docs.streamlit.io/
- **LangChain**: https://python.langchain.com/
- **OpenAI**: https://platform.openai.com/docs

## ✅ Checklist

Before using in production:

- [ ] All tests pass (`python test_setup.py`)
- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] API status shows "Connected"
- [ ] Can upload PDF successfully
- [ ] Analysis completes in <30 seconds
- [ ] Results display correctly
- [ ] `.env` has real API key (not placeholder)
- [ ] Read full documentation
- [ ] Understand API costs (~$0.004 per analysis)

---

**🎉 Congratulations! You're now ready to analyze resumes with AI!**

**Need help?** Check the Troubleshooting section in README.md

**Want to contribute?** See README.md for guidelines
