# 第 9 章 列表与元组
# 9.4 排序与统计基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：掌握 sort 与 sorted 的区别、key 规则和常用统计函数。

# ==================== 9.4.1 sort() 与 sorted() ====================
# sort 原地排序，修改列表本身并返回 None；sorted 返回新列表，原数据不变。
scores = [88, 61, 95, 76]
scores.sort()
print(scores)                         # -> [61, 76, 88, 95]
scores.sort(reverse=True)
print(scores)                         # -> [95, 88, 76, 61]

original = [88, 61, 95, 76]
ranked = sorted(original)
print(ranked)                         # -> [61, 76, 88, 95]
print(original)                       # -> [88, 61, 95, 76]
# // C++: std::sort 对应原地排序；需要副本时先拷贝一份再 sort。

# sort() 的返回值是 None，不要写成 ranked = scores.sort()。
print(scores.sort())                  # -> None
print(scores)                         # -> [61, 76, 88, 95]
# 这行 sort() 又执行了一次默认升序排序，所以列表从降序变回升序。

# key 指定排序依据，函数只接收一个元素并返回用于比较的键。
records = [("A100", 12), ("B201", 0), ("C305", 25)]
by_quantity = sorted(records, key=lambda record: record[1])
print(by_quantity)                    # -> [('B201', 0), ('A100', 12), ('C305', 25)]
by_quantity_desc = sorted(records, key=lambda record: record[1], reverse=True)
print(by_quantity_desc)               # -> [('C305', 25), ('A100', 12), ('B201', 0)]
# // C++: 需要写比较函数或 lambda 传给 std::sort，Python 用 key 抽取排序字段。

# key 也可以调用内置函数，例如按绝对值排序。
numbers = [-5, 3, -1, 8]
print(sorted(numbers, key=abs))       # -> [-1, 3, -5, 8]

# 字符串默认按字符码点比较，大小写混排时通常要统一成小写再比较。
names = ["Beta", "alpha", "Gamma", "beta"]
print(sorted(names))                  # -> ['Beta', 'Gamma', 'alpha', 'beta']
print(sorted(names, key=str.lower))   # -> ['alpha', 'Beta', 'beta', 'Gamma']

# ==================== 9.4.2 len()、max()、min()、sum() ====================
# 四个内置函数直接作用于列表，不需要导入模块。
scores = [88, 76, 95, 61, 88]
print(len(scores))                    # -> 5
print(max(scores))                    # -> 95
print(min(scores))                    # -> 61
print(sum(scores))                    # -> 408
print(sum(scores) / len(scores))      # -> 81.6
print(round(sum(scores) / len(scores), 1))  # -> 81.6
# // C++: 需要 std::accumulate 或手写循环求总和、最值。

# max 和 min 也支持 key，可以按指定字段取出整条记录。
records = [("A100", 12), ("B201", 0), ("C305", 25)]
print(max(records, key=lambda record: record[1]))  # -> ('C305', 25)
print(min(records, key=lambda record: record[1]))  # -> ('B201', 0)

# 统计高分人数时，先用条件过滤再计数，避免把判断散落在多处。
high_scores = [score for score in scores if score >= 88]
print(len(high_scores))               # -> 3
print(sum(high_scores))               # -> 271

# ==================== 9.4.3 简单排序规则 ====================
# 元组默认按“第一个元素，然后第二个元素”依次比较，即字典序。
print(sorted([("B", 3), ("A", 5), ("B", 1)]))  # -> [('A', 5), ('B', 1), ('B', 3)]

# 多字段排序把 key 写成元组：先按库存升序，库存相同再按单价升序。
stock = [("A100", 12, 3.5), ("B201", 0, 9.0), ("C305", 12, 2.0), ("D407", 5, 7.5)]
by_quantity_price = sorted(stock, key=lambda item: (item[1], item[2]))
print(by_quantity_price)
# 输出：
# [('B201', 0, 9.0), ('D407', 5, 7.5), ('C305', 12, 2.0), ('A100', 12, 3.5)]

# 想对某个字段降序，可以在 key 里取负号，保持其余字段升序。
quantity_desc = sorted(stock, key=lambda item: (-item[1], item[2]))
print(quantity_desc)
# 输出：
# [('C305', 12, 2.0), ('A100', 12, 3.5), ('D407', 5, 7.5), ('B201', 0, 9.0)]
# // C++: 需要自己写多字段比较函数，容易漏掉某个字段。
# 也可以用 operator.itemgetter(1, 2) 作为 key，等价于取元组字段。

# 排序是稳定的：键相同的元素保持原有先后顺序。
teams = [("一组", 88), ("二组", 95), ("一组", 72), ("二组", 90)]
by_score_desc = sorted(teams, key=lambda item: item[1], reverse=True)
print(by_score_desc)
# 输出：
# [('二组', 95), ('二组', 90), ('一组', 88), ('一组', 72)]
grouped = sorted(by_score_desc, key=lambda item: item[0])
print(grouped)
# 输出：
# [('一组', 88), ('一组', 72), ('二组', 95), ('二组', 90)]
# 利用稳定性：先按次要键排序，再按主要键排序，组内顺序即可保留。

# 常见坑点：
# 1. 写 ranked = scores.sort()：sort 原地排序并返回 None，
#    ranked 会变成 None；需要新列表时用 sorted(scores)。
# 2. 对混合类型列表直接排序：整数和字符串无法比较，会抛 TypeError，
#    应先统一类型，或用 key 把比较值转换成同一类型。
# 3. 把 key 写成 key=record[1]：这里只是取了一个值，要传函数，
#    正确写法是 key=lambda record: record[1]。
# 4. 对空列表调用 max() 或 min()：会抛 ValueError，sum() 却返回 0，
#    统计前先判断 if scores: 处理空数据。
# 5. 多字段排序时只用一次 reverse=True：它会把所有字段一起反转，
#    需要“一升一降”时应把降序字段取负，或使用元组 key。
