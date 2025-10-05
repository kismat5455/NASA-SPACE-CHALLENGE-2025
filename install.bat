@echo off
echo =========================================================
echo NASA RAG System - Windows Installation Script
echo =========================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Checking configuration...
if not exist .env (
    echo Creating .env file template...
    copy env_template.txt .env
    echo.
    echo IMPORTANT: Edit .env file and add your Gemini API key
    echo Get your key from: https://makersuite.google.com/app/apikey
    echo.
)

echo.
echo Step 3: Creating directories...
if not exist data mkdir data
if not exist vector_store mkdir vector_store

echo.
echo =========================================================
echo Installation Complete!
echo =========================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Google API key
echo 2. Add NASA documents to the data/ folder
echo 3. Run: python document_ingestion.py
echo 4. Run: streamlit run app.py
echo.
echo Run 'python quickstart.py' to verify your setup
echo.
pause

