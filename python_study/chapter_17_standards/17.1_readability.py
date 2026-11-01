# 第 17 章 Python 基础规范与良好习惯
# 17.1 可读性优先原则
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件用订单场景对比命名、空格缩进与表达式写法，同一段逻辑给出错误与正确版本。

# ==================== 17.1.1 命名规范 ====================
# 变量与函数用小写加下划线（snake_case），类用 PascalCase，常量全大写。
# 错误写法：名字看不出含义，只能靠猜。
a = 12.5
b = 4
c = 0.9
d = a * b * c
print(d)                                                     # -> 45.0
# 正确写法：同一份计算，但每个名字都说明了它是什么。
unit_price = 12.5
quantity = 4
member_discount = 0.9
order_total = unit_price * quantity * member_discount
print(order_total)                                           # -> 45.0
# // C++: 命名同样的重要，但 C++ 习惯 const double UNIT_PRICE 与成员 m_xxx；
# // Python 没有 const，常量靠全大写加下划线来表达“约定不改”。
FREE_SHIPPING_THRESHOLD = 99.0
is_member = True                       # 布尔值加 is_ / has_ / can_ 前缀
has_coupon = False
cart_items = ["笔记本", "钢笔"]        # 存放多个值用复数名
print(FREE_SHIPPING_THRESHOLD, is_member, len(cart_items))   # -> 99.0 True 2
# 不要用拼音缩写混写（如 yhk_zh）、不要把类型塞进名字（如 price_float）。
# 循环变量也要有意义：for item in cart_items 比 for x in cart_items 更清楚。

# ==================== 17.1.2 缩进、空格与空行 ====================
# Python 用缩进表示代码块，官方风格是每级 4 个空格，绝不混用 tab。
# 错误示例（只做文字对照，混用会直接报 IndentationError / TabError）：
# if order_total >= 100:
#   print("免运费")        <- 缩进 2 空格
#     print("满减 10 元")    <- 同一代码块缩进不一致，解释器无法判断层级
# 正确示例：同一代码块缩进一致，用空行分隔不同的函数。
def shipping_fee(total: float) -> float:
    if total >= FREE_SHIPPING_THRESHOLD:
        return 0.0
    return 6.0


def format_total(total: float) -> str:
    fee = shipping_fee(total)
    return f"商品 {total:.2f} 元，运费 {fee:.2f} 元，合计 {total + fee:.2f} 元"


print(format_total(45.0))                                    # -> 商品 45.00 元，运费 6.00 元，合计 51.00 元
print(format_total(120.0))                                   # -> 商品 120.00 元，运费 0.00 元，合计 120.00 元
# 空格规则：二元运算符两侧各一个空格；逗号后加空格；函数调用名与括号之间不加空格。
# 错误：total=price*quantity ;  calc (price ,quantity)
# 正确：total = price * quantity ;  calc(price, quantity)
# 默认参数与关键字参数的等号两侧不加空格：def calc(price, quantity=1)。
# // C++: 大括号位置和空行同样影响可读性，Python 把这些交给缩进与空行表达层级。

# ==================== 17.1.3 表达式书写清晰化 ====================
# 错误写法：一行里塞进多层条件与算术，读者无法看出业务步骤。
price = 88.0
quantity = 3
is_vip = True
vip_level = 2
total_bad = price * quantity * (0.95 if is_vip and vip_level >= 2 else 0.98 if is_vip else 1.0)
print(round(total_bad, 2))                                   # -> 250.8
# 正确写法：把规则拆成有名字的步骤，嵌套的三元表达式换成提前 return 的小函数。
def discount_rate(member: bool, level: int) -> float:
    if member and level >= 2:
        return 0.95
    if member:
        return 0.98
    return 1.0


subtotal = price * quantity
rate = discount_rate(is_vip, vip_level)
final_total = round(subtotal * rate, 2)
print(final_total)                                           # -> 250.8
# 判断区间条件时用链式比较，C++ 必须写成两个比较。
score = 85
print(0 <= score <= 100)                                     # -> True
# // C++: if (score >= 0 && score <= 100) { ... }
# 布尔结果直接返回，不要写 if cond: return True / else: return False。
def is_free_shipping(total: float) -> bool:
    return total >= FREE_SHIPPING_THRESHOLD


print(is_free_shipping(45.0))                                # -> False
# 不要把 and / or 当三元表达式用：前面为假值时会得到意料之外的结果。
empty_count = 0
print(empty_count and empty_count or 100)                    # -> 100
print(100 if empty_count is None else empty_count)           # -> 0
# 优先级不确定就加括号：net = (unit_price - coupon) * quantity。

# 常见坑点：
# 1. 现象：读到 a * b * c 完全不知道算的是什么；原因：用单字母名和魔法数；
#    做法：变量名写业务含义，常量提取为大写常量。
# 2. 现象：调用 sum(...) 报 TypeError: 'int' object is not callable；原因：变量名覆盖了
#    内置函数；做法：改名 total_score，不要用 list/dict/sum/str 当变量名。
# 3. 现象：运行报 TabError 或 IndentationError；原因：tab 与空格混用；
#    做法：编辑器统一设成 4 空格。
# 4. 现象：嵌套三元表达式结果总是不对；原因：条件优先级写不清；做法：拆成带提前 return
#    的小函数。
# 5. 现象：`x and x or 默认值` 在 x 为 0 或空串时返回默认值；原因：and/or 返回的是操作数
#    而不是布尔值；做法：用 `默认值 if x is None else x`。
