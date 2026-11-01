# 第 8 章 推导式与基础表达式优化
# 8.3 生成器表达式
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：用圆括号表达式实现按需计算，并观察惰性求值的效果。

# ==================== 8.3.1 生成器表达式认知 ====================
# 把列表推导式的方括号换成圆括号，就得到生成器表达式。
# 它不会一次性产生整份列表，而是按需逐个给出元素。
numbers = [12, 5, 30, 8]
squares = (number * number for number in numbers)
print(type(squares))                  # -> <class 'generator'>
print(next(squares))                  # -> 144
print(next(squares))                  # -> 25
print(list(squares))                  # -> [900, 64]
# // C++: 类似按需生成元素的迭代器，而不是先填满一个 vector。
# 注意不要直接 print 生成器对象本身，输出里会带内存地址，无法复现。

# 生成器表达式同样支持条件过滤和二选一表达式。
scores = [88, 45, 92, 61, 37]
pass_count = sum(1 for score in scores if score >= 60)
print(pass_count)                     # -> 3
# 这里用 sum(1 for ...) 统计数量，避免为了计数先建一份完整列表。

# 直接把生成器交给 max()、min()、sum() 等聚合函数，是最常见的用法。
amounts = [120, 340, 90, 45]
total = sum(amount for amount in amounts)
print(total)                          # -> 595
highest = max(amount * 2 for amount in amounts)
print(highest)                        # -> 680

# ==================== 8.3.2 与列表推导式的区别 ====================
# 列表推导式立刻计算全部结果，内存中保存完整列表。
list_form = [amount * 2 for amount in amounts]
print(list_form)                      # -> [240, 680, 180, 90]
print(len(list_form))                 # -> 4

# 生成器表达式只保存计算规则，元素在取值时才产生。
gen_form = (amount * 2 for amount in amounts)
print(len(list(gen_form)))            # -> 4
# 生成器没有 len()，也不能下标访问或切片；需要这些能力时必须用列表。

# 生成器是一次性迭代器：消费完就为空，不能回头重读。
double_gen = (value * 2 for value in [1, 2, 3])
print(list(double_gen))               # -> [2, 4, 6]
print(list(double_gen))               # -> []
# // C++: 自己实现的输入迭代器同样只能前进，读取过的元素不会自动回到开头。

# 选择原则：需要反复使用、需要长度或切片时用列表推导式；
# 只是一次性聚合（求和、求最大值、逐批处理）时用生成器表达式。

# ==================== 8.3.3 惰性求值初步 ====================
# 惰性求值指“写出表达式时不计算，取值时才读取当时的数据”。
source = [1, 2, 3]
lazy = (value * 2 for value in source)
print("生成器已创建，此时还没有读取任何元素")  # -> 生成器已创建，此时还没有读取任何元素
source.append(4)
print(next(lazy))                     # -> 2
print(list(lazy))                     # -> [4, 6, 8]
# 创建之后才追加的 4 也被计算进来，说明元素是在取值那一刻才读取的。
# // C++: 类似惰性迭代器在解引用时才访问容器，容器变化会影响后续结果。

# 惰性还能应对“无法一次性装入内存”的数据：无限序列也能按需取前几项。
from itertools import batched, count, islice
infinite = (number * number for number in count(1))
print(list(islice(infinite, 5)))      # -> [1, 4, 9, 16, 25]

# itertools.batched 可以把惰性数据流按固定大小分批，不必先收集全部元素。
rows = [f"订单{index:02d}" for index in range(1, 8)]
print(rows)                           # -> ['订单01', '订单02', '订单03', '订单04', '订单05', '订单06', '订单07']
for batch in batched(rows, 3):
    print(batch)
# 输出：
# ('订单01', '订单02', '订单03')
# ('订单04', '订单05', '订单06')
# ('订单07',)

# 用生成器表达式配合 batched，可以一边计算一边分批汇总。
stream = (amount * 2 for amount in [10, 20, 30, 40, 50])
for batch in batched(stream, 2):
    print(sum(batch))                 # -> 60
# 后续两条输出依次为：
# 140
# 100
# // C++: 需要手动维护缓冲区，凑够一批再处理，Python 由 batched 统一处理尾部。

# 常见坑点：
# 1. 生成器被消费后再次遍历得到空结果：它是单向迭代器，
#    需要重复使用时应改成列表推导式并保存结果。
# 2. 以为 (value for value in ...) 是元组：圆括号表达式是生成器，
#    单元素元组必须写 (value,)，否则只是普通括号。
# 3. 对生成器调用 len()、下标或切片：生成器不支持这些操作，
#    会抛出 TypeError，改为先 list() 再处理。
# 4. 直接 print 生成器对象做调试：输出会包含内存地址，每次运行都不同，
#    应打印 type() 或取出的元素。
# 5. 在生成器表达式里依赖外部可变数据：计算推迟到取值那一刻，
#    若期间外部列表已被修改，结果会与书写时预期不同。
