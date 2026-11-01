# 第 9 章 列表与元组
# 9.2 列表元素常用操作
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习添加、删除、修改、查找四类列表元素操作。

# ==================== 9.2.1 添加元素 ====================
# append 在末尾追加一个元素；extend 把另一个可迭代对象的元素逐个追加。
cart = ["苹果", "牛奶"]
cart.append("面包")
print(cart)                       # -> ['苹果', '牛奶', '面包']
cart.extend(["鸡蛋", "大米"])
print(cart)                       # -> ['苹果', '牛奶', '面包', '鸡蛋', '大米']
cart.insert(1, "酸奶")
print(cart)                       # -> ['苹果', '酸奶', '牛奶', '面包', '鸡蛋', '大米']
# // C++: push_back 对应 append；insert 需要传迭代器位置，如 cart.insert(cart.begin() + 1, x)。

# append 与 extend 的区别必须分清：追加列表时 append 会嵌套。
box = ["A"]
box.append(["B", "C"])
print(box)                        # -> ['A', ['B', 'C']]
box = ["A"]
box.extend(["B", "C"])
print(box)                        # -> ['A', 'B', 'C']

# 加号生成新列表，原列表不变；+= 在原列表上追加。
front = ["A100"]
rear = ["B201"]
merged = front + rear
print(merged)                     # -> ['A100', 'B201']
print(front)                      # -> ['A100']
left = ["A100"]
left += ["B201"]
print(left)                       # -> ['A100', 'B201']
# // C++: 向量相加需要自己循环或 std::copy，Python 的 + 直接拼接。
# 注意 += 修改原对象，若另有名字指向同一列表，也会看到变化。

# ==================== 9.2.2 删除元素 ====================
# remove 按值删除第一个匹配项；pop 按索引删除并返回被删元素。
orders = ["A100", "B201", "C305", "D407", "E508"]
orders.remove("C305")
print(orders)                     # -> ['A100', 'B201', 'D407', 'E508']
last = orders.pop()
print(last)                       # -> E508
print(orders)                     # -> ['A100', 'B201', 'D407']
first = orders.pop(0)
print(first)                      # -> A100
print(orders)                     # -> ['B201', 'D407']
# // C++: erase 与 remove 语义不同，C++ 的 remove 只是移动元素，
# 真正删除要配合 erase；Python 的 remove 直接删除。

# del 按下标删除，也可以删除一段切片；clear 清空整个列表。
del orders[0]
print(orders)                     # -> ['D407']
orders = ["A100", "B201", "C305", "D407"]
del orders[1:3]
print(orders)                     # -> ['A100', 'D407']
orders.clear()
print(orders)                     # -> []

# ==================== 9.2.3 修改元素 ====================
# 按下标赋值替换单个元素；切片赋值可以一次替换一段，长度可以不同。
scores = [60, 75, 80, 90]
scores[0] = 65
print(scores)                     # -> [65, 75, 80, 90]
scores[1:3] = [78, 85, 95]
print(scores)                     # -> [65, 78, 85, 95, 90]
scores[1:2] = [70, 72]
print(scores)                     # -> [65, 70, 72, 85, 95, 90]
# // C++: 对应 scores[0] = 65；批量替换需要 erase 后再 insert。

# 引用语义：切片是浅拷贝，只复制外层，内层列表仍被共享。
rows = [[1, 2], [3, 4]]
shallow = rows[:]
shallow[0][0] = 9
print(rows)                       # -> [[9, 2], [3, 4]]
print(shallow)                    # -> [[9, 2], [3, 4]]
# // C++: vector<vector<int>> 的复制默认是深拷贝；Python 需要明确深层复制。
# 需要每行独立时，可以写 rows = [[value for value in row] for row in rows]。

# ==================== 9.2.4 查找元素 ====================
# in 判断是否存在；index 返回值的位置；count 统计出现次数。
stock = ["A100", "B201", "C305", "B201"]
print("B201" in stock)            # -> True
print("Z999" in stock)            # -> False
print(stock.index("B201"))        # -> 1
print(stock.index("B201", 2))     # -> 3
print(stock.count("B201"))        # -> 2
# // C++: 查找用 std::find，判断存在要比较返回值与 end()，写法更啰嗦。

# 需要按条件查找时，用循环加 break，找到就停，语义最清楚。
prices = [("A100", 120), ("B201", 45), ("C305", 300)]
target_code = None
for code, price in prices:
    if price >= 200:
        target_code = code
        break
print(target_code)                # -> C305

# 也可以用 next() 配合生成器表达式取第一个匹配项，默认值写 None。
cheap_code = next((code for code, price in prices if price < 100), None)
print(cheap_code)                 # -> B201

# 常见坑点：
# 1. 用 append 添加一个列表，结果得到嵌套结构：append 只追加一个对象，
#    要展开元素请用 extend 或 +=。
# 2. remove 一个不存在的值会抛 ValueError，pop 索引越界会抛 IndexError，
#    删除前先用 in 判断或 len() 校验。
# 3. 在 for 循环中按值 remove 当前元素：后面的元素会整体前移导致漏处理，
#    应改为生成新列表或倒序遍历。
# 4. 用整数下标赋值来改变列表长度：scores[1] = [70, 72] 会把这个列表当成一个元素，
#    需要插入或替换一段时应使用切片赋值。
# 5. 以为 copy() 或 [:] 复制了所有层级：它们只是浅拷贝，
#    内层可变对象仍被两个列表共享，深层复制需要逐层重建。
