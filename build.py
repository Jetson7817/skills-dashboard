#!/usr/bin/env python3
"""一键重建：扫描本机 → 注入模板 → 生成 index.html"""
import json, subprocess, datetime, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
data = json.loads(subprocess.check_output([sys.executable, "scan_skills.py"]))
tpl = open("template.html", encoding="utf-8").read()
out = tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False))
out = out.replace("__SCAN_DATE__", datetime.date.today().isoformat())
open("index.html", "w", encoding="utf-8").write(out)
print(f"index.html 已生成：{len(data)} 项，{len(out)} 字节")
