@echo off
setlocal

REM 设置 Python 下载链接和安装文件名
set PYTHON_VERSION=3.12.3
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

REM 检查 Python 是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading Python %PYTHON_VERSION% installer...
    
    REM 下载 Python 安装程序
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
    
    if exist %PYTHON_INSTALLER% (
        echo Installing Python %PYTHON_VERSION%...
        
        REM 安装 Python
        start /wait "" %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
        
        REM 删除安装文件
        del %PYTHON_INSTALLER%
        
        REM 检查安装是否成功
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

REM 启动 main.py
echo Python is installed. Running main.py...
python main.py

endlocal
