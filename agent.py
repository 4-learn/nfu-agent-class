"""第 2 節：自己寫一個 AI Agent。

模型只會「提議」呼叫哪個函式；真正執行函式的是這支程式。

    python agent.py "示波器還有幾台？"
    python agent.py --replay "示波器還有幾台？"   沒有 Token 時，用寫好的劇本代替模型

Token：放在同資料夾的 token.txt（一行），或設環境變數 NMKING_TOKEN。不要上傳或傳給別人。
"""

import json
import os
import sys
from pathlib import Path

from equipment import borrow, query_stock

BASE_URL = "https://ai.nmking.io/v1"
MODEL = os.environ.get("NMKING_MODEL", "gpt-5.6-luna")  # 點數池綁定的模型（2026-10-19 /v1/models 列出）
MAX_STEPS = 3                                         # 最多問模型幾次，避免停不下來、燒光點數

# 1. 工具清單：名字 → 函式
TOOLS = {"query_stock": query_stock, "borrow": borrow}

# 2. 給模型看的工具說明（模型只看得到這些文字，看不到函式本身）
TOOL_SPECS = [
    {"type": "function", "name": "query_stock", "description": query_stock.__doc__,
     "parameters": {"type": "object", "properties": {"item": {"type": "string"}},
                    "required": ["item"], "additionalProperties": False}},
    {"type": "function", "name": "borrow", "description": borrow.__doc__,
     "parameters": {"type": "object",
                    "properties": {"item": {"type": "string"}, "qty": {"type": "integer"},
                                   "student_id": {"type": "string"}},
                    "required": ["item", "qty", "student_id"], "additionalProperties": False}},
]


def run_tool(name, arguments):
    """3. 真正執行函式的地方：模型給的名字和參數都可能是錯的。"""
    if name not in TOOLS:
        return f"錯誤：沒有叫 {name} 的工具"
    try:
        args = json.loads(arguments)
        return TOOLS[name](**args)
    except (json.JSONDecodeError, TypeError) as error:
        return f"錯誤：參數不對（{error}）"


def agent(question, ask_model):
    history = [{"role": "user", "content": question}]
    for step in range(1, MAX_STEPS + 1):
        reply = ask_model(history)
        calls = [item for item in reply.output if item.type == "function_call"]
        if not calls:
            print(f"[第 {step} 次] 模型回答：{reply.output_text}")
            return reply.output_text
        history += reply.output
        for call in calls:
            print(f"[第 {step} 次] 模型提議：{call.name}({call.arguments})")
            result = run_tool(call.name, call.arguments)
            print(f"           程式執行：{result}")
            history.append({"type": "function_call_output", "call_id": call.call_id, "output": result})
    print(f"已經問了 {MAX_STEPS} 次，停止。")
    return None


def real_model():
    from openai import OpenAI
    token_file = Path(__file__).with_name("token.txt")
    token = os.environ.get("NMKING_TOKEN") or (token_file.read_text(encoding="utf-8-sig").strip() if token_file.exists() else "")
    if not token:
        sys.exit("找不到 Token：請建立 token.txt，或改用 --replay")
    client = OpenAI(base_url=BASE_URL, api_key=token)
    return lambda history: client.responses.create(model=MODEL, input=history, tools=TOOL_SPECS)


def replay_model():
    """劇本：固定的回應，不是真的模型。格式和真的模型一樣。"""
    from types import SimpleNamespace as NS
    script = [
        [NS(type="function_call", name="query_stock", arguments='{"item": "示波器"}', call_id="c1")],
        [NS(type="message")],
    ]
    texts = ["", "示波器目前還有 5 台可以借。"]

    def ask(history):
        n = sum(1 for h in history if isinstance(h, dict) and h.get("type") == "function_call_output")
        n = min(n, len(script) - 1)
        return NS(output=script[n], output_text=texts[n])
    return ask


if __name__ == "__main__":
    replay = "--replay" in sys.argv
    words = [a for a in sys.argv[1:] if a != "--replay"]
    question = words[0] if words else "示波器還有幾台？"
    print(f"問題：{question}（{'劇本，不是真的模型' if replay else '真的模型：' + MODEL}）")
    agent(question, replay_model() if replay else real_model())
