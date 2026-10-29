#!/usr/bin/env python3
"""扫描本机所有 AI 技能/插件/MCP/CLI 工具，输出 JSON 数据供看板使用。

用法: python3 scan_skills.py > skills_data.json
      或直接运行 build.py 一键扫描 + 生成 index.html
"""
import os, re, json, datetime

HOME = os.path.expanduser("~")

def parse_frontmatter_desc(path):
    """解析 SKILL.md frontmatter 里的 description（兼容块标量写法）。"""
    try:
        content = open(path, encoding='utf-8', errors='ignore').read(4000)
    except Exception:
        return ""
    m = re.search(r'^---\s*\n(.*?)\n---', content, re.S)
    if not m:
        return ""
    lines = m.group(1).split('\n')
    desc_lines, collecting = [], False
    for ln in lines:
        if ln.startswith('description:'):
            val = ln[len('description:'):].strip()
            collecting = True
            if val in ('>', '|', '>-', '|-'):
                continue
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                return val[1:-1].strip()
            if val:
                desc_lines.append(val)
            continue
        if collecting:
            if ln.startswith('  ') or ln.startswith('\t') or (ln and not re.match(r'^\w[\w-]*:', ln) and not ln.startswith('-')):
                desc_lines.append(ln.strip())
            else:
                break
    return re.sub(r'\s+', ' ', ' '.join(desc_lines)).strip()[:220]

def mtime_of(path):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d')
    except Exception:
        return ""

def scan_skill_dirs(root, source_label, kind="skill"):
    items = []
    if not os.path.isdir(root):
        return items
    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        sm = os.path.join(d, 'SKILL.md')
        if os.path.isfile(sm) and not os.path.islink(d):  # 符号链接是共享副本，跳过
            items.append({"name": name, "desc": parse_frontmatter_desc(sm),
                          "path": d.replace(HOME, "~"), "date": mtime_of(sm),
                          "source": source_label, "kind": kind})
    return items

data = []
data += scan_skill_dirs(f"{HOME}/.agents/skills", "Agents 通用")
data += scan_skill_dirs(f"{HOME}/.zcode/skills", "ZCode")
data += scan_skill_dirs(f"{HOME}/.codex/skills", "Codex")
cd = f"{HOME}/.claude/skills"
if os.path.isdir(cd):
    for name in sorted(os.listdir(cd)):
        d = os.path.join(cd, name)
        if os.path.isfile(os.path.join(d, 'SKILL.md')) and not os.path.islink(d):
            data.append({"name": name, "desc": parse_frontmatter_desc(os.path.join(d, 'SKILL.md')),
                         "path": d.replace(HOME, "~"), "date": mtime_of(d), "source": "Claude", "kind": "skill"})
data += scan_skill_dirs(f"{HOME}/.cursor/skills-cursor", "Cursor")
data += scan_skill_dirs(f"{HOME}/.openclaw-autoclaw/skills", "OpenClaw")
data += scan_skill_dirs(f"{HOME}/.hub/skills", "Hub 视频创意")
data += scan_skill_dirs(f"{HOME}/.workbuddy/skills", "WorkBuddy")
data += scan_skill_dirs(f"{HOME}/.minimax/.builtin-skills", "MiniMax 内置")
data += scan_skill_dirs(f"{HOME}/.42plugin/builtin", "42plugin")
data += scan_skill_dirs(f"{HOME}/.kimi/daimon/skills", "Kimi")
for proj_root in (f"{HOME}/ZCodeProject/skills", f"{HOME}/dasupervision-db/skills"):
    if os.path.isdir(proj_root):
        for name in sorted(os.listdir(proj_root)):
            d = os.path.join(proj_root, name)
            if os.path.isfile(os.path.join(d, 'SKILL.md')):
                data.append({"name": name, "desc": parse_frontmatter_desc(os.path.join(d, 'SKILL.md')),
                             "path": d.replace(HOME, "~"), "date": mtime_of(d), "source": "项目内", "kind": "skill"})
for single in [f"{HOME}/Desktop/GSTZ/Humanizer-zh", f"{HOME}/Documents/AI日报改版测试/ai-hot-image-brief",
               f"{HOME}/Documents/AI日报改版测试/ai-daily-brief", f"{HOME}/Documents/视频/ai-promo-video-maker",
               f"{HOME}/Documents/Harness+Loop/harness-loop", f"{HOME}/Documents/项目开发框架skill/harness-project-scaffold"]:
    sm = os.path.join(single, 'SKILL.md')
    if os.path.isfile(sm):
        data.append({"name": os.path.basename(single), "desc": parse_frontmatter_desc(sm),
                     "path": single.replace(HOME, "~"), "date": mtime_of(single), "source": "项目内", "kind": "skill"})

