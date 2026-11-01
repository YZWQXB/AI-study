# 第 15 章 异常处理与基础调试
# 15.1 错误与异常基础
# 学习优先级：P1（重点掌握） | 掌握要求：理解
# 本文件：区分语法错误、运行时异常和逻辑错误，并学会用 compile() 提前检查代码能否编译。

from pathlib import Path
import tempfile

# ==================== 15.1.1 语法错误 ====================
# 语法错误在编译阶段就暴露，代码一行都不会执行，所以 try/except 根本来不及生效。
broken_source = "total = 0\nif total = 3:\n    print(total)\n"
try:
    compile(broken_source, "<演示代码>", "exec")
except SyntaxError as error:
    print("类型：", type(error).__name__)                        # -> 类型： SyntaxError
    print("信息：", error.msg)                                   # -> 信息： invalid syntax. Maybe you meant '==' or ':=' instead of '='?
    print("位置：第", error.lineno, "行，第", error.offset, "列")  # -> 位置：第 2 行，第 4 列
    print("问题行：", error.text.strip())                        # -> 问题行： if total = 3:
# // C++: 语法错误由编译器报告，无法生成可执行文件；Python 的 compile() 只检查语法，不执行代码。
# 括号不配对、冒号缺失、缩进错乱同样属于这一类；异常信息里通常已经指出正确写法。

# ==================== 15.1.2 运行时异常 ====================
# 语法完全正确，但执行到某条语句时出错，这类错误才是 try/except 能处理的异常。
def average(total: int, count: int) -> float:
    return total / count

try:
    print("正常调用：", average(87, 3))       # -> 正常调用： 29.0
    print("异常调用：", average(87, 0))
except ZeroDivisionError as error:
    print("捕获类型：", type(error).__name__)   # -> 捕获类型： ZeroDivisionError
    print("异常信息：", error)                  # -> 异常信息： division by zero
# 异常发生时，try 中剩下的语句会被跳过，直接跳到匹配的 except 分支。

with tempfile.TemporaryDirectory() as temp_dir:
    try:
        (Path(temp_dir) / "config.ini").read_text(encoding="utf-8")
    except FileNotFoundError as error:
        print("文件缺失：", type(error).__name__)   # -> 文件缺失： FileNotFoundError
# 这里只打印异常类型而不打印 error：它的信息里带着本机绝对路径，不适合作为固定输出。

# ==================== 15.1.3 逻辑错误 ====================
# 程序不报错、能跑完，只是结果不符合业务预期；只能靠对照预期值或检查中间结果发现。
scores = [78, 92, 65, 88]

def average_wrong(values: list[int]) -> float:
    total = 0
    for index in range(len(values) - 1):
        total += values[index]
    return total / len(values)

def average_right(values: list[int]) -> float:
    return sum(values) / len(values)

print("错误算法：", average_wrong(scores))       # -> 错误算法： 58.75
print("正确算法：", average_right(scores))       # -> 正确算法： 80.75
# 两个函数都能正常返回，没有任何异常，差别只在循环少遍历了最后一个元素。

def average_wrong_traced(values: list[int]) -> float:
    total = 0
    for index in range(len(values) - 1):
        total += values[index]
        print(f"  第 {index} 次累加后总分：{total}")
    print(f"  参与平均的元素个数：{len(values)}")
    return total / len(values)

print("带中间输出的错误算法：")
print(average_wrong_traced(scores))
# 输出：
# 带中间输出的错误算法：
#   第 0 次累加后总分：78
#   第 1 次累加后总分：170
#   第 2 次累加后总分：235
#   参与平均的元素个数：4
# 58.75
# 中间值显示累加只做了 3 次、分母却用了 4，问题就落在 range(len(values) - 1) 上。

# 常见坑点：
# 1. 用 try/except 去包带语法错误的代码：SyntaxError 发生在编译期，try 还没建立；应先用 compile() 或直接运行检查。
# 2. 把逻辑错误当成异常去搜索：它不抛任何异常，只能对比预期值与中间结果；先写清预期再验证。
# 3. 用 eval/exec 执行用户输入的表达式：语法错误与安全风险都难控制；结构化数据应交给专门的解析函数。
# 4. 只看最终结果不打印中间值：定位不到具体出错的那一步；临时加上带标记的 print。
# 5. 认为 except Exception 能兜住一切：语法错误与解释器层面的严重问题不在此列，不要依赖它掩盖问题。
