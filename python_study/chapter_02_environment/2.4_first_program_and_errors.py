# 第 2 章 开发环境搭建与程序运行
# 2.4 第一个 Python 程序
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：以温度转换为例完成第一个实用程序，并区分语法错误与运行错误。

from pathlib import Path

# ==================== 2.4.1 编写第一个实用程序 ====================
# 不写 hello world，直接做一个有输入、计算、输出的温度转换。
celsius = 36.6
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius:.1f} 摄氏度 = {fahrenheit:.1f} 华氏度")   # -> 36.6 摄氏度 = 97.9 华氏度
# // C++: 同样的算式用 double 计算；Python 的 / 总是浮点除法，整数除法要用 //。

# ==================== 2.4.2 保存、执行与查看结果 ====================
# 文件应保存为 .py，并在终端执行 python 2.4_first_program_and_errors.py。
# __file__ 是当前脚本的路径，可用来定位同目录资源。
print("脚本文件名：", Path(__file__).name)   # -> 脚本文件名： 2.4_first_program_and_errors.py
# // C++: 可用 __FILE__ 或 argv[0] 获取源文件信息；Python 的 __file__ 是运行时属性。

# ==================== 2.4.3 初识语法错误与运行错误 ====================
# 语法错误发生在编译阶段，整个文件都无法运行；
# 运行错误发生在执行阶段，只有执行到出错语句时才触发。
try:
    compile("if True print('ok')", "<syntax-demo>", "exec")
except SyntaxError as exc:
    print("SyntaxError 阶段错误：", exc.msg)   # -> SyntaxError 阶段错误： invalid syntax

try:
    print(undefined_total)
except NameError as exc:
    print("NameError 名字未定义：", exc)       # -> NameError 名字未定义： name 'undefined_total' is not defined

try:
    int("85分")
except ValueError as exc:
    print("ValueError 值不合法：", exc)        # -> ValueError 值不合法： invalid literal for int() with base 10: '85分'
# // C++: 语法错误由编译器报告；除零、越界等在运行期才暴露。
# 阅读 traceback 时先看最后一行异常类型与信息，再自下而上定位调用链。

# 常见坑点：
# 1. 试图用 try/except 捕获当前文件自身的语法错误：文件根本没通过编译。
# 2. 只看 traceback 第一行，忽略了最后一行的真实异常原因。
# 3. 用裸 except 吞掉所有异常，导致缩进错误、拼写错误都难以发现。
# 4. 把运行结果不对归为“环境问题”，却不先用打印和断点检查中间值。
