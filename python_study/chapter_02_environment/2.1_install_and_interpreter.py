# 第 2 章 开发环境搭建与程序运行
# 2.1 Python 安装与版本基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：确认解释器信息、理解字节码执行流程，并识别 3.x 版本差异。

import sys

# ==================== 2.1.1 Python 安装与验证 ====================
# 安装后可在终端执行 python --version 或 py -0p 查看版本；
# 脚本内部则通过 sys 模块获取同一份信息，便于做版本兼容判断。
print("版本：", sys.version.split()[0])        # -> 版本： 3.12.15
print("实现：", sys.implementation.name)      # -> 实现： cpython
print("最大索引值：", sys.maxsize)             # -> 最大索引值： 9223372036854775807
# // C++: 常用 sizeof(void*) 和 INT_MAX 判断平台；Python 的 sys.maxsize 表示索引上限。
# 多个版本同时安装时，Windows 可用 py -3.12 指定解释器，避免调错版本。

# ==================== 2.1.2 Python 解释器的基本概念 ====================
# Python 先把源码编译为字节码，再由虚拟机执行；不是逐字符直接解释。
# compile() 返回代码对象，co_names 记录源码中出现的全局名字。
source = "result = 6 * 7"
code = compile(source, "<demo>", "exec")
print("代码对象中的名字：", code.co_names)   # -> 代码对象中的名字： ('result',)
namespace = {}
exec(code, namespace)
print("执行结果：", namespace["result"])      # -> 执行结果： 42
# // C++: 编译产物是机器码，运行时没有 exec 这种“执行字符串代码”的常规能力；
# // Python 的 exec/eval 灵活但会绕过静态检查，生产代码应谨慎使用。
# 首次导入模块后会在 __pycache__ 生成 .pyc 字节码缓存，源文件不变时直接复用。

# ==================== 2.1.3 Python 3 版本认知 ====================
# 3.8 之后新增了海象运算符、联合类型、match、异常组、PEP 701 f-string 等能力。
# 本课程使用 3.12，因此可以直接写下标类型和字典类型，不必导入 typing。
print("主次版本：", sys.version_info[:2])   # -> 主次版本： (3, 12)
scores: dict[str, int] = {"语文": 91, "数学": 88}
print("类型标注：", list(scores.items()))    # -> 类型标注： [('语文', 91), ('数学', 88)]
# 3.12 的 f-string 允许在表达式内复用外层引号，下面的写法在 3.8 会报语法错误。
record = {"name": "林同学", "score": 95}
print(f"{record['name']} 的成绩是 {record['score']}")   # -> 林同学 的成绩是 95
# // C++: 语言标准由编译器决定；Python 由解释器版本决定，部署前要确认目标版本。

# 常见坑点：
# 1. 终端里的 python 指向旧版本，代码用了 3.12 语法却报 SyntaxError。
# 2. 以为 Python 是纯解释执行，忽略 .pyc 缓存和字节码编译阶段。
# 3. 用 exec/eval 执行外部输入，可能引入安全风险，且失去静态检查。
# 4. 只看版本号数字，不确认实现（CPython、PyPy 等行为与性能可能不同）。
