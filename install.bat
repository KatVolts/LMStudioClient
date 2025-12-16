@echo off
echo ==========================================
echo   Setting up LMStudioClient Library
echo ==========================================

:: 1. Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found! 
    echo Please install Python and check "Add to PATH" in the installer.
    pause
    exit /b
)

:: 2. Upgrade pip to ensure it handles pyproject.toml correctly
echo.
echo [1/2] Upgrading pip...
python -m pip install --upgrade pip

:: 3. Install the current directory in editable mode
echo.
echo [2/2] Installing LMStudioClient...
pip install -e .

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. See error messages above.
) else (
    echo.
    echo [SUCCESS] Library installed! You can now import 'lm_studio_client' in any script.
)

pause