# 第 12 章 函数基础
# 12.1 为什么需要函数
# 学习优先级：P0（核心必学） | 掌握要求：理解
# 本文件：用重复代码重构前后的对比，说明函数在代码复用、降低复杂度和提高可维护性上的作用。

# ==================== 12.1.1 代码复用 ====================
# 同一段计算规则在多处出现时，复制粘贴会让代码变长，修改时还容易漏掉某处。
# 先假设加班费规则固定：时薪 45 元，加班工资按 1.5 倍计算。
hourly_wage = 45
overtime_rate = 1.5

# 重构前：三名员工的加班费各写一遍，表达式重复三次。
print("重构前")
print(f"张工加班 6 小时：{6 * hourly_wage * overtime_rate:.2f}")    # -> 张工加班 6 小时：405.00
print(f"李工加班 4 小时：{4 * hourly_wage * overtime_rate:.2f}")    # -> 李工加班 4 小时：270.00
print(f"王工加班 9 小时：{9 * hourly_wage * overtime_rate:.2f}")    # -> 王工加班 9 小时：607.50

# 重构后：规则只写进函数一次，每位员工只传入自己的加班小时数。
def overtime_pay(hours: float) -> float:
    return hours * hourly_wage * overtime_rate

print("重构后")
for name, hours in [("张工", 6), ("李工", 4), ("王工", 9)]:
    print(f"{name}加班 {hours} 小时：{overtime_pay(hours):.2f}")
# 输出与重构前完全一致：405.00、270.00、607.50。
# def 的具体语法在 12.2 详细学习，这里先关注“规则只写一次”的效果。
# // C++: double overtimePay(double hours) { return hours * hourly_wage * overtime_rate; }

# ==================== 12.1.2 降低复杂度 ====================
# 一个结算流程同时做校验、计算和输出时，读代码要一直记住上下文的每一层。
# 重构前：所有步骤挤在一段代码里。
unit_price = 40.0
quantity = 3
member_level = 2
print("重构前")
if quantity <= 0:
    print("数量不合法")
else:
    subtotal = unit_price * quantity
    if subtotal >= 100:
        discount = subtotal * 0.1
    else:
        discount = 0.0
    if member_level >= 2:
        discount += 5.0
    print(f"小计：{subtotal:.2f}")                    # -> 小计：120.00
    print(f"优惠：{discount:.2f}")                    # -> 优惠：17.00
    print(f"应付：{subtotal - discount:.2f}")         # -> 应付：103.00

# 重构后：每个函数只做一件事，主流程读起来接近自然语言。
def is_quantity_valid(quantity: int) -> bool:
    return quantity > 0

def calc_subtotal(unit_price: float, quantity: int) -> float:
    return unit_price * quantity

def calc_discount(subtotal: float, member_level: int) -> float:
    discount = subtotal * 0.1 if subtotal >= 100 else 0.0
    if member_level >= 2:
        discount += 5.0
    return discount

print("重构后")
if not is_quantity_valid(quantity):
    print("数量不合法")
else:
    subtotal = calc_subtotal(unit_price, quantity)
    discount = calc_discount(subtotal, member_level)
    print(f"小计：{subtotal:.2f}")                    # -> 小计：120.00
    print(f"优惠：{discount:.2f}")                    # -> 优惠：17.00
    print(f"应付：{subtotal - discount:.2f}")         # -> 应付：103.00

# 函数名本身就是说明：读主流程时不必再逐行分析条件表达式。
# // C++: 同样可以把结算拆成 bool isValidQuantity(int) 等小函数，减少主流程的认知负担。

# ==================== 12.1.3 提高可维护性 ====================
# 满 100 减 15 的活动规则写在三个地方，规则一变就要改三处，容易漏改。
order_a = 128.0
order_b = 86.0
order_c = 245.0
print("重构前")
print(f"订单 A 应付：{(order_a - 15 if order_a >= 100 else order_a):.2f}")    # -> 订单 A 应付：113.00
print(f"订单 B 应付：{(order_b - 15 if order_b >= 100 else order_b):.2f}")    # -> 订单 B 应付：86.00
print(f"订单 C 应付：{(order_c - 15 if order_c >= 100 else order_c):.2f}")    # -> 订单 C 应付：230.00

# 重构后：门槛和减免额只在函数中定义一次。
MIN_AMOUNT = 100.0
REDUCTION = 15.0

def payable(total: float) -> float:
    if total >= MIN_AMOUNT:
        return total - REDUCTION
    return total

print("重构后")
for order_name, order_total in [("A", order_a), ("B", order_b), ("C", order_c)]:
    print(f"订单 {order_name} 应付：{payable(order_total):.2f}")

# 活动改成“满 120 减 20”时，只需修改 MIN_AMOUNT 和 REDUCTION 两行常量。
# // C++: 常把规则写成 const double 常量或封装成函数，避免魔法数字散落在多个调用点。

# 常见坑点：
# 1. 只把重复代码原样塞进函数，函数仍然又校验又计算又打印。
#    原因：抽取时没有划分职责，函数只是“变短的复制粘贴”。
#    正确做法：按“校验、计算、展示”拆成多个小函数。
# 2. 函数名用 do_process 一类空泛词，调用处看不出在做什么。
#    原因：只关注“有函数”，没有关注函数名要表达意图。
#    正确做法：用动词加对象命名，例如 calc_discount、is_quantity_valid。
# 3. 规则变化后只改了其中一处调用点，其余两处仍然用旧数字。
#    原因：规则以字面量形式散落在多处。
#    正确做法：把规则集中到常量或函数中，调用点只传数据。
# 4. 为了复用而抽取只调用一次、只有一行的代码。
#    原因：把“减少行数”当成唯一目标，反而增加跳转成本。
#    正确做法：只有重复、复杂或需要独立测试的逻辑才值得封装。
# 5. 函数依赖外部变量（如 hourly_wage）却不作为参数，换规则时要改变量值。
#    原因：函数与全局状态耦合，复用范围被限制。
#    正确做法：规则稳定时用常量，规则会变时把费率作为参数传入。
