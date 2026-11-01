# 第 12 章 函数基础
# 12.2 函数定义与调用
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习 def 语法、函数调用过程，以及用文档字符串描述函数的输入与输出。

# ==================== 12.2.1 def 语法 ====================
# def 函数名(参数列表): 后面接缩进代码块；函数体只有在被调用时才执行。
def show_greeting(name: str) -> None:
    print(f"欢迎你，{name}")

print("定义完成，函数体还没有执行")
show_greeting("小林")        # -> 欢迎你，小林
show_greeting("阿强")        # -> 欢迎你，阿强
# // C++: void showGreeting(std::string name) { std::cout << "欢迎你，" << name << std::endl; }
# Python 用缩进代替花括号，def 行末的冒号不能省略，函数体至少缩进一级。

# 无参数、无返回值的函数：每次调用都重新执行函数体。
def show_order_total() -> None:
    price = 25.0
    quantity = 4
    print(f"合计：{price * quantity:.2f}")

show_order_total()           # -> 合计：100.00
show_order_total()           # -> 合计：100.00
# price、quantity 是每次调用时新建的局部变量，两次调用互不影响。
# // C++: 局部变量在函数调用时创建，函数返回时销毁，机制相同。

# 函数必须先定义后调用，否则名字还不存在。
# show_later()               # 取消注释会抛出 NameError，因为定义在这行之后
# def show_later() -> None:
#     print("稍后定义的函数")

# ==================== 12.2.2 调用过程 ====================
# 调用时先跳进函数体，执行到 return 或函数末尾，再回到调用处继续往下执行。
def calc_tax(amount: float) -> float:
    print("    进入 calc_tax")
    tax = amount * 0.06
    print("    计算完成，准备返回")
    return tax

print("调用前")
tax = calc_tax(200.0)
print(f"调用后，税额：{tax}")        # -> 调用后，税额：12.0
print("调用结束后继续执行下一行")
# 完整输出顺序：调用前、进入 calc_tax、计算完成，准备返回、调用后、调用结束后继续执行下一行。
# // C++: 函数调用同样会压栈、执行、返回；Python 的函数调用开销相对更大。

# return 一旦执行，函数立即结束，后面的语句不会再执行。
def check_stock(stock: int, wanted: int) -> str:
    if wanted <= 0:
        return "数量必须大于 0"
    if stock < wanted:
        return "库存不足"
    return "可以出货"

print(check_stock(5, 3))     # -> 可以出货
print(check_stock(2, 5))     # -> 库存不足
print(check_stock(5, 0))     # -> 数量必须大于 0
# 提前 return 让正常路径不用再套一层 else，这也是后续常用的“守卫式”写法。

# ==================== 12.2.3 文档字符串基础 ====================
# 三引号字符串写在函数体第一行就是 docstring，用来描述参数、返回值和调用方式。
def calc_discount(total: float) -> float:
    """计算订单满减优惠，满 100 元减 15 元。

    参数：
        total: 订单原价，单位为元。
    返回：
        优惠金额；未达到 100 元时返回 0.0。
    """
    if total >= 100:
        return 15.0
    return 0.0

print(calc_discount(120.0))                              # -> 15.0
print(calc_discount(80.0))                               # -> 0.0
print(calc_discount.__doc__.strip().splitlines()[0])     # -> 计算订单满减优惠，满 100 元减 15 元。
# docstring 保存在函数对象的 __doc__ 属性中，IDE 提示和 help() 都会读取它。
# // C++: 通常用 /** ... */ 或 /// 注释，编译后不保留；Python 的文档字符串会随函数对象保留。

# 单行 docstring 适用于简单函数：一句话说明做什么即可。
def format_price(value: float) -> str:
    """把价格格式化为两位小数的字符串。"""
    return f"{value:.2f}"

print(format_price(9.5))                                 # -> 9.50
print(format_price.__doc__)                              # -> 把价格格式化为两位小数的字符串。

# 常见坑点：
# 1. 只写 def 不加括号，以为会执行函数。
#    现象：输出类似 <function show_greeting at 0x...> 的文本，函数体没有运行。
#    原因：函数名本身是一个函数对象。
#    正确做法：调用必须写成 函数名(实参)，即使没有参数也要写空括号。
# 2. 函数内忘记写 return，调用处却使用返回值。
#    现象：得到 None，后续运算抛出 TypeError。
#    原因：没有 return 的函数默认返回 None。
#    正确做法：需要结果时显式 return；只做展示的函数可以返回 None 并在命名上体现。
# 3. 把 docstring 写在函数体第二行或写在 def 上方。
#    现象：函数的 __doc__ 是 None。
#    原因：只有函数体第一条语句的三引号字符串才算 docstring。
#    正确做法：docstring 紧跟在 def 行之后，且位于任何可执行语句之前。
# 4. 缩进层级不一致，或混用空格与制表符。
#    现象：抛出 IndentationError 或 TabError。
#    原因：Python 用缩进定义代码块。
#    正确做法：整个文件统一用 4 个空格缩进。
# 5. 在定义之前调用函数。
#    现象：抛出 NameError: name 'show_later' is not defined。
#    原因：Python 从上到下执行，def 执行后名字才被绑定。
#    正确做法：先定义后调用；被多处使用的函数放到文件顶部。
