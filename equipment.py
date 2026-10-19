"""系上器材借用：三節課共用的工具函式（一般的 Python 函式，沒有任何 AI）。"""

STOCK = {"示波器": 5, "三用電錶": 12, "麵包板": 30}
LOANS = []
MAX_PER_LOAN = 3


def query_stock(item: str) -> str:
    """查詢某項器材目前還有幾個可以借。"""
    if item not in STOCK:
        return f"沒有「{item}」這項器材。可借的有：{'、'.join(STOCK)}"
    return f"{item} 還有 {STOCK[item]} 個"


def borrow(item: str, qty: int, student_id: str) -> str:
    """幫學生借器材。一次最多借 3 個。"""
    if item not in STOCK:
        return f"借用失敗：沒有「{item}」這項器材"
    if qty < 1 or qty > MAX_PER_LOAN:
        return f"借用失敗：一次只能借 1～{MAX_PER_LOAN} 個，你要借 {qty} 個"
    if qty > STOCK[item]:
        return f"借用失敗：{item} 只剩 {STOCK[item]} 個"
    STOCK[item] -= qty
    LOANS.append((student_id, item, qty))
    return f"借用成功：{student_id} 借了 {qty} 個{item}，剩 {STOCK[item]} 個"
