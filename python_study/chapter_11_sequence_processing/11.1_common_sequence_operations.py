# 第 11 章 序列与基础数据处理
# 11.1 通用序列操作
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习序列的索引、切片、遍历、成员判断以及拼接与重复。

# ==================== 11.1.1 索引、切片与遍历 ====================
# 字符串、列表、元组都支持按下标访问；负数下标从末尾数，-1 是最后一个元素。
scores = [88, 92, 76, 95, 63]
print(scores[0])                            # -> 88
print(scores[-1])                           # -> 63
print(scores[1:4])                          # -> [92, 76, 95]，左闭右开
print(scores[:2])                           # -> [88, 92]
print(scores[::2])                          # -> [88, 76, 63]
print(scores[::-1])                         # -> [63, 95, 76, 92, 88]
print(scores[0:100])                        # -> [88, 92, 76, 95, 63]，切片越界自动截断
# 切片生成新列表，修改切片结果不会影响原序列；用 [] 越界才会抛 IndexError。
part = scores[1:3]
part[0] = 90
print(part)                                 # -> [90, 76]
print(scores)                               # -> [88, 92, 76, 95, 63]
# 字符串切片常用于拆分工号、日期等固定格式文本。
code = "S2024-001"
print(code[:5])                             # -> S2024
print(code[6:])                             # -> 001
# // C++: std::string 用 substr(pos, len)，std::vector 没有切片语法，只能按迭代器区间复制。
# 遍历直接 for value in scores，需要下标时再用 enumerate()（11.2 节）。

# ==================== 11.1.2 成员判断 ====================
# in 检查值是否出现在序列中；对字典则检查键，而不是值。
print(92 in scores)                         # -> True
print(100 in scores)                        # -> False
print("2024" in code)                       # -> True
print(92 in {"D01": 92})                    # -> False，字典的 in 判断键
print(92 in {"D01": 92}.values())           # -> True，判断值要显式用 values()
# 列表的 in 是线性扫描 O(n)；集合的成员判断平均 O(1)，数据量大时差异明显。
allowed_users = {"u1001", "u1002", "u1003"}
print("u1001" in allowed_users)             # -> True
print("u1004" in allowed_users)             # -> False
# // C++: std::find 返回迭代器，要再与 end() 比较；unordered_set 用 find() 平均 O(1)。

# ==================== 11.1.3 拼接与重复 ====================
# + 连接同类型序列并生成新对象；* 把序列重复若干次。
first_half = ["S01", "S02"]
second_half = ["S03", "S04"]
all_ids = first_half + second_half
print(all_ids)                              # -> ['S01', 'S02', 'S03', 'S04']
print(first_half)                           # -> ['S01', 'S02']，+ 不修改原列表
print(("admin", "editor") + ("viewer",))     # -> ('admin', 'editor', 'viewer')
print(["S05"] * 3)                          # -> ['S05', 'S05', 'S05']
print("-" * 20)                             # -> --------------------
# 列表不能和字符串直接相加，会抛 TypeError；文本拼接用 join()。
print("S01" + "-" + "S02")                  # -> S01-S02
# += 对列表是原地扩展，别名会看到变化。
ids = ["S01", "S02"]
alias = ids
ids += ["S03"]
print(alias)                                # -> ['S01', 'S02', 'S03']
# 重复运算复制的是引用，可变元素会被多个位置共享。
rows = [[0] * 3] * 2
rows[0][0] = 1
print(rows)                                 # -> [[1, 0, 0], [1, 0, 0]]
right_rows = []
for _ in range(2):
    right_rows.append([0] * 3)
right_rows[0][0] = 1
print(right_rows)                           # -> [[1, 0, 0], [0, 0, 0]]
# // C++: vector 的 operator+ 不存在，通常用 insert 追加区间；重复元素同样要防止共享指针。

# 常见坑点：
# 1. 切片是浅拷贝：列表里嵌套列表时，改切片内的子列表仍会影响原数据。原因：切片只复制外层引用。
#    需要完全独立时用 copy.deepcopy。
# 2. 下标越界抛 IndexError，而切片越界不报错，会静默截断。原因：切片允许端点超出范围并自动裁剪。
#    不能靠切片判断长度是否够。
# 3. 不同类型不能相加：["S01"] + "S02" 抛 TypeError。原因：+ 只接受同类型序列。字符串拼接应写 "S01" + "S02" 或 join。
# 4. [[0] * 3] * 2 只创建了一个内层列表的两份引用，改一行两行都变；必须逐行创建。
# 5. 字典的 in 判断键。原因：字典的成员判断只看键。要判断值用 in d.values()，要判断键值对用 in d.items()。
