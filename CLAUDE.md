# 小红书官网复盘帖自动化

用户是设计工作室，不懂技术，全程用中文、回复要短。

- 用户丢来一个网址、或说"跑帖子 / 做帖子 / 发小红书 / 拆解"时，按 `.claude/skills/xhs-ins-post/SKILL.md` 全自动跑完，用户只在浏览器里点「发布」。
- 代码：`xhs/shoot.py`（截图）、`xhs/mockup.py`（拼图）、`xhs/publish.py`（填写发布页）。
- `accounts/`（登录状态）、`materials/`（素材）、`posts/`（帖子）是用户的本地数据，**永远不要提交到 git 或上传到任何地方**。
- 运行环境是用户自己的 Mac，Python 用 `python3`。
