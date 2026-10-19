"""上課前檢查：python check.py"""

import importlib.metadata as meta
import shutil
import sys
from pathlib import Path

ok = True
print(f"Python {sys.version.split()[0]}", "✅" if sys.version_info >= (3, 10) else "❌ 需要 3.10 以上")
for pkg in ("mcp", "openai"):
    try:
        print(f"{pkg} {meta.version(pkg)} ✅")
    except meta.PackageNotFoundError:
        ok = False
        print(f"{pkg} ❌ 還沒安裝：python -m pip install mcp==2.3.0 openai==3.35.1")
print("Codex CLI", "✅" if shutil.which("codex") else "❌ 找不到 codex 指令（第 3 節才需要）")
token = Path(__file__).with_name("token.txt")
print("token.txt", "✅" if token.exists() and token.read_text().strip() else "➖ 還沒放（第 1 節可先用 --replay）")
print("可以上課了" if ok else "請先完成上面標 ❌ 的項目")
