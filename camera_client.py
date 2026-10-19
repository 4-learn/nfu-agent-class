"""第 2 節最後：同一個 client 程式，改連另一台機器上的 MCP server（教室的 Pi 5 攝影機）。

    python camera_client.py            只列出工具
    python camera_client.py --capture  請攝影機拍一張照（約 10 秒），存成 photo.jpg
"""

import asyncio
import base64
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://nfu-mcp.4impact.cc/mcp"   # 上課時才開放
PHOTO = Path(__file__).with_name("photo.jpg")


def text(result):
    return " ".join(part.text for part in result.content if part.type == "text")


async def main(capture):
    async with streamable_http_client(URL) as (read, write), ClientSession(read, write) as client:
        await client.initialize()
        print("這台機器提供的工具：")
        for tool in (await client.list_tools()).tools:
            print(f"   {tool.name}：{(tool.description or '').splitlines()[0]}")
        if capture:
            print("拍照中（約 10 秒）……")
            print("結果：", text(await client.call_tool("capture_now", {})))
            frame = await client.call_tool("get_latest_frame", {})
            for part in frame.content:
                if part.type == "image":
                    PHOTO.write_bytes(base64.b64decode(part.data))
                    print(f"照片已存成 {PHOTO.name}，打開來看看拍到什麼")


try:
    asyncio.run(main("--capture" in sys.argv))
except Exception:
    sys.exit("連不上教室攝影機：攝影機目前沒有開放（上課時才會開），不是你做錯。")
