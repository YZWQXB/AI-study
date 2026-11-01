# 第 10 章 集合与字典
# 10.2 字典基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习字典的键值对结构、创建与访问、增改删以及 dict | 合并。

# ==================== 10.2.1 键值对结构 ====================
# 字典保存“键 -> 值”的映射，键唯一且必须可哈希，按 key 查找平均 O(1)。
# 3.7 起字典保留插入顺序，遍历顺序稳定，但它不是排序结果。
scores: dict[str, int] = {"D01": 88, "D02": 92, "D03": 76}
print(scores)                               # -> {'D01': 88, 'D02': 92, 'D03': 76}
print(len(scores))                          # -> 3
print(scores["D02"])                        # -> 92
# 键可以是字符串、数字或元组；值可以是任意对象，包括列表和另一个字典。
config = {"host": "127.0.0.1", "port": 8000, "debug": False}
print(config["port"])                       # -> 8000
positions = {(2, 3): "仓库 A 区", (5, 1): "仓库 B 区"}
print(positions[(2, 3)])                    # -> 仓库 A 区
# // C++: std::map 是红黑树，按键有序，查找 O(log n)；
# // std::unordered_map 是哈希表，平均 O(1) 但遍历顺序不确定。
# // Python 的 dict 是哈希表，同时额外保留插入顺序。

# ==================== 10.2.2 创建与访问 ====================
# 字面量最常用；dict() 还能从关键字参数或键值对序列创建。
price = {"apple": 3.5, "banana": 2.0}
print(price["apple"])                       # -> 3.5
keyword_price = dict(apple=3.5, banana=2.0)
print(keyword_price)                        # -> {'apple': 3.5, 'banana': 2.0}
print(list(keyword_price))                  # -> ['apple', 'banana']，遍历字典得到键
# 用 [] 访问不存在的键会抛 KeyError；先用 in 判断，或用 10.3 节的 get()。
if "orange" in price:
    print(price["orange"])                  # 该分支不会执行，price 中没有 orange 键
else:
    print("orange 未登记")                   # -> orange 未登记
# // C++: m[key] 在键不存在时会插入默认值；Python 的 d[key] 只读，不存在就报错。
# // 值类型混合时 C++ 需要 std::variant 或封装结构体，Python 字典可以随意混放。

# ==================== 10.2.3 新增、修改与删除 ====================
# 对键赋值时，键不存在就新增，键已存在就覆盖旧值。
scores["D04"] = 95          # 新增
scores["D01"] = 90          # 修改，位置保持不变
print(scores)               # -> {'D01': 90, 'D02': 92, 'D03': 76, 'D04': 95}
del scores["D03"]
print(scores)               # -> {'D01': 90, 'D02': 92, 'D04': 95}
# setdefault 在键不存在时写入默认值并返回它；键已存在时原值不变。
contact = {"name": "张明"}
contact.setdefault("phone", "未填写")
print(contact)              # -> {'name': '张明', 'phone': '未填写'}
print(contact.setdefault("name", "李雷"))   # -> 张明
# // C++: map::insert 在键已存在时不覆盖；Python 的 setdefault 语义相同。

# | 合并两个字典生成新字典，同名键以右边为准；|= 才原地修改左边。
base_price = {"apple": 3.5, "banana": 2.0}
holiday_price = {"banana": 1.8, "orange": 4.2}
merged = base_price | holiday_price
print(merged)               # -> {'apple': 3.5, 'banana': 1.8, 'orange': 4.2}
print(base_price)           # -> {'apple': 3.5, 'banana': 2.0}
base_price |= {"apple": 3.2}
print(base_price)           # -> {'apple': 3.2, 'banana': 2.0}
# // C++: 合并 map 通常循环 insert；C++17 的 merge() 只插入缺失键，不覆盖已有键。

# 常见坑点：
# 1. 用列表当键会抛 TypeError: unhashable type: 'list'。键必须可哈希，可用 tuple 替代。
# 2. d[key] 在键不存在时抛 KeyError，而不是返回 None。原因：dict 的 [] 只做读取，不提供默认值。不确定时用 in 或 get()。
# 3. d.get(key, []).append(x) 里的列表是临时对象，append 后不会写回字典。原因：get 只返回对象，不做赋值。应改用 setdefault。
# 4. 字典遍历顺序是插入顺序，不是按键或按值排序。原因：dict 只维护插入顺序，不维护排序。需要排序时用 sorted()。
# 5. a | b 生成新字典且不修改 a，原地合并要写 a |= b。原因：| 运算返回新对象。| 的操作数必须都是字典。
