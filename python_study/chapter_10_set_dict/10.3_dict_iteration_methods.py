# 第 10 章 集合与字典
# 10.3 字典遍历与常用方法
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习 keys、values、items 视图，get、update、pop 方法及常见遍历模式。

# ==================== 10.3.1 keys()、values()、items() ====================
# items() 同时给出键和值，需要成对处理时优先用它，避免再按键查一次。
scores = {"D01": 88, "D02": 92, "D03": 76}
print(list(scores.keys()))                  # -> ['D01', 'D02', 'D03']
print(list(scores.values()))                # -> [88, 92, 76]
print(list(scores.items()))                 # -> [('D01', 88), ('D02', 92), ('D03', 76)]
# 三者返回视图而不是新列表：不复制数据，并跟随字典变化。
keys_view = scores.keys()
scores["D04"] = 95
print(len(keys_view))                       # -> 4
# // C++: 遍历 map 拿到的是 std::pair<const Key, Value>，first 是键，second 是值。
# // Python 视图支持 len() 和 in，但按下标取值要先 list()；迭代中不能改动字典大小。

# ==================== 10.3.2 get()、update()、pop() ====================
# get 在键缺失时返回 None 或指定默认值，不会抛异常。
print(scores.get("D05"))                    # -> None
print(scores.get("D05", 0))                 # -> 0
print(scores.get("D02", 0))                 # -> 92
# update 用另一个字典批量更新：已有键覆盖，新键添加。
scores.update({"D02": 95, "D05": 84})
print(scores)      # -> {'D01': 88, 'D02': 95, 'D03': 76, 'D04': 95, 'D05': 84}
# pop 删除并返回值；键不存在时必须给默认值，否则抛 KeyError。
removed = scores.pop("D05")
print(removed)                              # -> 84
print(scores.pop("D06", -1))                # -> -1
print(len(scores))                          # -> 4
# // C++: erase(key) 不返回被删值，需要先取出；C++20 起可用 contains() 判断键是否存在。
# popitem() 删除并返回最后插入的键值对，适合按栈顺序清理数据。

# ==================== 10.3.3 遍历字典的常见模式 ====================
# 模式一：按键值对累加统计。
class_scores = {"D01": 88, "D02": 92, "D03": 76, "D04": 95}
total = 0
for code, score in class_scores.items():
    total += score
print(total)                                # -> 351
print(f"{total / len(class_scores):.1f}")   # -> 87.8
# 模式二：按条件筛选并生成新字典。
passed = {}
for code, score in class_scores.items():
    if score >= 90:
        passed[code] = score
print(sorted(passed))                       # -> ['D02', 'D04']
# 模式三：遍历中记录最值，并列时保留先出现的那一条。
top_code = ""
top_score = -1
for code, score in class_scores.items():
    if score > top_score:
        top_code = code
        top_score = score
print(top_code, top_score)                  # -> D04 95
# // C++: range-for 遍历 map 同样可做累加与筛选，但键值需要 .first/.second 访问。

# 常见坑点：
# 1. 直接 for item in d 得到的是键而不是值。原因：字典的迭代协议默认给出键。要值用 d[item] 或 d.values()。
# 2. 遍历 items() 时新增或删除键会抛 RuntimeError: dictionary changed size during iteration。
#    原因：视图长度在迭代中被改变。正确做法是先 list(d.items()) 生成快照，或先记录待改键，循环结束后统一修改。
# 3. get 的默认值不会写入字典。原因：get 只返回值，不执行赋值。需要写入默认值并返回时用 setdefault。
# 4. items()、keys()、values() 是视图不是列表，不支持下标，也不能反复当列表切片使用。
#    原因：视图动态映射原字典，不复制数据。需要固定快照时先 list()。
# 5. pop 不带默认值且键不存在时会抛 KeyError。原因：pop 要求键存在才能返回被删值。popitem 只能按后进先出顺序删除，不能指定键。
