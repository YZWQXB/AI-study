# 第 13 章 函数进阶与模块基础
# 13.3 函数设计规范
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：学习单一职责、命名规范，以及把长函数拆成可读小函数的具体方法。

# ==================== 13.3.1 单一职责原则初步 ====================
# 一个函数只承担一件事：校验、计算、展示分开后，每段逻辑都能独立理解和替换。
# 重构前：校验、计算和输出混在一起，想复用计算部分只能复制代码。
def process_order_bad(quantity: int, unit_price: float) -> None:
    if quantity <= 0:
        print("数量不合法")
        return
    total = quantity * unit_price
    if total >= 200:
        total -= 20
    print(f"应付：{total:.2f}")

process_order_bad(5, 45.0)       # -> 应付：205.00

# 重构后：三个函数各做一件事，调用方按需组合。
def is_valid_quantity(quantity: int) -> bool:
    return quantity > 0

def calc_amount(quantity: int, unit_price: float) -> float:
    total = quantity * unit_price
    return total - 20 if total >= 200 else total

def show_amount(amount: float) -> None:
    print(f"应付：{amount:.2f}")

print("拆分后")
if is_valid_quantity(5):
    show_amount(calc_amount(5, 45.0))    # -> 应付：205.00
else:
    print("数量不合法")
# 单一职责不是“一个函数只写一行”，而是“一个函数只因为一个原因被修改”。
# 活动规则变化时只改 calc_amount，输出格式变化时只改 show_amount。
# // C++: 同样可拆成 bool isValidQuantity(int)、double calcAmount(...)、void showAmount(...)。

# ==================== 13.3.2 函数命名规范 ====================
# 函数名以动词开头，说明做什么；返回布尔值的函数用 is_、has_、can_ 开头。
def calc_monthly_interest(principal: float, annual_rate: float) -> float:
    return round(principal * annual_rate / 12, 2)

def is_adult(age: int) -> bool:
    return age >= 18

print(calc_monthly_interest(12000.0, 0.045))    # -> 45.0
print(is_adult(17))                             # -> False
# 名字应包含“动作 + 对象”，例如 calc_monthly_interest 比 calc 更能说明计算内容。
# 避免 do_data、process、handle 这类空泛名字；含义具体的名字让调用处几乎不用看注释。
# // C++: 常见驼峰命名 calcMonthlyInterest，原则相同：动词开头、语义具体。

# 命名对比：左侧名字无法判断参数含义和返回值，右侧名字可直接读懂调用。
def convert(value: float) -> float:
    return round(value * 7.2, 2)

def convert_usd_to_cny(usd_amount: float) -> float:
    return round(usd_amount * 7.2, 2)

print(convert(100.0), convert_usd_to_cny(100.0))    # -> 720.0 720.0
# 两个函数计算结果相同，但右侧更容易确认汇率方向和单位。

# ==================== 13.3.3 长函数拆分方法 ====================
# 长函数通常同时包含“准备数据、计算、格式化输出”三类步骤，可按步骤边界切开。
# 重构前：一个函数从拼接明细到打印汇总全部包办，需要滚动才能读完。
def print_invoice_bad(items: list[tuple[str, int, float]]) -> None:
    print("       订单清单")
    subtotal = 0.0
    for name, quantity, unit_price in items:
        line_total = quantity * unit_price
        subtotal += line_total
        print(f"{name} x{quantity}  {line_total:>8.2f}")
    if subtotal >= 300:
        discount = 20.0
    else:
        discount = 0.0
    print(f"小计：{subtotal:.2f}")
    print(f"优惠：{discount:.2f}")
    print(f"应付：{subtotal - discount:.2f}")

print_invoice_bad([("键盘", 2, 89.0), ("鼠标", 3, 45.0)])

# 重构后：每个函数只输出或计算一个部分，主函数只负责按顺序调用。
def build_line(name: str, quantity: int, unit_price: float) -> str:
    return f"{name} x{quantity}  {quantity * unit_price:>8.2f}"

def calc_subtotal(items: list[tuple[str, int, float]]) -> float:
    return sum(quantity * unit_price for _, quantity, unit_price in items)

def calc_discount(amount: float) -> float:
    return 20.0 if amount >= 300 else 0.0

def print_invoice(items: list[tuple[str, int, float]]) -> None:
    print("       订单清单")
    for name, quantity, unit_price in items:
        print(build_line(name, quantity, unit_price))
    amount = calc_subtotal(items)
    discount = calc_discount(amount)
    print(f"小计：{amount:.2f}")
    print(f"优惠：{discount:.2f}")
    print(f"应付：{amount - discount:.2f}")

print("拆分后")
print_invoice([("键盘", 2, 89.0), ("鼠标", 3, 45.0)])
# 两次输出完全一致：
#        订单清单
# 键盘 x2    178.00
# 鼠标 x3    135.00
# 小计：313.00
# 优惠：20.00
# 应付：293.00
# 判断是否需要拆分的信号：函数超过一屏、出现多个注释分段、需要来回滚动确认变量来源。
# 拆分后 calc_subtotal 可以单独测试，改折扣规则也不影响排版代码。
# // C++: 拆分思路相同，小函数更容易被内联优化，也更容易写单元测试。

# 常见坑点：
# 1. 函数名空泛，例如 process、handle、do_data。
#    现象：调用处必须回到定义处逐行阅读才能确认行为。
#    原因：名字只表达“有事发生”，没有说明对象和结果。
#    正确做法：使用动词加对象，例如 calc_discount、is_quantity_valid。
# 2. 计算函数内部直接 print，导致结果无法复用。
#    现象：其他模块想拿到数值时只能解析文本。
#    原因：计算与展示没有分离。
#    正确做法：计算函数 return 结果，展示函数负责格式化。
# 3. 为了“单一职责”拆得过细，出现大量只调用一次的短函数。
#    现象：阅读主流程要跳转十几次，理解成本反而上升。
#    原因：把职责理解成行数，而不是修改原因。
#    正确做法：按“校验、计算、展示”等稳定步骤拆分，保留必要的组合层。
# 4. 拆分后各函数仍通过全局变量共享数据。
#    现象：无法单独调用某个小函数，结果依赖外部状态。
#    原因：数据没有通过参数和返回值流动。
#    正确做法：把依赖作为参数传入，把结果 return 出来。
# 5. 命名与已有内置函数或常用函数冲突，例如自定义 sum、max。
#    现象：调用内置函数时行为异常或直接报错。
#    原因：同名函数遮蔽了内置名字。
#    正确做法：改用 calc_sum、find_max 等具体名字。
