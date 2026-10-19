"""第 2 節：用程式當 client，連上自己的 MCP server（不需要 AI）。

    python client.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

SERVER = Path(__file__).with_name("server.py")


def text(result):
    return " ".join(part.text for part in result.content if part.type == "text")


async def main():
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(params) as (read, write), ClientSession(read, write) as client:
        await client.initialize()

        print("1. 這個 server 有哪些工具：")
        for tool in (await client.list_tools()).tools:
            print(f"   {tool.name}：{tool.description}")
            print(f"      參數規格：{tool.input_schema['properties']}")

        print("2. 查庫存：", text(await client.call_tool("query_stock", {"item": "示波器"})))
        print("3. 借 2 個：", text(await client.call_tool("borrow", {"item": "示波器", "qty": 2, "student_id": "B11234567"})))
        print("4. 借 10 個：", text(await client.call_tool("borrow", {"item": "示波器", "qty": 10, "student_id": "B11234567"})))

        wrong = await client.call_tool("borrow", {"item": "示波器", "qty": "很多", "student_id": "B11234567"})
        print("5. qty 傳文字：", "被擋下" if wrong.is_error else "沒被擋", "－", text(wrong)[:60])


asyncio.run(main())
