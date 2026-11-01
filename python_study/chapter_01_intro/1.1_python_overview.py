# 第 1 章 Python 语言认知与学习方法
# 1.1 Python 语言概述
# 学习优先级：P2（进阶了解） | 掌握要求：理解
# 本文件：用可运行代码认识 Python 的版本、类型系统、数值模型与典型用途。

import sys
from collections import Counter

# ==================== 1.1.1 Python 的发展历史 ====================
# Python 由 Guido van Rossum 于 1991 年发布，2008 年推出的 Python 3 与 2.x 不兼容。
# 本课程统一使用 Python 3.12+，示例会用到 3.10 之后才有的语法特性。
print("解释器版本：", sys.version.split()[0])               # -> 解释器版本： 3.12.15
print("满足 3.12+：", sys.version_info >= (3, 12))          # -> 满足 3.12+： True
# // C++: 通常用 __cplusplus 或 __cpp_* 宏判断标准版本；Python 在运行时判断 sys.version_info。
if sys.version_info < (3, 12):
    raise SystemExit("本课程示例需要 Python 3.12 或更高版本")

# ==================== 1.1.2 Python 的核心特点 ====================
# 特点一：变量名只是对象的引用，赋值不会复制对象，名字还可以重新绑定到其他类型。
score = 92
backup = score                    # backup 与 score 指向同一个整数对象
print("重新绑定前：", score, backup)   # -> 重新绑定前： 92 92
score = "九十二"                   # 同一个名字改指向 str 对象
print("重新绑定后：", score, backup)   # -> 重新绑定后： 九十二 92
# // C++: int score = 92; 之后不能赋成 std::string；变量类型在编译期固定。

# 特点二：整数没有固定位宽，不会像 C++ 的 uint64_t 那样溢出。
big_number = 2 ** 100
print("2 的 100 次方：", big_number)   # -> 2 的 100 次方： 1267650600228229401496703205376
# // C++: 2^100 早已超出 64 位整数范围，需要大整数库或自行实现。

# 特点三：内置列表、字典等高层容器，并支持负索引与切片。
flight_codes = ["A1001", "B2002", "C3003"]
print("首尾航班：", flight_codes[0], flight_codes[-1])   # -> 首尾航班： A1001 C3003
print("前两条：", flight_codes[:2])                      # -> 前两条： ['A1001', 'B2002']
print("倒序：", flight_codes[::-1])                      # -> 倒序： ['C3003', 'B2002', 'A1001']
# // C++: std::vector 不支持负下标，切片需要用迭代器或下标循环手动构造。

# 特点四：赋值共享对象，修改可变对象会同时影响所有引用它的名字。
order = {"id": "A1001", "amount": 199.0}
same_order = order
same_order["amount"] = 188.0
print("原订单金额：", order["amount"])   # -> 原订单金额： 188.0
# // C++: 结构体赋值默认复制值；Python 这里不是复制，需要 copy.deepcopy 才会独立。

# ==================== 1.1.3 Python 的典型应用场景 ====================
# 数据分析与文本处理是最常见的入门场景：标准库 Counter 可以直接完成词频统计。
text = "Python is simple, Python is readable, and Python is widely used"
words = [word.strip(",.").lower() for word in text.split()]
print("高频词：", Counter(words).most_common(2))   # -> 高频词： [('python', 3), ('is', 3)]
# // C++: 需要 unordered_map 统计，再按次数排序；Python 用标准库三行即可完成。
# 其他典型场景：自动化脚本、Web 后端（Django/FastAPI）、爬虫、机器学习与科学计算。

# 常见坑点：
# 1. 把 Python 2 的 print 语句或 "except A, e" 写法带进 3.12，会直接产生语法错误。
# 2. 以为 a = b 是复制：两个名字指向同一可变对象，改一个会影响另一个。
# 3. 用 C++ 思维给每个名字先声明类型：Python 的变量没有类型，类型属于对象。
# 4. 以为整数会溢出：Python 整数可无限增长，但大数运算更慢，仍要关注算法复杂度。
