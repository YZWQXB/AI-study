# 第 9 章 列表与元组
# 9.1 列表基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：创建列表、按索引与切片访问元素、遍历列表。

# ==================== 9.1.1 列表的创建 ====================
# 列表用方括号写，元素之间用逗号分隔；同一列表内的元素类型可以不同。
scores = [85, 92, 78]
print(scores)                     # -> [85, 92, 78]
print(len(scores))                # -> 3
print(type(scores))               # -> <class 'list'>
# // C++: std::vector<int> scores = {85, 92, 78}; 元素类型必须统一。
# Python 列表是动态类型容器，运行时才决定每个元素是什么。

empty_scores = []
print(empty_scores)               # -> []

# list() 可以把其他可迭代对象转换成列表，常用于 range 和字符串。
from_range = list(range(1, 5))
print(from_range)                 # -> [1, 2, 3, 4]
letters = list("ABC")
print(letters)                    # -> ['A', 'B', 'C']
# // C++: 逐个 push_back 或用迭代器区间构造 vector。

mixed = ["A100", 12, 3.5, True]
print(mixed)                      # -> ['A100', 12, 3.5, True]

# 列表可以嵌套，形成二维表格结构。
nested = [[1, 2], [3, 4]]
print(nested)                     # -> [[1, 2], [3, 4]]
# // C++: 需要 std::vector<std::vector<int>>，且每行长度由使用者自己维护。

# ==================== 9.1.2 元素访问与切片 ====================
# 下标从 0 开始，负数表示从末尾倒数。
scores = [85, 92, 78, 64, 90]
print(scores[0])                  # -> 85
print(scores[2])                  # -> 78
print(scores[-1])                 # -> 90
print(scores[-2])                 # -> 64

# 切片写作 [start:stop:step]，包含 start，不包含 stop。
print(scores[1:3])                # -> [92, 78]
print(scores[:2])                 # -> [85, 92]
print(scores[3:])                 # -> [64, 90]
print(scores[::2])                # -> [85, 78, 90]
print(scores[::-1])               # -> [90, 64, 78, 92, 85]
# // C++: 没有切片语法，需要 for 循环或 std::copy 拷贝区间。
# 切片越界不会报错，只是返回能取到的部分。
print(scores[2:100])              # -> [78, 64, 90]
# 但单个下标的索引越界会抛出 IndexError。

# 切片会生成一份新列表，修改它不会影响原列表。
part = scores[1:3]
part[0] = 100
print(part)                       # -> [100, 78]
print(scores)                     # -> [85, 92, 78, 64, 90]

# 直接赋值只是让两个名字指向同一个列表对象，不会复制。
alias = scores
alias[0] = 86
print(scores)                     # -> [86, 92, 78, 64, 90]
print(alias)                      # -> [86, 92, 78, 64, 90]
# // C++: vector 赋值是深拷贝的值语义；Python 赋值只增加一个引用，
# 这是 C++ 学习者最容易踩的差异，需要复制时写 scores[:] 或 list(scores)。

# ==================== 9.1.3 列表遍历 ====================
# 直接遍历得到元素本身。
for score in scores:
    print("成绩：", score)
# 输出：
# 成绩： 86
# 成绩： 92
# 成绩： 78
# 成绩： 64
# 成绩： 90

# 需要下标时用 enumerate()，比 range(len(...)) 更清晰。
for index, score in enumerate(scores, start=1):
    print(f"第 {index} 位：{score}")
# 输出：
# 第 1 位：86
# 第 2 位：92
# 第 3 位：78
# 第 4 位：64
# 第 5 位：90
# // C++: 常用 for (size_t i = 0; i < scores.size(); ++i)，自增下标容易出错。

# 遍历二维列表，逐行输出。
orders = [["A100", 3], ["B201", 1]]
for code, quantity in orders:
    print(f"{code} 数量 {quantity}")
# 输出：
# A100 数量 3
# B201 数量 1
# // C++: 内层容器写成 vector<string> 与 vector<int> 时无法直接解包，
# Python 的列表解包由元素数量决定，运行时才检查。

# 常见坑点：
# 1. 用 scores[5] 访问长度为 5 的列表：合法下标是 0 到 4，
#    越界会抛 IndexError，访问前先确认 len() 或改用切片。
# 2. 切片越界却以为会报错：scores[2:100] 只返回到末尾，不抛异常，
#    需要严格校验时自己判断 stop 是否超出范围。
# 3. 用 alias = scores 以为复制了列表：这只是多了一个名字，
#    修改 alias 会同时改掉 scores，真复制要写 scores[:] 或 list(scores)。
# 4. 遍历列表的同时用 remove() 删除元素：下标会前移导致漏项，
#    需要过滤时应生成新列表或倒序遍历。
# 5. 以为嵌套列表创建时各行独立：[[0] * 3] * 2 的两行是同一个对象，
#    应写 [[0] * 3 for _ in range(2)]。
