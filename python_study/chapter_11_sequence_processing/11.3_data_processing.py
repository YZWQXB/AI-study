# 第 11 章 序列与基础数据处理
# 11.3 基础数据处理方法
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习统计、查找、筛选与去重这四类最常用的数据处理操作。

# ==================== 11.3.1 统计 ====================
# 长度、求和、最值、平均是最基础的一组统计，内置函数都能直接完成。
sales = [120, 340, 260, 180]
print(len(sales))                           # -> 4
print(sum(sales))                           # -> 900
print(max(sales))                           # -> 340
print(min(sales))                           # -> 120
print(sum(sales) / len(sales))              # -> 225.0
# 需要按类别汇总时，用字典累加：get 提供初始值 0。
records = [("P01", 120), ("P02", 340), ("P01", 260)]
totals = {}
for sku, amount in records:
    totals[sku] = totals.get(sku, 0) + amount
print(totals)                               # -> {'P01': 380, 'P02': 340}
print(sum(totals.values()))                 # -> 720
# // C++: accumulate 配合自定义初值可做汇总；按类别累加通常用 map<string, int> 的 [] 自增。

# ==================== 11.3.2 查找 ====================
# in 判断存在，index 返回第一个匹配位置；找不到时会抛 ValueError。
students = ["张明", "李雷", "王芳"]
print("李雷" in students)                   # -> True
print(students.index("王芳"))               # -> 2
target = "赵强"
if target in students:
    print(students.index(target))           # 该分支不会执行，赵强不在名单中
else:
    print(-1)                               # -> -1
# 查找整条记录时，遍历并在命中后 break，保留 first 匹配的语义。
records = [
    {"id": "S01", "score": 88},
    {"id": "S02", "score": 92},
    {"id": "S03", "score": 58},
]
query = "S02"
matched = None
for record in records:
    if record["id"] == query:
        matched = record
        break
if matched is None:
    print("未找到")                         # 该分支不会执行，S02 已命中
else:
    print(matched["score"])                 # -> 92
# // C++: std::find 返回迭代器，需判断是否为 end()；std::string::find 找不到时返回 npos，不是 -1。

# ==================== 11.3.3 筛选 ====================
# 筛选就是“保留满足条件的元素”，结果通常放进新列表，不改动原数据。
scores = [88, 55, 92, 76, 43]
passed = []
for score in scores:
    if score >= 60:
        passed.append(score)
print(passed)                               # -> [88, 92, 76]
print(len(passed))                          # -> 3
print(len(scores) - len(passed))            # -> 2
# 多条件筛选按业务顺序写判断；命中就进入结果集，不命中就跳过。
products = [("P01", 12.0), ("P02", 3.5), ("P03", 26.0)]
affordable = []
for name, price in products:
    if price <= 15.0 and name.startswith("P"):
        affordable.append(name)
print(affordable)                           # -> ['P01', 'P02']
# // C++: 对应 std::copy_if，需要额外的结果容器与谓词函数。

# ==================== 11.3.4 去重 ====================
# dict.fromkeys 以元素作键，天然去重且保留首次出现的顺序。
logs = ["home", "detail", "home", "cart", "detail"]
unique_pages = list(dict.fromkeys(logs))
print(unique_pages)                         # -> ['home', 'detail', 'cart']
print(len(unique_pages))                    # -> 3
# 只关心种类数量时用集合；集合无序，不能直接展示访问顺序。
print(len(set(logs)))                       # -> 3
# 去重和计数常常一起做：一次遍历同时得到次数。
visit_counts = {}
for page in logs:
    visit_counts[page] = visit_counts.get(page, 0) + 1
print(visit_counts)     # -> {'home': 2, 'detail': 2, 'cart': 1}
# // C++: std::unique 只能去掉相邻重复，通常要先排序；保留原顺序需要 set + 手工插入。

# 常见坑点：
# 1. 对空列表求平均会抛 ZeroDivisionError。原因：除数是 len(data)，空列表时为 0。先判断 len(data) 是否为 0。
# 2. list.index() 找不到时抛 ValueError，不像 C++ string::find 那样返回 npos。
#    原因：index 只返回成功结果，没有失败返回值。先用 in 判断。
# 3. set 去重会打乱顺序。原因：集合基于哈希表，不保存位置。需要保留首次出现顺序时必须用 dict.fromkeys。
# 4. 先 in 再 index 会扫描两遍；大数据量下一次遍历并用 break 更高效。
# 5. sum() 不能直接拼接字符串列表。原因：sum 默认从整数 0 开始相加，0 + str 会抛 TypeError。字符串拼接用 "".join()。
