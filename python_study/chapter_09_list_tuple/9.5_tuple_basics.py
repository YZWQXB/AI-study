# 第 9 章 列表与元组
# 9.5 元组基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：理解元组的不可变性，掌握打包、解包和星号收集。

# ==================== 9.5.1 元组的定义 ====================
# 元组用圆括号写，元素之间用逗号分隔；它同样是序列，支持下标和切片。
point = (3.5, 2.0)
print(point)                          # -> (3.5, 2.0)
print(len(point))                     # -> 2
print(type(point))                    # -> <class 'tuple'>
print(point[0])                       # -> 3.5
print(point[-1])                      # -> 2.0
print(point[0:2])                     # -> (3.5, 2.0)
# // C++: 对应 std::pair 或 std::tuple，取元素要写 std::get<0>()。

# 空元组和由其他可迭代对象转换而来的元组。
empty = ()
print(empty)                          # -> ()
print(len(empty))                     # -> 0
from_list = tuple([1, 2, 3])
print(from_list)                      # -> (1, 2, 3)

# 元组也可以嵌套，常用于一条记录由多个字段组成。
record = ("A100", (12, 3.5))
print(record)                         # -> ('A100', (12, 3.5))
print(record[1][0])                   # -> 12

# ==================== 9.5.2 元组的不可变性 ====================
# 创建后不能修改元素，也不能增删元素。
origin = (0, 0)
# origin[0] = 5   # 取消注释会抛 TypeError: 'tuple' object does not support item assignment
print(origin)                         # -> (0, 0)
# // C++: 类似 const 数组，区别是 Python 的不可变由对象本身保证，不是变量修饰。

# 可以用加号或重复运算符拼接出新元组，原元组保持不变。
extended = origin + (1,)
print(extended)                       # -> (0, 0, 1)
repeated = ("A",) * 3
print(repeated)                       # -> ('A', 'A', 'A')

# 因为不可变且可哈希，元组可以直接作为字典的键。
location_counts = {("A区", "01"): 3, ("B区", "02"): 5}
print(location_counts[("A区", "01")])  # -> 3
# // C++: std::map 的键只要可比较即可，Python 要求键必须可哈希。

# 但“不可变”只针对顶层元素：元组里的列表仍然可以修改。
record = ("A100", [10, 20])
record[1].append(30)
print(record)                         # -> ('A100', [10, 20, 30])
# 需要真正不可变的数据，内部也应使用元组等不可变类型。

# ==================== 9.5.3 打包与解包 ====================
# 多个值用逗号写在一起就是打包成元组，括号可以省略。
warehouse = "A100", 12, 3.5
print(warehouse)                      # -> ('A100', 12, 3.5)

# 解包把元组的各个元素分别赋给变量，数量必须与元素个数一致。
code, quantity, price = warehouse
print(code)                           # -> A100
print(quantity)                       # -> 12
print(price)                          # -> 3.5
# // C++: 需要 std::tie 或结构化绑定（C++17 的 auto [a, b, c]）。

# 解包也常用于交换两个变量，不需要临时变量。
left, right = 1, 2
left, right = right, left
print(left, right)                    # -> 2 1

# 星号变量收集剩余元素，得到的是列表，且只能出现一个。
scores = [88, 76, 95, 61]
first, *middle, last = scores
print(first)                          # -> 88
print(middle)                         # -> [76, 95]
print(last)                           # -> 61

# 遍历时直接解包，比按下标取值更清楚。
for code, quantity in [("A100", 12), ("B201", 0)]:
    print(f"{code} 库存 {quantity}")
# 输出：
# A100 库存 12
# B201 库存 0

# zip 解包时用 strict=True，两个序列长度不一致会立即报错。
codes = ["A100", "B201"]
quantities = [12, 0]
for code, quantity in zip(codes, quantities, strict=True):
    print(code, quantity)
# 输出：
# A100 12
# B201 0
# // C++: 没有直接对应写法，需要自己保证两个容器长度一致。

# 单元素元组必须带逗号，括号本身不能造出元组。
not_tuple = (5)
print(type(not_tuple))                # -> <class 'int'>
single = (5,)
print(single)                         # -> (5,)
print(len(single))                    # -> 1
also_single = 5,
print(also_single)                    # -> (5,)

# 常见坑点：
# 1. 写 single = (5) 以为创建了元组：括号只是分组，
#    单元素元组必须写 (5,) 或 5,，逗号才是元组的关键。
# 2. 试图给元组元素赋值：会抛 TypeError，需要修改时应先用 list() 转成列表，
#    改完再 tuple() 转回。
# 3. 认为元组完全不可变：元组内若包含列表，列表内容仍可修改，
#    需要深层不可变时内部元素也要用不可变类型。
# 4. 解包时变量个数与元素个数不一致：会抛 ValueError，
#    不确定长度时用 *rest 收集剩余元素。
# 5. 把元组当可变容器使用：元组没有 append、remove 等方法，
#    需要频繁增删时应改用列表。
