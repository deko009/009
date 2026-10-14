#!/bin/bash
cd "$(dirname "$0")"
read -p "请输入账号名字（随便起，比如 主号），然后按回车：" ACC
python3 -m xhs.publish login "$ACC"
read -p "按回车关闭..."
