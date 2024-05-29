@echo off
setlocal

REM ���� Python �������ӺͰ�װ�ļ���
set PYTHON_VERSION=3.12.3
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

REM ��� Python �Ƿ��Ѱ�װ
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading Python %PYTHON_VERSION% installer...
    
    REM ���� Python ��װ����
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
    
    if exist %PYTHON_INSTALLER% (
        echo Installing Python %PYTHON_VERSION%...
        
        REM ��װ Python
        start /wait "" %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
        
        REM ɾ����װ�ļ�
        del %PYTHON_INSTALLER%
        
        REM ��鰲װ�Ƿ�ɹ�
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo Failed to install Python. Please install it manually.
            exit /b 1
        )
    ) else (
        echo Failed to download Python installer. Please check your internet connection.
        exit /b 1
    )
)

REM ���� main.py
echo Python is installed. Running main.py...
python main.py

endlocal
