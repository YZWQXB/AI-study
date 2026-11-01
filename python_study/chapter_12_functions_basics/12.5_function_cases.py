# 第 12 章 函数基础
# 12.5 函数应用案例
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：用函数封装计算器、成绩处理和菜单流程，完整体验“拆分而不是堆叠”的写法。

from collections.abc import Callable

# ==================== 12.5.1 计算器函数封装 ====================
# 每个运算单独成函数，便于复用、替换和单独验证。
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float | None:
    if b == 0:                   # 守卫式判断：先排除不能计算的情况
        return None
    return round(a / b, 2)

print(add(12.0, 8.0))            # -> 20.0
print(subtract(12.0, 8.0))       # -> 4.0
print(multiply(2.5, 4.0))        # -> 10.0
print(divide(12.0, 3.0))         # -> 4.0
print(divide(12.0, 0.0))         # -> None

# 用字典把运算符映射到函数，避免写一长串 if-elif。
operations: dict[str, Callable[[float, float], float | None]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

def calculate(a: float, operator: str, b: float) -> float | None:
    func = operations.get(operator)
    if func is None:
        return None
    return func(a, b)

print(calculate(7.0, "+", 5.0))      # -> 12.0
print(calculate(7.0, "/", 2.0))      # -> 3.5
print(calculate(7.0, "%", 2.0))      # -> None，未知运算符
# 函数可以像普通值一样存进字典，这称为函数是一等对象。
# // C++: 可用函数指针或 std::function<double(double, double)> 存入 map，
# // 但类型声明更繁琐，Python 直接存函数对象即可。

# ==================== 12.5.2 成绩处理函数封装 ====================
# 把等级判断、平均分、及格率分别封装，主流程只负责组织数据。
def grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 60:
        return "C"
    return "D"

def average(scores: list[int]) -> float:
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)

def pass_rate(scores: list[int], passing: int = 60) -> float:
    if not scores:
        return 0.0
    passed = sum(1 for score in scores if score >= passing)
    return round(passed / len(scores) * 100, 2)

scores = [88, 72, 95, 61, 49]
print(f"平均分：{average(scores):.2f}")        # -> 平均分：73.00
print(f"及格率：{pass_rate(scores):.2f}%")     # -> 及格率：80.00%
for index, score in enumerate(scores, start=1):
    print(f"第 {index} 位  {score:>4}  {grade(score)}")
# 输出五行：
# 第 1 位    88  B
# 第 2 位    72  C
# 第 3 位    95  A
# 第 4 位    61  C
# 第 5 位    49  D

# 空列表是常见边界，函数自行处理后调用方不必再写特判。
print(f"空列表平均分：{average([])}")          # -> 空列表平均分：0.0
print(f"空列表及格率：{pass_rate([])}")        # -> 空列表及格率：0.0
# // C++: 计算平均分前也要先判断 size() 是否为 0，否则发生除零。

# ==================== 12.5.3 菜单程序函数化重构 ====================
# 重构前：菜单、命令判断和业务处理混在一个循环里，加一个功能就要改整段。
# 重构后：展示菜单、处理单条命令、驱动循环各由一个函数负责。
def show_menu() -> None:
    print("1 计算平均分")
    print("2 查询最高分")
    print("3 打印成绩单")
    print("0 退出")

def handle_command(command: str, scores: list[int]) -> bool:
    if command == "1":
        print(f"平均分：{average(scores):.2f}")
    elif command == "2":
        print(f"最高分：{max(scores)}")
    elif command == "3":
        for index, score in enumerate(scores, start=1):
            print(f"第 {index} 位：{score}")
    elif command == "0":
        print("退出菜单")
        return False
    else:
        print("未知命令")
    return True

def run_menu(scores: list[int], commands: list[str]) -> None:
    show_menu()
    for command in commands:
        print(f"输入命令：{command}")
        if not handle_command(command, scores):
            break

run_menu([88, 72, 95], ["1", "2", "3", "9", "0"])
# 输出顺序：
# 四行菜单、输入命令：1、平均分：85.00、输入命令：2、最高分：95、
# 输入命令：3、三行成绩单、输入命令：9、未知命令、输入命令：0、退出菜单
# handle_command 用返回值告诉主循环“是否继续”，避免在深层嵌套里写 break。
# // C++: 常写成 bool handleCommand(...)，主循环 while (running) { ... }，
# // Python 这里用 for 遍历固定命令列表，便于演示且不依赖 input()。

# 常见坑点：
# 1. 把 print 写进计算函数，导致同一结果无法被其他代码复用。
#    现象：想要原始数值时只能重新解析输出文本。
#    原因：计算与展示耦合。
#    正确做法：计算函数 return 结果，展示函数负责格式化输出。
# 2. 除法没有检查除数为 0，程序直接崩溃。
#    现象：抛出 ZeroDivisionError。
#    原因：浮点除法同样不允许除数为 0。
#    正确做法：先判断 b == 0 并返回 None 或明确提示。
# 3. 用一长串 if-elif 判断运算符，新增运算要改多处。
#    现象：分支越来越长，容易漏改提示文字。
#    原因：没有把“运算符到处理函数”的映射集中起来。
#    正确做法：用字典映射到函数，未知键统一返回失败标记。
# 4. 菜单函数既打印菜单又读取命令又处理业务。
#    现象：想换一种输入方式（文件、网络）时必须大改。
#    原因：输入、分发、业务三层没有分离。
#    正确做法：展示、命令处理、循环驱动拆成独立函数。
# 5. 调用计算函数时顺序参数传错，例如 divide(0, 12) 当成 0 除以 12。
#    现象：结果与预期相反或返回 None。
#    原因：同类型位置参数无法从字面上区分语义。
#    正确做法：明确参数顺序并在必要时使用关键字传参（13.1 讲解）。
