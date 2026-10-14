#!/bin/bash
cd "$(dirname "$0")"
read -p "请输入要用来发帖的账号名字（和登录时一样），然后按回车：" ACC
python3 -m xhs.publish post posts/example --account "$ACC"
read -p "按回车关闭..."
