#!/bin/bash
cd "$(dirname "$0")"
echo "正在安装，需要几分钟，请不要关闭窗口..."
python3 -m pip install -r requirements.txt || { echo "没找到 Python！请先到 python.org 安装 Python"; read -p "按回车关闭..."; exit 1; }
python3 -m playwright install chromium
echo "安装完成！"; read -p "按回车关闭..."
