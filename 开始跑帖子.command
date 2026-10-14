#!/bin/bash
# 双击打开：在这个文件夹里启动 Claude Code，然后直接把网址发给它
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"
if ! command -v claude >/dev/null 2>&1; then
  echo "第一次使用，正在安装 Claude Code..."
  curl -fsSL https://claude.ai/install.sh | bash || { echo "安装失败，请截图发给 Claude"; read -p "按回车关闭..."; exit 1; }
  export PATH="$HOME/.local/bin:$PATH"
fi
python3 -m pip install -q -r requirements.txt
echo ""
echo "✅ 准备好了。在下面输入：跑帖子 + 网址，比如：跑帖子 https://www.wwake.com"
echo ""
claude
