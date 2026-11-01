# 第 9 章 列表与元组
# 9.3 列表方法详解
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：系统梳理列表增删查改相关的常用方法及其返回值。

# ==================== 9.3.1 append()、extend()、insert() ====================
# 三个方法都在原列表上修改，返回值都是 None。
cart = ["苹果", "牛奶"]
print(cart.append("面包"))            # -> None
print(cart)                           # -> ['苹果', '牛奶', '面包']

# extend 接收可迭代对象，元组和字符串都可以逐个展开加入。
cart.extend(("鸡蛋", "大米"))
print(cart)                           # -> ['苹果', '牛奶', '面包', '鸡蛋', '大米']
cart.insert(2, "酸奶")
print(cart)                           # -> ['苹果', '牛奶', '酸奶', '面包', '鸡蛋', '大米']
# // C++: 对应 push_back、insert(end, ...) 和 insert(begin() + i, ...)。
# Python 的方法名表意更直接，但位置参数是普通下标，不是迭代器。

# insert 的索引超出范围时会被夹到两端，不会报错。
items = ["A", "B"]
items.insert(10, "C")
print(items)                          # -> ['A', 'B', 'C']
items.insert(-10, "D")
print(items)                          # -> ['D', 'A', 'B', 'C']

# 注意：字符串也是可迭代对象，extend("ABC") 会逐字符加入。
letters = []
letters.extend("ABC")
print(letters)                        # -> ['A', 'B', 'C']
# 如果本意是加入整段文本，应写 letters.append("ABC")。
letters = []
letters.append("ABC")
print(letters)                        # -> ['ABC']

# ==================== 9.3.2 remove()、pop()、clear() ====================
# remove 按值删除，只删第一个匹配项；pop 按索引删除并返回被删元素。
cart = ["面包", "苹果", "牛奶", "面包", "鸡蛋"]
cart.remove("面包")
print(cart)                           # -> ['苹果', '牛奶', '面包', '鸡蛋']
removed = cart.pop(1)
print(removed)                        # -> 牛奶
print(cart)                           # -> ['苹果', '面包', '鸡蛋']
cart.clear()
print(cart)                           # -> []
# // C++: erase 需要迭代器；Python 的 remove 用值更直观，但要先确认值存在。

# pop 不传参数时删除末尾元素，适合把列表当作栈使用。
items = ["A", "B", "C"]
print(items.pop())                    # -> C
print(items.pop(0))                   # -> A
print(items)                          # -> ['B']
# // C++: 对应 pop_back() 与 erase(begin())，后者需要额外写迭代器。

# ==================== 9.3.3 count()、index()、reverse() ====================
# count 统计出现次数，找不到时返回 0。
cart = ["苹果", "牛奶", "苹果", "鸡蛋", "苹果"]
print(cart.count("苹果"))             # -> 3
print(cart.count("面包"))             # -> 0

# index 返回第一个匹配位置，可以指定查找起点；找不到会抛 ValueError。
print(cart.index("苹果"))             # -> 0
print(cart.index("苹果", 1))          # -> 2
print(cart.index("苹果", 3))          # -> 4
# // C++: std::find 返回迭代器，找不到返回 end()；Python 直接抛异常。

# reverse 原地反转，返回 None；reversed 返回迭代器，不修改原列表。
cart.reverse()
print(cart)                           # -> ['苹果', '鸡蛋', '苹果', '牛奶', '苹果']
ordered = list(reversed(cart))
print(ordered)                        # -> ['苹果', '牛奶', '苹果', '鸡蛋', '苹果']
# // C++: std::reverse(cart.begin(), cart.end()) 原地反转，语义与 reverse() 一致。

# 常见坑点：
# 1. 写 cart = cart.append("面包")：append 返回 None，
#    这样写会让 cart 变成 None，正确做法是单独调用，不要再赋值。
# 2. 用 extend("ABC") 想加入整段文本：字符串会被拆成单个字符，
#    需要整段加入时用 append。
# 3. 写 reversed_cart = cart.reverse()：reverse 原地修改并返回 None，
#    想要新列表应写 list(reversed(cart))。
# 4. 用 index 判断元素是否存在：找不到会抛 ValueError 而不是返回 -1，
#    判存在用 in，取次数用 count。
# 5. 对空列表调用 pop() 或传入越界索引：会抛 IndexError，
#    调用前先用 if cart: 判断列表是否非空。
