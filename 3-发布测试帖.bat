@echo off
chcp 65001 >nul
cd /d "%~dp0"
set /p ACC=请输入要用来发帖的账号名字（和登录时一样），然后按回车：
python -m xhs.publish post posts\example --account %ACC%
pause
