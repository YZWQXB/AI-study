# 第 17 章 Python 基础规范与良好习惯
# 17.2 代码组织基础
# 学习优先级：P1（重点掌握） | 掌握要求：会用
# 本文件用一个下单结算小项目演示主流程与辅助函数分离、三层职责划分以及消除重复代码。

# ==================== 17.2.1 主流程与辅助函数分离 ====================
# 数据层：常量与解析函数，只负责把外部文本变成结构化数据。
ORDER_ROWS = ["机械键盘,299.0,2", "无线鼠标,79.5,3", "显示器,1099.0,1"]
MEMBER_RATE = 0.9


def parse_order_row(row: str) -> tuple[str, float, int]:
    name, price_text, quantity_text = row.split(",")
    return name, float(price_text), int(quantity_text)


# 逻辑层：只做计算，既不读输入也不打印，方便复用和单独验证。
def line_amount(order: tuple[str, float, int]) -> float:
    _, price, quantity = order
    return round(price * quantity, 2)


# 展示层：只负责把结果拼成字符串，打印交给主流程。
def format_line(order: tuple[str, float, int]) -> str:
    name, _, quantity = order
    return f"{name} x{quantity}，小计 {line_amount(order):.2f} 元"


# 主流程：按“取数据 -> 计算 -> 展示”三步走，每一步只调用现成函数。
def main() -> None:
    orders = [parse_order_row(row) for row in ORDER_ROWS]
    total = sum(line_amount(order) for order in orders)
    for order in orders:
        print(format_line(order))                            # -> 每行一条商品明细
    print(f"合计：{total:.2f} 元")                            # -> 合计：1935.50 元


if __name__ == "__main__":
    main()
# 输出三行明细加一行合计：
# -> 机械键盘 x2，小计 598.00 元
# -> 无线鼠标 x3，小计 238.50 元
# -> 显示器 x1，小计 1099.00 元
# -> 合计：1935.50 元
# // C++: 通常写成 main() 里调用 calc()、print() 等函数；__main__ 判断相当于
# // 只在“作为程序入口”时才执行主流程，被其他代码导入时不执行。
# 好处：改数据格式只动 parse，改计算规则只动 line_amount，改输出样式只动 format_line。

# ==================== 17.2.2 模块职责划分 ====================
# 三层职责的边界：解析层不打印、逻辑层不打印、展示层不计算，各自只做一件事。
first_row = ORDER_ROWS[0]
parsed_order = parse_order_row(first_row)
print(parsed_order)                                          # -> ('机械键盘', 299.0, 2)
print(line_amount(parsed_order))                             # -> 598.0
print(format_line(parsed_order))                             # -> 机械键盘 x2，小计 598.00 元
# 因为逻辑层返回数字而不是直接打印，所以可以拿来比较、累加、写进报表。
print(line_amount(parsed_order) > 500)                       # -> True
print(sum(line_amount(parse_order_row(row)) for row in ORDER_ROWS))   # -> 1935.5
# 反过来，如果逻辑函数里直接 print，就只能靠“看输出对不对”，无法被 17.4 的断言复用。
# 小项目也建议按这个顺序写文件：常量、辅助函数、主流程、入口判断。
# // C++: 多文件项目按 .h 声明 / .cpp 实现拆开；单文件 Python 用函数分层就够清晰。

# ==================== 17.2.3 避免重复代码 ====================
# 重构前：同一个会员折扣公式抄了三遍，折扣率一改就要改三处，很容易漏。
keyboard_total = round(299.0 * 2 * 0.9, 2)
mouse_total = round(79.5 * 3 * 0.9, 2)
monitor_total = round(1099.0 * 1 * 0.9, 2)
print(keyboard_total, mouse_total, monitor_total)            # -> 538.2 214.65 989.1
# 重构后：规则只写一次，数量与单价作为参数传进来，折扣率用常量。
def member_total(price: float, quantity: int, rate: float = MEMBER_RATE) -> float:
    return round(price * quantity * rate, 2)


legacy_results = (keyboard_total, mouse_total, monitor_total)
new_results = (member_total(299.0, 2), member_total(79.5, 3), member_total(1099.0, 1))
print(new_results)                                           # -> (538.2, 214.65, 989.1)
print(legacy_results == new_results)                         # -> True
# 重复的 print 也别复制三行，用循环把相同动作只写一次。
for name, price, quantity in [parse_order_row(row) for row in ORDER_ROWS]:
    print(f"{name} 会员应付 {member_total(price, quantity):.2f} 元")
# 输出三行：
# -> 机械键盘 会员应付 538.20 元
# -> 无线鼠标 会员应付 214.65 元
# -> 显示器 会员应付 989.10 元
# 判断是否真的重复：两段代码改一处必须同步改另一处，就该抽成函数或数据。
# // C++: 同样的重构目标，C++ 用函数模板或普通函数消除重复，Python 用默认参数更灵活。

# 常见坑点：
# 1. 现象：想验证计算结果只能看屏幕；原因：计算函数里直接 print；做法：计算返回数值，
#    打印放在主流程或展示函数里。
# 2. 现象：脚本一导入就自动跑一遍并打印；原因：业务代码写在模块顶层；
#    做法：收进 main()，用 if __name__ == "__main__": 调用。
# 3. 现象：改折扣率后某几行还是旧价；原因：同一个公式复制多份；做法：抽成一个函数并
#    用常量作为默认参数。
# 4. 现象：数据改了但展示代码里还写死旧值；原因：硬编码重复数据；做法：只保留一份数据源，
#    其他代码从它算出来。
# 5. 现象：所有函数都在做“解析 + 计算 + 打印”，任何改动牵一发动全身；原因：职责混杂；
#    做法：按数据层、逻辑层、展示层划分，每层只依赖下一层的数据。
