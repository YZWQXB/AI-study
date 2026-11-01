# 第 11 章 序列与基础数据处理
# 11.2 常见内置函数
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习 len、enumerate、zip、all、any、sorted、reversed 的常见用法。

# ==================== 11.2.1 len()、enumerate()、zip() ====================
# len() 对字符串、列表、元组、字典、集合都可用，返回元素个数。
scores = [88, 92, 76]
print(len(scores))                          # -> 3
print(len("Python"))                        # -> 6
# enumerate 在遍历时同时给出序号和元素；start=1 让序号从 1 开始。
for order, score in enumerate(scores, start=1):
    print(f"第 {order} 条：{score}")        # -> 见下方三行输出
# -> 第 1 条：88
# -> 第 2 条：92
# -> 第 3 条：76
# zip 把多个序列按位置配对；strict=True 要求长度一致，不一致直接抛 ValueError。
names = ["张明", "李雷", "王芳"]
pairs = list(zip(names, scores, strict=True))
print(pairs)        # -> [('张明', 88), ('李雷', 92), ('王芳', 76)]
for name, score in zip(names, scores, strict=True):
    print(f"{name}: {score}")               # -> 见下方三行输出
# -> 张明: 88
# -> 李雷: 92
# -> 王芳: 76
score_map = dict(zip(names, scores, strict=True))
print(score_map)        # -> {'张明': 88, '李雷': 92, '王芳': 76}
# // C++: 标准库没有 zip 算法，通常用一个下标同时访问两个容器；
# // Python 的 zip 返回迭代器，只能完整消费一次，需要复用先 list() 保存。
# strict=True 是 3.10 起支持的参数；不用它时 zip 会按最短序列静默截断。

# ==================== 11.2.2 all()、any() ====================
# all：全部为真才为真；any：至少一个为真就为真。它们接收一个可迭代的布尔值。
stocks = [12, 5, 0]
stock_flags = []
for stock in stocks:
    stock_flags.append(stock > 0)
print(stock_flags)                          # -> [True, True, False]
print(all(stock_flags))                     # -> False，存在缺货商品
print(any(stock_flags))                     # -> True，至少还有商品
score_flags = []
for score in scores:
    score_flags.append(score >= 60)
print(all(score_flags))                     # -> True，全部及格
print(any(score_flags))                     # -> True
# 空序列的默认语义：all([]) 为 True（没有反例），any([]) 为 False。
print(all([]))                              # -> True
print(any([]))                              # -> False
# // C++: 对应 std::all_of / std::any_of，需要传入区间和谓词函数。
# 熟练后可直接写 all(score >= 60 for score in scores) 这种生成器表达式。

# ==================== 11.2.3 sorted()、reversed() ====================
# sorted 返回新的有序列表，原序列不变；reverse=True 表示降序。
scores = [88, 92, 76, 95]
print(sorted(scores))                       # -> [76, 88, 92, 95]
print(sorted(scores, reverse=True))         # -> [95, 92, 88, 76]
print(sorted(["P03", "P01", "P02"]))        # -> ['P01', 'P02', 'P03']
print(sorted(["笔记本", "笔", "文件夹"], key=len))   # -> ['笔', '笔记本', '文件夹']
# key 接收一个函数，sorted 按这个函数的返回值比较；len 让短名称排在前面。
original = [88, 92, 76]
sorted_copy = sorted(original)
print(original)                             # -> [88, 92, 76]
print(sorted_copy)                          # -> [76, 88, 92]
# reversed 返回反向迭代器，不会修改原序列，打印成列表要加 list()。
print(list(reversed(scores)))               # -> [95, 76, 92, 88]
# // C++: std::sort 原地排序，需要副本时先复制；std::stable_sort 与 Python 的稳定排序一致。
# Python 的 sorted 是稳定排序：key 相同的元素保持原来的相对顺序。

# 常见坑点：
# 1. zip 默认按最短序列截断，容易悄悄丢数据。原因：任一序列耗尽时 zip 就停止。长度必须一致时加上 strict=True。
# 2. enumerate 默认从 0 开始，报表序号通常要写 start=1。原因：默认参数就是 start=0。
# 3. all([]) 是 True、any([]) 是 False。原因：这是“无元素”的数学约定。
#    空数据要单独判断，不能只靠 all 判断“有数据且都合格”。
# 4. 写成 data = data.sort() 会得到 None，因为 list.sort() 原地排序且返回 None；需要副本用 sorted。
# 5. zip、enumerate、reversed 返回的都是迭代器，遍历一次就耗尽，不能再按下标访问或直接打印成列表。
#    原因：迭代器只保留当前位置，不保存全部元素。
