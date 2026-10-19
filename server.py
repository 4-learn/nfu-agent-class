"""第 2 節：把第 1 節的函式變成 MCP 工具。

    python server.py      （通常不用自己執行；client.py 或 Codex 會幫你啟動）
"""

from mcp.server.mcpserver import MCPServer

import equipment

server = MCPServer("equipment")


@server.tool()
def query_stock(item: str) -> str:
    """查詢某項器材目前還有幾個可以借。"""
    return equipment.query_stock(item)


@server.tool()
def borrow(item: str, qty: int, student_id: str) -> str:
    """幫學生借器材。一次最多借 3 個。"""
    return equipment.borrow(item, qty, student_id)


if __name__ == "__main__":
    server.run("stdio")
