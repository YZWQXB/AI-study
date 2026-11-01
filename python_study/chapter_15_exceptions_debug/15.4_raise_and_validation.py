# 第 15 章 异常处理与基础调试
# 15.4 主动抛出异常基础
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：用 raise 做输入校验与业务规则保护，掌握自定义异常、异常链与 add_note。

from pathlib import Path
import tempfile

# ==================== 15.4.1 raise ====================
# raise 主动指出“数据不合法”，让调用方无法忽略；返回一个无效值往往会被继续传下去。
def deposit(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError("存款金额必须大于 0")
    return balance + amount

try:
    print("正常存款：", deposit(1000.0, 200.0))   # -> 正常存款： 1200.0
    print("非法存款：", deposit(1000.0, -50.0))
except ValueError as error:
    print("被拒绝：", error)                       # -> 被拒绝： 存款金额必须大于 0
# raise 后面必须跟异常实例或异常类；只写 raise "错误" 会抛 TypeError。
# // C++: throw std::invalid_argument("原因"); 语义相同，但 C++ 的异常类型不受限制，Python 要求是 BaseException 子类。

def update_balance(balance: float, amount: float) -> float:
    try:
        return deposit(balance, amount)
    except ValueError:
        print("  记录失败日志后重新抛出")
        raise

try:
    update_balance(1000.0, -1.0)
except ValueError as error:
    print("最外层捕获：", error)      # -> 最外层捕获： 存款金额必须大于 0
# 不带参数的 raise 原样抛出当前异常，保留原始抛出位置；换新异常类型则要说明与原异常的关系。

with tempfile.TemporaryDirectory() as temp_dir:
    limit_path = Path(temp_dir) / "limit.txt"

    def read_limit(path: Path) -> int:
        try:
            return int(path.read_text(encoding="utf-8").strip())
        except FileNotFoundError as error:
            raise RuntimeError("读取限额配置失败") from error

    try:
        print("限额：", read_limit(limit_path))
    except RuntimeError as error:
        print("包装后的异常：", error)                       # -> 包装后的异常： 读取限额配置失败
        print("原始原因：", type(error.__cause__).__name__)  # -> 原始原因： FileNotFoundError
# from error 把原异常挂到 __cause__ 上，traceback 会标出“直接原因”，排错时不丢原始线索。

# ==================== 15.4.2 输入校验 ====================
# 自定义异常继承 ValueError，既表达具体含义，又能被原有的 ValueError 捕获。
class ScoreFormatError(ValueError):
    """成绩格式不合法时抛出。"""


def parse_score(raw: str) -> int:
    text = raw.strip()
    if not text:
        raise ScoreFormatError("成绩不能为空")
    try:
        value = int(text)
    except ValueError as error:
        raise ScoreFormatError(f"成绩必须是整数，收到 {text!r}") from error
    if not 0 <= value <= 100:
        raise ScoreFormatError(f"成绩必须在 0 到 100 之间，收到 {value}")
    return value

raw_scores = ["90", " 88 ", "", "九十分", "120"]
valid_scores = []
for raw in raw_scores:
    try:
        score = parse_score(raw)
    except ScoreFormatError as error:
        print(f"  {raw!r} 校验失败：{error}")
    else:
        valid_scores.append(score)
        print(f"  {raw!r} 校验通过：{score}")
# 输出：
#   '90' 校验通过：90
#   ' 88 ' 校验通过：88
#   '' 校验失败：成绩不能为空
#   '九十分' 校验失败：成绩必须是整数，收到 '九十分'
#   '120' 校验失败：成绩必须在 0 到 100 之间，收到 120
print("有效成绩条数：", len(valid_scores))     # -> 有效成绩条数： 2

try:
    parse_score("")
except ValueError as error:
    print("按父类捕获：", type(error).__name__)   # -> 按父类捕获： ScoreFormatError

try:
    parse_score("九十分")
except ScoreFormatError as error:
    error.add_note("发生在批量导入成绩文件第 3 行")
    print("异常备注：", error.__notes__)    # -> 异常备注： ['发生在批量导入成绩文件第 3 行']
# add_note 在 3.11 起可用，用来补充“出错时的上下文”，不改变异常类型和信息。

# ==================== 15.4.3 业务规则保护初步 ====================
# 自定义异常层次让业务错误可以分层捕获：先按订单错误统一处理，必要时再细分。
class OrderError(Exception):
    """订单业务错误的基类。"""


class InsufficientStockError(OrderError):
    """库存不足时抛出，携带商品与数量信息。"""

    def __init__(self, item: str, requested: int, available: int) -> None:
        super().__init__(f"{item} 库存不足：需要 {requested}，仅剩 {available}")
        self.item = item
        self.requested = requested
        self.available = available


def ship_order(stock: dict[str, int], item: str, amount: int) -> int:
    if amount <= 0:
        raise ValueError("出库数量必须大于 0")
    available = stock.get(item, 0)
    if available < amount:
        raise InsufficientStockError(item, amount, available)
    stock[item] = available - amount
    return stock[item]


stock = {"显示器": 5, "键盘": 12}
print("第一次出库后剩余：", ship_order(stock, "显示器", 3))   # -> 第一次出库后剩余： 2

try:
    ship_order(stock, "显示器", 4)
except OrderError as error:
    print("业务拦截：", error)            # -> 业务拦截： 显示器 库存不足：需要 4，仅剩 2
    print("可用数量：", error.available)   # -> 可用数量： 2
# 用 OrderError 作为父类捕获，调用方不必为每种业务错误各写一个 except。

try:
    ship_order(stock, "键盘", 0)
except ValueError as error:
    print("参数校验：", error)      # -> 参数校验： 出库数量必须大于 0
# 参数错误用 ValueError，业务冲突用自定义异常；两类问题在上层可能需要不同处理方式。

try:
    ship_order(stock, "鼠标", 2)
except OrderError as error:
    print("缺货拦截：", error)      # -> 缺货拦截： 鼠标 库存不足：需要 2，仅剩 0
# 关键点：先校验、后修改库存；校验失败时数据没有被改动过。

# 常见坑点：
# 1. 只写 raise ValueError 而不实例化：抛出的是类型而不是异常信息，调用方拿不到原因；应写 raise ValueError("具体原因")。
# 2. 自定义异常继承 Exception，而上层用 except ValueError 捕获：类型不匹配导致漏捕；按语义选择基类。
# 3. 在 except 里换成新异常却不写 from：调用链断裂，原始错误被掩盖；用 raise NewError(...) from error。
# 4. 用异常代替常规分支（例如用异常判断“是否找到”）：可预期的结果用返回值，真正的错误才抛异常。
# 5. 抛出异常前已经修改了数据：库存已扣减才校验失败，状态无法回滚；必须先校验、后修改。