plugin_root = f"{HOME}/.zcode/cli/plugins/cache/zcode-plugins-official"
if os.path.isdir(plugin_root):
    for name in sorted(os.listdir(plugin_root)):
        p = os.path.join(plugin_root, name)
        if not os.path.isdir(p):
            continue
        vers = sorted(os.listdir(p))
        ver = vers[-1] if vers else ""
        skills = []
        for root2, dirs, files in os.walk(os.path.join(p, ver)):
            if 'SKILL.md' in files:
                rel = os.path.relpath(root2, os.path.join(p, ver))
                skills.append(rel.split('/')[0] if rel != '.' else name)
            dirs[:] = [x for x in dirs if x not in ('node_modules', '.git')]
        data.append({"name": name, "desc": f"官方插件 v{ver}" + (f"，含技能: {', '.join(sorted(set(skills)))[:150]}" if skills else ""),
                     "path": os.path.join(p, ver).replace(HOME, "~"), "date": mtime_of(p),
                     "source": "ZCode 插件", "kind": "plugin", "version": ver})

# ===== 以下 MCP / CLI 为本机（作者）快照的精选清单，其他机器请按需修改 =====
mcps = [
    {"name": "rea", "desc": "逆向工程全家桶（Reverse-Engineering-Anything）：Mach-O/ELF/APK/Electron/固件/网页分析，集成 Ghidra、Hopper、JEB、Binwalk、apktool 等，200+ 工具", "path": "~/.local/node-arm64/bin/rea", "source": "MCP 服务器", "clients": "ZCode / Codex"},
    {"name": "web_reader", "desc": "网页抓取与阅读：把 URL 转成大模型友好的 Markdown 输入", "path": "ZCode 内置", "source": "MCP 服务器", "clients": "ZCode"},
    {"name": "4_5v_mcp", "desc": "AI 视觉图像分析：远程图片 URL 的高级理解（布局、风格、组件提取）", "path": "ZCode 内置", "source": "MCP 服务器", "clients": "ZCode"},
    {"name": "node_repl", "desc": "Browser Use / Computer Use 的 Node REPL 执行环境（ChatGPT.app 内置）", "path": "MCP", "source": "MCP 服务器", "clients": "Codex"},
    {"name": "kimi-cu", "desc": "KimiCU 电脑操控 MCP（KimiCU.app，-s user 全局）", "path": "/Applications/KimiCU.app", "source": "MCP 服务器", "clients": "Codex"},
    {"name": "evaluate", "desc": "evaluate MCP 服务器", "path": "~/.local/bin/evaluate", "source": "MCP 服务器", "clients": "Claude"},
    {"name": "jev", "desc": "JEV 启动器（Python）", "path": "~/Desktop/AI 实践/.../launch.py", "source": "MCP 服务器", "clients": "Codex"},
    {"name": "computer-use", "desc": "Codex 电脑操控客户端（当前已禁用）", "path": "MCP", "source": "MCP 服务器", "clients": "Codex (禁用)"},
]
for m in mcps:
    m["kind"] = "mcp"; m["date"] = ""
    data.append(m)

cli = [
    ("openclaw", "OpenClaw — 开源个人 AI 助手/agent 网关框架（~/.openclaw-autoclaw 的宿主）", None),
    ("xiaohongshu-mcp", "小红书 MCP 服务器 CLI（配合 xiaohongshu 技能）", None),
    ("xiaohongshu-login", "小红书登录/身份维护 CLI", None),
    ("lark-cli", "飞书 / Lark 命令行客户端", None),
    ("alipay-bot", "支付宝相关自动化机器人 CLI", None),
    ("ashare-daily-publish", "A 股日报自动发布 CLI（配合 a-stock-broadcast 技能）", None),
    ("getnote", "Get笔记 CLI（配合 getnote-* 技能）", "node-arm64"),
    ("firecrawl", "Firecrawl 网页抓取 CLI", "node-arm64"),
    ("mcporter", "MCP 服务器导入/管理工具", "node-arm64"),
    ("uipro", "UI/UX Pro Max 技能安装器 CLI（给各 AI 编码助手装设计技能）", "node-arm64"),
    ("dsh", "DeepSeek Harness 启动器：按 profile 组合插件补丁栈", "node-arm64"),
    ("agent-browser", "浏览器代理 CLI（agent-browser 二进制）", "node-arm64"),
    ("rea", "REA 逆向工程 CLI（rea / rea-agents）", "node-arm64"),
    ("claude", "Claude Code CLI", "node-arm64"),
    ("codex", "OpenAI Codex CLI", "node-arm64"),
]
for name, desc, bindir in cli:
    base = f"{HOME}/.local/node-arm64/bin" if bindir == "node-arm64" else f"{HOME}/.local/bin"
    p = os.path.join(base, name)
    if os.path.exists(p):
        data.append({"name": name, "desc": desc, "path": p.replace(HOME, "~"),
                     "date": mtime_of(p), "source": "命令行 CLI", "kind": "cli"})

print(json.dumps(data, ensure_ascii=False, indent=1))
