"""上課前檢查：python check.py"""

import importlib.metadata as meta
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
config = Path.home() / ".codex" / "config.toml"
if config.exists() and "ai.nmking.io" in config.read_text(encoding="utf-8", errors="ignore"):
    print("Codex 已接上生生有 Token ✅")
else:
    ok = False
    print("Codex ❌ 還沒接上生生有 Token（第 1 節：執行 1-套用-NMKING-Codex.bat）")
token = Path(__file__).with_name("token.txt")
if token.exists() and token.read_text(encoding="utf-8-sig").strip():
    print("token.txt ✅")
else:
    ok = False
    print("token.txt ❌ 還沒放（第 1 節最後一步）")
print("可以上課了" if ok else "請先完成上面標 ❌ 的項目")
