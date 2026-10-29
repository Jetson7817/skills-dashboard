# 🗂 我的技能 · 工具榜

一个本地 AI 技能/工具清单看板：扫描你电脑上散落在各处的 AI Agent 技能、插件、MCP 服务器和命令行工具，生成一个 aihot.news 风格的单文件 HTML 看板。

**在线示例（作者的机器快照，288 项 / 16 个来源）**：
👉 https://jetson7817.github.io/skills-dashboard/

## 它解决什么问题

装了一堆从 GitHub 拿来的技能和工具，散落在 `~/.agents`、`~/.codex`、`~/.claude`、`~/.zcode`、`~/.hub`…… 十几个目录里，很快就忘了自己有什么、装在哪、哪个客户端能用。这个项目把它们全部扫出来，做成一张可搜索、可过滤、可收藏（浏览器本地）的看板。

## 快速开始

```bash
git clone https://github.com/Jetson7817/skills-dashboard.git
cd skills-dashboard

# 方式一：直接看作者的示例
open index.html

# 方式二：扫描你自己的机器，生成你的看板
python3 build.py && open index.html
```

> 仅支持 macOS（扫描的是 `~` 下的常见 AI 工具目录）。无任何依赖，纯标准库。

## 会扫描哪些位置

| 来源 | 位置 |
|---|---|
| Agents 通用 | `~/.agents/skills` |
| Codex | `~/.codex/skills` |
| ZCode | `~/.zcode/skills` + 官方插件目录 |
| Claude | `~/.claude/skills` + 插件 |
| Cursor | `~/.cursor/skills-cursor` |
| OpenClaw | `~/.openclaw-autoclaw/skills` |
| 视频创意 | `~/.hub/skills` |
| 其他 | WorkBuddy / MiniMax / 42plugin / Kimi / 项目内 SKILL.md / `~/.local/bin` CLI |

说明：
- 各 AI 客户端里指向 `~/.agents/skills` 的符号链接（如 firecrawl 全家桶）会被跳过，避免重复计数
- MCP 服务器与 CLI 清单是作者机器的精选快照（在 `scan_skills.py` 底部），按需改成你自己的
- 页面数据为生成时的静态快照，新装了工具重新跑 `build.py` 即可

## 功能

- 🔍 搜索（名称/描述/路径）、分类 tab、最近更新热榜、分类统计
- 🌓 浅色 / 深色 / 跟随系统三档主题
- 点击卡片展开完整描述，一键复制安装路径
- 单文件 `index.html`，无外部依赖，可托管到任意静态空间（GitHub Pages / Netlify…）

## 结构

```
├── index.html       # 预生成的看板（作者机器快照）
├── template.html    # 页面模板（__DATA__ 占位符）
├── scan_skills.py   # 本机扫描器 → JSON
└── build.py         # 一键：扫描 + 注入模板 → index.html
```

## 致谢

页面视觉风格参考了开源项目 [aihot.news](https://aihot.news/)（米白纸感底色、青绿主色、时间线卡片流、热榜侧栏）。

## License

MIT
