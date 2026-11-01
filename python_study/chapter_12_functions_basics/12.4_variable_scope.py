# 第 12 章 函数基础
# 12.4 变量作用域
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习局部变量与全局变量、LEGB 查找规则，以及 global 的风险和 nonlocal 入门。

# ==================== 12.4.1 局部变量 ====================
# 在函数内部赋值的名字默认是局部变量，只在本次调用期间存在。
counter = 10

def add_one() -> None:
    counter = 1                  # 新建局部变量，遮蔽了外面的同名变量
    counter += 1
    print(f"函数内 counter：{counter}")

add_one()                        # -> 函数内 counter：2
print(f"函数外 counter：{counter}")    # -> 函数外 counter：10
# // C++: 函数内 int counter = 1; 会遮蔽全局变量，作用规则类似。

# 局部变量在函数返回后就不存在了，函数外无法访问。
def build_message() -> str:
    message = "订单已提交"
    return message

print(build_message())           # -> 订单已提交
# print(message)                 # NameError: name 'message' is not defined

# 不同函数即使使用同名局部变量，也各自独立。
def calc_area() -> float:
    size = 6.0
    return size * size

def calc_perimeter() -> float:
    size = 4.0
    return size * 4

print(calc_area(), calc_perimeter())    # -> 36.0 16.0
# // C++: 同名局部变量位于不同函数栈帧，互不影响，机制相同。

# ==================== 12.4.2 全局变量 ====================
# 模块级定义的变量是全局变量；函数内可以直接读取，但修改需要 global 声明。
total_calls = 0

def record_call() -> None:
    global total_calls           # 声明这里修改的是模块级 total_calls
    total_calls += 1

record_call()
record_call()
record_call()
print(f"累计调用次数：{total_calls}")     # -> 累计调用次数：3

# 没有 global 时，total_calls += 1 会被当作新建局部变量，随后读取时报错。
def record_call_wrong() -> None:
    # total_calls += 1           # UnboundLocalError: 局部变量在赋值前被引用
    pass

# 原地修改可变对象不需要 global，因为并没有重新绑定名字。
orders = []

def add_order(order: str) -> None:
    orders.append(order)         # 只是调用列表方法，没有给 orders 赋值

add_order("A1001")
add_order("A1002")
print(orders)                    # -> ['A1001', 'A1002']

# 但用全局变量在函数之间传递数据会隐藏依赖关系，推荐改为参数传入、返回值传出。
def calc_final_price(amount: float, tax_rate: float) -> float:
    return round(amount * (1 + tax_rate), 2)

print(calc_final_price(600.0, 0.13))    # -> 678.0
# // C++: 全局变量同样能读写，但大型程序通常用参数和返回值隔离状态。

# ==================== 12.4.3 作用域常见问题 ====================
# Python 按 LEGB 顺序查找名字：局部 L、外层函数 E、全局 G、内置 B。
rate = 0.13                      # G：模块级

def show_rate() -> None:
    rate = 0.09                  # L：局部变量遮蔽全局变量
    print(f"函数内税率：{rate}")

show_rate()                      # -> 函数内税率：0.09
print(f"模块级税率：{rate}")     # -> 模块级税率：0.13

def outer() -> None:
    label = "外层"
    def inner() -> None:
        print(f"inner 读到的 label：{label}")    # E：外层函数的局部变量
    inner()

outer()                          # -> inner 读到的 label：外层
# // C++: 没有 LEGB 概念；嵌套函数对外层局部变量的访问是 Python 特有规则。

# 局部变量可以遮蔽内置函数名，导致函数内无法再使用原内置函数。
def count_items_bad(items: list[int]) -> int:
    len = 3                      # 遮蔽内置 len
    print(f"局部 len 的值：{len}")    # -> 局部 len 的值：3
    return len                   # 返回常量 3，而不是列表长度

print(count_items_bad([1, 2, 3, 4]))    # -> 3

def count_items(items: list[int]) -> int:
    return len(items)            # 正常使用内置 len

print(count_items([1, 2, 3, 4]))        # -> 4
# 不要用内置名（len、list、sum、max）作为变量名或形参名。

# 闭包：内层函数引用外层函数的局部变量；要修改它必须声明 nonlocal。
from collections.abc import Callable

def make_counter(start: int) -> Callable[[], int]:
    count = start
    def next_value() -> int:
        nonlocal count           # 修改外层函数的 count，而不是新建局部变量
        count += 1
        return count
    return next_value

counter_a = make_counter(0)
counter_b = make_counter(10)
print(counter_a(), counter_a(), counter_a())    # -> 1 2 3
print(counter_b())                              # -> 11
# 每个闭包有自己独立的环境，所以两个计数器互不影响。
# nonlocal 修改外层函数变量，global 修改模块级变量，二者不能混用。
# // C++: 可用 lambda 按引用捕获局部变量（[&count]() mutable { return ++count; }），
# // 或写一个保存状态的仿函数类；C++ 没有 nonlocal 关键字。

# 常见坑点：
# 1. 在函数内给全局变量赋值却没写 global。
#    现象：抛出 UnboundLocalError，提示变量在赋值前被引用。
#    原因：赋值语句让该名字在整个函数内都被判定为局部变量。
#    正确做法：确实要修改全局变量时在函数开头写 global，更推荐改用返回值。
# 2. 以为在函数内 counter = 1 会修改函数外的 counter。
#    现象：函数外变量保持原值。
#    原因：赋值只是新建局部变量并遮蔽同名全局变量。
#    正确做法：用 return 返回新值，或使用可变容器并明确说明。
# 3. 用内置函数名做变量名，例如 len = 3、list = []。
#    现象：后续调用 len(...) 抛出 TypeError: 'int' object is not callable。
#    原因：局部或全局名字遮蔽了内置名字。
#    正确做法：变量名改为 length、items 这类具体名字。
# 4. 在闭包内修改外层变量却忘记 nonlocal。
#    现象：抛出 UnboundLocalError，或每次调用都从初始值开始。
#    原因：赋值让 count 变成闭包内的新局部变量。
#    正确做法：需要修改时声明 nonlocal count；只读取时不需要声明。
# 5. 函数通过全局变量读写数据，导致结果依赖调用顺序。
#    现象：同样输入得到不同结果，难以单独测试。
#    原因：函数与模块级状态耦合。
#    正确做法：把依赖作为参数传入，把结果通过 return 交回。
