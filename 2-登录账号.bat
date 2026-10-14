@echo off
chcp 65001 >nul
cd /d "%~dp0"
set /p ACC=请输入账号名字（随便起，比如 主号），然后按回车：
python -m xhs.publish login %ACC%
pause
