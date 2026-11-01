# 第 17 章 Python 基础规范与良好习惯
# 17.5 可维护代码习惯
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件用订单与取款场景演示函数拆分、数据结构选择和错误信息设计，并给出重构前后对比。

from dataclasses import dataclass

# ==================== 17.5.1 函数短小清晰 ====================
# 重构前：一个函数同时做校验、计算和拼字符串，读者要一次消化三件事。
DISCOUNT_RATE = 0.05


def process_order_bad(name: str, price: float, quantity: int, is_member: bool) -> str:
    if not name:
        return "商品名不能为空"
    if price <= 0 or quantity <= 0:
        return "单价与数量必须大于 0"
    subtotal = round(price * quantity, 2)
    discount = round(subtotal * DISCOUNT_RATE, 2) if is_member else 0.0
    total = round(subtotal - discount, 2)
    return f"{name} x{quantity} 小计 {subtotal:.2f} 优惠 {discount:.2f} 应付 {total:.2f}"


print(process_order_bad("机械键盘", 299.0, 2, True))
# -> 机械键盘 x2 小计 598.00 优惠 29.90 应付 568.10
# 重构后：拆成四个短函数，每个只有 3 到 5 行，名字直接说明职责。
def validate_order(name: str, price: float, quantity: int) -> None:
    if not name:
        raise ValueError("商品名不能为空")
    if price <= 0:
        raise ValueError(f"单价必须大于 0，当前为 {price}")
    if quantity <= 0:
        raise ValueError(f"数量必须大于 0，当前为 {quantity}")


def calc_totals(price: float, quantity: int, is_member: bool) -> tuple[float, float, float]:
    """返回三元组：(小计, 优惠, 应付)。"""
    subtotal = round(price * quantity, 2)
    discount = round(subtotal * DISCOUNT_RATE, 2) if is_member else 0.0
    total = round(subtotal - discount, 2)
    return subtotal, discount, total


def build_receipt(name: str, quantity: int, amounts: tuple[float, float, float]) -> str:
    subtotal, discount, total = amounts
    return f"{name} x{quantity} 小计 {subtotal:.2f} 优惠 {discount:.2f} 应付 {total:.2f}"


validate_order("机械键盘", 299.0, 2)
amounts = calc_totals(299.0, 2, True)
print(build_receipt("机械键盘", 2, amounts))
# -> 机械键盘 x2 小计 598.00 优惠 29.90 应付 568.10
print(process_order_bad("机械键盘", 299.0, 2, True) == build_receipt("机械键盘", 2, amounts))   # -> True
# 拆分后校验失败会抛出异常，而不是返回一句给用户看的字符串，调用方可以自己决定怎么提示。
# // C++: 拆函数的目标一致；Python 额外强调“一个函数只做一件事”，因为动态类型下
# // 读函数签名就能理解行为，条件分支越少越好。
try:
    validate_order("无线鼠标", -79.5, 3)
except ValueError as error:
    print(error)                                             # -> 单价必须大于 0，当前为 -79.5

# ==================== 17.5.2 数据结构合理 ====================
# 重构前：三个并行列表靠下标对齐，中间删掉一个元素后所有下标都会错位。
names = ["机械键盘", "无线鼠标", "显示器"]
prices = [299.0, 79.5, 1099.0]
quantities = [2, 3, 1]


def total_by_index() -> float:
    total = 0.0
    for index in range(len(names)):
        total += prices[index] * quantities[index]
    return round(total, 2)


print(total_by_index())                                      # -> 1935.5
# 重构后：一行订单就是一个记录对象，字段绑定在一起，增删都不会影响其他行。
@dataclass(slots=True)
class OrderLine:
    name: str
    price: float
    quantity: int

    def amount(self) -> float:
        return round(self.price * self.quantity, 2)


order_lines = [
    OrderLine("机械键盘", 299.0, 2),
    OrderLine("无线鼠标", 79.5, 3),
    OrderLine("显示器", 1099.0, 1),
]
print([line.amount() for line in order_lines])               # -> [598.0, 238.5, 1099.0]
print(round(sum(line.amount() for line in order_lines), 2))  # -> 1935.5
print(order_lines[1])                                        # -> OrderLine(name='无线鼠标', price=79.5, quantity=3)
# 需要按名称查找时建字典索引，查一次是 O(1)，比每次遍历列表快。
lines_by_name = {line.name: line for line in order_lines}
print(lines_by_name["显示器"].price)                         # -> 1099.0
# 相同的数据还能按数量排序、按金额汇总，记录结构让这些操作都变成一句话。
print(sorted(order_lines, key=lambda line: line.amount()))
# -> [OrderLine(name='无线鼠标', price=79.5, quantity=3), OrderLine(name='机械键盘', price=299.0, quantity=2), OrderLine(name='显示器', price=1099.0, quantity=1)]
# // C++: 对应 struct OrderLine 加 std::vector<OrderLine>，用命名字段而不是下标访问。

# ==================== 17.5.3 错误信息友好明确 ====================
# 重构前：出错只返回 -1，调用方无法区分“金额非法”和“余额不足”，也无法展示原因。
def withdraw_bad(balance: float, amount: float) -> float:
    if amount <= 0 or amount > balance:
        return -1.0
    return round(balance - amount, 2)


print(withdraw_bad(1000.0, 5000.0))                          # -> -1.0
# 重构后：继承 ValueError 的自定义异常 + 带当前值的消息，调用方能分级处理。
class InsufficientBalanceError(ValueError):
    """余额不足：便于单独捕获，也可按 ValueError 统一处理。"""


def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError(f"取款金额必须大于 0，当前为 {amount}")
    if amount > balance:
        raise InsufficientBalanceError(f"余额不足：当前余额 {balance:.2f} 元，取款 {amount:.2f} 元")
    return round(balance - amount, 2)


for amount in [200.0, -50.0, 5000.0]:
    try:
        print(f"取款 {amount:.2f} 元成功，余额 {withdraw(1000.0, amount):.2f} 元")
    except InsufficientBalanceError as error:                # 子类必须写在父类之前
        print(f"取款 {amount:.2f} 元失败（余额不足）：{error}")
    except ValueError as error:
        print(f"取款 {amount:.2f} 元失败（参数非法）：{error}")
# 输出三行：
# -> 取款 200.00 元成功，余额 800.00 元
# -> 取款 -50.00 元失败（参数非法）：取款金额必须大于 0，当前为 -50.0
# -> 取款 5000.00 元失败（余额不足）：余额不足：当前余额 1000.00 元，取款 5000.00 元
# 好错误信息的三个要素：说明发生了什么、当前的输入或状态是什么、期望的范围是什么。
# // C++: 常用异常类或 std::expected/错误码；返回 -1 这类哨兵值在多语言里都是维护陷阱。

# 常见坑点：
# 1. 现象：函数长到要滚动才能读完；原因：校验、计算、格式化混在一起；
#    做法：按“一件事一个函数”拆开，参数控制在三个以内。
# 2. 现象：删掉一个商品后金额全错位；原因：用多个并行列表按下标对齐；
#    做法：一行数据用一个 dataclass 或字典记录。
# 3. 现象：报错只显示 -1 或“错误”；原因：用哨兵值表达失败；做法：抛出带原因和当前值
#    的明确异常。
# 4. 现象：自定义异常捕获不到；原因：except 顺序写反，父类在前把子类吃掉；
#    做法：先写具体的异常类型，再写宽泛的父类。
# 5. 现象：重构后结果悄悄变了；原因：拆分时改了计算顺序或取整位置；做法：用重构前的
#    输出做对照断言（见 17.4），确认行为不变。
