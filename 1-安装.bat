@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在安装，需要几分钟，请不要关闭窗口...
python -m pip install -r requirements.txt || (echo. & echo 没找到 Python！请先安装 Python，安装时勾选 "Add Python to PATH" & pause & exit /b)
python -m playwright install chromium
echo.
echo 安装完成！
pause
