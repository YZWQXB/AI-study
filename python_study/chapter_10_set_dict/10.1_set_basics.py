# 第 10 章 集合与字典
# 10.1 集合基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习集合的定义、去重、成员判断与并集、交集、差集运算。

# ==================== 10.1.1 集合的定义与特点 ====================
# 集合用花括号写元素，元素不重复、不按位置排列，只保留“有哪些值”。
# 元素必须是可哈希的不可变值：数字、字符串、元组可以，列表和字典不可以。
stock_codes = {"A01", "A02", "A03", "A01"}
print(len(stock_codes))                     # -> 3
print("A02" in stock_codes)                 # -> True
print("A04" in stock_codes)                 # -> False
print(sorted(stock_codes))                  # -> ['A01', 'A02', 'A03']
empty_set = set()
print(len(empty_set))                       # -> 0
# // C++: std::unordered_set 是哈希容器，元素不重复、不保证顺序；
# // C++: std::set 是红黑树，元素有序，查找 O(log n)；Python 的 set 平均 O(1)。

# ==================== 10.1.2 去重与成员判断 ====================
# 把列表交给 set() 即可去掉重复值；需要保留原顺序时不能直接用集合。
raw_tags = ["新人", "促销", "新人", "清仓", "促销"]
unique_tags = set(raw_tags)
print(len(unique_tags))                     # -> 3
print(sorted(unique_tags))                  # -> ['促销', '新人', '清仓']
# 判断“在不在”用 in：集合平均 O(1)，列表要从头逐个比较，平均 O(n)。
allowed_users = {"u1001", "u1002", "u1003"}
print("u1002" in allowed_users)             # -> True
print("u1004" in allowed_users)             # -> False
print("u1003" in ["u1001", "u1002", "u1003"])   # -> True
# // C++: unordered_set 用 find() 判断存在并拿到迭代器，找不到返回 end()。
# 只做存在性判断时优先集合；需要下标、排序或重复值时仍然用列表。

# ==================== 10.1.3 并集、交集、差集 ====================
# | 并集（两边全部），& 交集（两边都有），- 差集（左边独有），^ 对称差集。
python_group = {"张明", "李雷", "王芳"}
data_group = {"李雷", "王芳", "赵强"}
print(len(python_group | data_group))       # -> 4
print(sorted(python_group & data_group))    # -> ['李雷', '王芳']
print(sorted(python_group - data_group))    # -> ['张明']
print(sorted(python_group ^ data_group))    # -> ['张明', '赵强']
# 同名方法 union()、intersection()、difference()、symmetric_difference() 效果相同。
group_copy = set(python_group)
group_copy |= {"赵强"}
print(len(group_copy))                      # -> 4
print(len(python_group))                    # -> 3，|= 只修改副本
# // C++: 集合运算借助 std::set_union、std::set_intersection 等算法；
# // 运算对象必须是 set 或 frozenset，列表不能直接参与 &、|。

# frozenset 是不可变集合，创建后不能增删，因此可哈希，能作为字典键或集合元素。
region_key = frozenset({"华东", "华南"})
freight_rule = {region_key: 0.9}
print(freight_rule[region_key])             # -> 0.9
print(len(frozenset({"华东", "华南", "华东"})))  # -> 2
# // C++: 类似 const std::unordered_set，但 C++ 容器通常不能直接用作 map 的键。

# 常见坑点：
# 1. set("abc") 得到 {'a', 'b', 'c'}。原因：字符串被当成可迭代对象逐字符取。正确写法 set(["abc"])。
# 2. 写 empty = {} 得到的是空字典。原因：花括号默认构造字典。空集合只能写 set()。
# 3. 把列表放进集合会抛 TypeError: unhashable type: 'list'。原因：list 可变、不可哈希。正确做法是转成 tuple 或 frozenset。
# 4. 集合无序，不能写 s[0] 或切片。原因：哈希表只保存值，不保存位置。需要固定输出顺序时用 sorted(s)。
# 5. 差集方向易写反：a - b 保留的是 a 中有而 b 中没有的元素。原因：差集按左操作数单向计算。判断包含关系用 <= 或 issubset()。
