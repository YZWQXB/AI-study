# 第 8 章 推导式与基础表达式优化
# 8.1 列表推导式
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：用列表推导式把“遍历 + 变换 + 筛选”合并成一条表达式。

# ==================== 8.1.1 基本语法 ====================
# 基本形状是 [表达式 for 变量 in 可迭代对象]。
# 结果是一份新列表，原数据保持不变；每轮循环都用同一个变量名取值。
prices = [100, 250, 80]
final_prices = [price - price // 10 for price in prices]
print(final_prices)                   # -> [90, 225, 72]
# // C++: 对应 std::vector<int> result; 循环 transform 后 push_back。
# 表达式部分可以任意组合运算，也可以调用方法。
raw_names = [" li ", "wang ", " zhao"]
clean_names = [name.strip().title() for name in raw_names]
print(clean_names)                    # -> ['Li', 'Wang', 'Zhao']

# 遍历元组序列时配合解包，可以一次取出多个字段。
orders = [("A100", 3, 25), ("B201", 1, 40)]
amounts = [quantity * unit_price for _, quantity, unit_price in orders]
print(amounts)                        # -> [75, 40]
# // C++: 元组解包可用 std::tie(code, quantity, unit_price) = order;

# ==================== 8.1.2 条件过滤 ====================
# 过滤条件写在 for 之后：只有条件为真的元素才进入结果。
scores = [88, 45, 92, 61, 37, 75]
passed = [score for score in scores if score >= 60]
print(passed)                         # -> [88, 92, 61, 75]

# 条件表达式写在 for 之前：每个元素都要保留，但取值可以二选一。
labels = ["及格" if score >= 60 else "不及格" for score in scores]
print(labels)                         # -> ['及格', '不及格', '及格', '及格', '不及格', '及格']
# // C++: 条件表达式对应 score >= 60 ? "及格" : "不及格"。
# 两种 if 的位置含义完全不同，写错位置要么语法错误，要么结果颠倒。

# 过滤条件可以用组合判断，也可以写成区间比较的链式形式。
stock_items = [("A100", 12), ("B201", 0), ("C305", 25), ("D407", 4)]
low_stock = [code for code, quantity in stock_items if 0 < quantity < 20]
print(low_stock)                      # -> ['A100', 'D407']
# // C++: 链式比较需要写成 0 < quantity && quantity < 20。

# 清洗文本时常用“先变换、再按变换结果筛选”的写法。
titles = ["Python 入门", "", "   ", "C++ 基础"]
usable_titles = [title.strip() for title in titles if title.strip()]
print(usable_titles)                  # -> ['Python 入门', 'C++ 基础']

# ==================== 8.1.3 与普通循环写法对比 ====================
# 同一件事用普通循环写，需要先建空列表，再逐项 append。
numbers = [3, -2, 7, -5]
squared_loop = []
for number in numbers:
    squared_loop.append(number * number)
print(squared_loop)                   # -> [9, 4, 49, 25]

squared_comp = [number * number for number in numbers]
print(squared_comp)                   # -> [9, 4, 49, 25]

# 推导式拥有独立的局部作用域，循环变量不会覆盖外部同名变量。
number = 100
doubled = [number * 2 for number in range(3)]
print(doubled)                        # -> [0, 2, 4]
print(number)                         # -> 100
# // C++: 循环变量在 for 语句内部声明，离开作用域即失效；Python 的这一点要自己当心。

# 表达式较长或需要中间状态时，普通循环反而更清楚。
records = ["A100:12", "B201:0", "C305:25"]
codes = [record.split(":")[0] for record in records]
print(codes)                          # -> ['A100', 'B201', 'C305']
# 这里 split(":")[0] 已经不太好读，如果再叠加条件判断，就应改回显式循环。

# 性能：两者时间复杂度都是 O(n)。推导式在 CPython 中字节码更紧凑，
# 不需要每轮查找 append 方法，常数开销更小；数据量小时差异不明显。
# 因此选择依据首先是可读性，而不是无条件追求“一行写完”。
# // C++: 类似手写 for 循环与 std::transform 的差别，都是一次线性扫描。

# 练习题：把上面的 final_prices 改成“只保留价格大于 80 的商品”，
# 再分别用推导式和普通循环实现一次，对比两者的行数。

# 常见坑点：
# 1. 把条件表达式写成 [x for x in xs if f(x) else y]：语法错误，
#    必须写成 [y if f(x) else z for x in xs]，if 和 else 成对出现在 for 之前。
# 2. 在推导式里调用 print 或向外部列表 append：看起来能跑，但结果难读，
#    这类“有副作用的遍历”应改回显式 for 循环。
# 3. 误以为推导式变量会影响外部同名变量：推导式有独立作用域，
#    外面同名的 number 仍是原值，需要交换数据时显式赋值。
# 4. 需要 break、提前退出或复杂状态累积时硬写成推导式：推导式无法中途退出，
#    这类逻辑应保留普通循环。
# 5. 以为推导式一定比循环快很多：两者都是 O(n)，优势只是常数开销，
#    可读性下降时不要强行使用。
