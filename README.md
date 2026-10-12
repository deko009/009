# 009 · 小红书 ins 风帖子自动化

流程：**网站 → 剪贴素材 → Figma 排版 → 写文案 → 多账号发布**
完整规则见 `.claude/skills/xhs-ins-post/SKILL.md`（风格 / 文案 / 账号分配部分需要你填）。

## 本地安装（自己电脑）
```bash
pip install -r requirements.txt
playwright install chromium
```

## 使用
```bash
# 1. 剪贴素材
python -m xhs.clip https://example.com/xxx --name 春季新品

# 2. 每个账号首次扫码登录（登录状态保存在 accounts/<账号>/，不会上传 git）
python -m xhs.publish login 账号A
python -m xhs.publish login 账号B

# 3. 发布
python -m xhs.publish post posts/example          # 填好后你手动点发布
python -m xhs.publish post posts/example --auto   # 全自动
python -m xhs.publish run                         # 按队列发布所有未发布帖子
```

## 防封建议
- 默认“半自动”：脚本填好内容，你点发布，最安全
- 同一账号每天 1–3 篇，队列默认间隔 20–60 分钟
- 不同账号尽量用不同网络/设备；不要发布大量重复图文
- 小红书页面改版后选择器可能失效，报错时把报错发我修
