# 第 13 章 函数进阶与模块基础
# 13.1 参数系统进阶
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习默认参数、关键字参数、*args 与 **kwargs、keyword-only 参数以及默认参数陷阱。

# ==================== 13.1.1 默认参数 ====================
# 形参可以带默认值，调用时省略该实参就使用默认值，适合“多数情况相同、少数情况需要改”的配置。
def make_invoice(customer: str, amount: float, tax_rate: float = 0.06) -> str:
    return f"{customer}应付款 {amount * (1 + tax_rate):.2f} 元"

print(make_invoice("甲公司", 2000.0))               # -> 甲公司应付款 2120.00 元
print(make_invoice("乙公司", 2000.0, 0.09))         # -> 乙公司应付款 2180.00 元
# 默认参数必须写在无默认值参数之后，否则定义时就会报语法错误。
# // C++: std::string makeInvoice(std::string customer, double amount, double taxRate = 0.06);
# // C++ 的默认实参同样只能从右往左连续设置。

# 默认值只在 def 执行时求值一次，所有省略该参数的调用共用同一个对象。
def describe_member(name: str, level: str = "普通", city: str = "未填写") -> str:
    return f"{name}（{level}，{city}）"

print(describe_member("周同学"))                    # -> 周同学（普通，未填写）
print(describe_member("周同学", "VIP"))             # -> 周同学（VIP，未填写）
print(describe_member("周同学", "VIP", "杭州"))     # -> 周同学（VIP，杭州）

# 用列表作为默认值可以看清“只求值一次”的副作用。
def add_item_bad(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

print(add_item_bad("苹果"))        # -> ['苹果']
print(add_item_bad("香蕉"))        # -> ['苹果', '香蕉']
# 第二次调用没有传入列表，却看到了上一次的内容，因为默认列表被复用了。
# // C++: 默认实参在每次调用时重新求值，std::vector<std::string> items = {} 每次都是新容器。

# 正确写法：默认值用 None，函数内部再创建新对象。
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item("苹果"))            # -> ['苹果']
print(add_item("香蕉"))            # -> ['香蕉']
print(add_item("西瓜", ["牛奶"]))  # -> ['牛奶', '西瓜']
# 传入的列表会被原地修改，这是调用方主动提供的容器，行为符合预期。

# ==================== 13.1.2 关键字参数 ====================
# 调用时写成 形参名=实参值，可以打乱顺序，让调用处的含义更清楚。
print(make_invoice("丙公司", tax_rate=0.13, amount=500.0))    # -> 丙公司应付款 565.00 元
# 位置参数必须写在关键字参数之前，下面这行是语法错误：
# make_invoice(amount=500.0, "丁公司", 0.13)
# 关键字名必须与形参名完全一致，拼错会抛出 TypeError。

# keyword-only 参数：在参数列表中加入 *，其后的参数只能用关键字传入。
def send_notice(message: str, *, urgent: bool = False, channel: str = "站内信") -> str:
    level = "加急" if urgent else "普通"
    return f"[{level}][{channel}] {message}"

print(send_notice("系统维护"))                        # -> [普通][站内信] 系统维护
print(send_notice("库存告警", urgent=True, channel="短信"))    # -> [加急][短信] 库存告警
# send_notice("库存告警", True)  # TypeError：* 之后的参数只能用关键字传入
# // C++: 没有关键字实参；常用重载、配置结构体或命名清晰的参数来表达相同意图。
# keyword-only 让布尔开关在调用处必须写明名字，避免 True/False 含义不明。

# ==================== 13.1.3 可变参数 ====================
# *args 把多余的位置实参收集成元组；**kwargs 把多余的关键字实参收集成字典。
def sum_prices(*prices: float) -> float:
    return round(sum(prices), 2)

def build_profile(name: str, **extra: str) -> str:
    details = [f"{key}={value}" for key, value in extra.items()]
    return name + "：" + "，".join(details)

print(sum_prices(12.5, 8.0, 30.5))                    # -> 51.0
print(sum_prices())                                   # -> 0
print(build_profile("王五", city="北京", level="普通"))    # -> 王五：city=北京，level=普通

# 调用侧同样可以用 * 和 ** 解包已有的列表与字典。
values = [10.0, 20.0]
options = {"city": "上海", "level": "VIP"}
print(sum_prices(*values))                            # -> 30.0
print(build_profile("赵六", **options))               # -> 赵六：city=上海，level=VIP
# 函数内 prices 是元组，可以遍历和求和，但没有 append 方法。
# // C++: 没有 *args；可用 std::initializer_list、模板参数包或 std::vector 接收不定数量实参。

# 普通参数与可变参数可以组合，普通参数写在前面。
def show_order(order_id: str, *items: str, coupon: str = "") -> str:
    text = f"订单 {order_id} 包含 {len(items)} 件商品：" + "、".join(items)
    if coupon:
        text += f"（使用优惠券 {coupon}）"
    return text

print(show_order("A1001", "键盘", "鼠标"))             # -> 订单 A1001 包含 2 件商品：键盘、鼠标
print(show_order("A1002", "显示器", coupon="NEW20"))   # -> 订单 A1002 包含 1 件商品：显示器（使用优惠券 NEW20）

# 常见坑点：
# 1. 用列表、字典作为默认参数。
#    现象：多次调用后列表累积之前的数据，或字典保留旧键值。
#    原因：默认对象在 def 时创建一次并被所有调用共享。
#    正确做法：默认值写 None，在函数体内判断后再创建新对象。
# 2. 把带默认值的参数写在无默认值参数前面。
#    现象：定义时报 SyntaxError: non-default argument follows default argument。
#    原因：位置参数按顺序绑定，后面的必填参数会被默认值挡住。
#    正确做法：必填参数在前，带默认值的参数在后。
# 3. 位置参数写在关键字参数之后。
#    现象：SyntaxError: positional argument follows keyword argument。
#    原因：Python 要求实参顺序先位置后关键字。
#    正确做法：先写位置实参，再写关键字实参。
# 4. 在 keyword-only 参数前忘记写 *，或误以为 * 后面还能按位置传。
#    现象：TypeError: takes 1 positional argument but 2 were given。
#    原因：* 之后的参数只能通过关键字传入。
#    正确做法：调用时写出参数名，例如 urgent=True。
# 5. 把 *args 当成列表使用。
#    现象：调用 prices.append(...) 抛出 AttributeError。
#    原因：*args 收集的是元组，不可变。
#    正确做法：需要列表时写成 list(prices)，或改用列表参数传入。
