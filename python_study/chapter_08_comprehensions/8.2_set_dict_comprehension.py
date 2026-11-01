# 第 8 章 推导式与基础表达式优化
# 8.2 集合推导式与字典推导式
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：用花括号推导式完成去重与键值映射转换。

# ==================== 8.2.1 集合推导式 ====================
# 集合推导式的形状是 {表达式 for 变量 in 可迭代对象}，结果自动去重。
order_codes = ["A100", "A100", "B201", "C305", "B201"]
unique_codes = {code for code in order_codes}
print(len(unique_codes))              # -> 3
print(sorted(unique_codes))           # -> ['A100', 'B201', 'C305']
# 集合不保证顺序，且字符串哈希受哈希种子影响；需要可复现输出时先 sorted()。
# // C++: std::unordered_set 同样无序，遍历顺序不应写进程序逻辑。

# 集合推导式也可以带条件，只收集符合规则的项。
tags = ["electronics", "book", "ELECTRONICS", "food", "BOOK"]
normalized_tags = {tag.lower() for tag in tags}
print(sorted(normalized_tags))        # -> ['book', 'electronics', 'food']

# 从一组记录中提取“出现过的类别”，是集合推导式最典型的用法。
stock_items = [("A100", "电子", 12), ("B201", "图书", 0), ("C305", "电子", 25)]
categories = {category for _, category, _ in stock_items}
print(sorted(categories))             # -> ['图书', '电子']
# // C++: 对应把元素 insert 进 std::set 或 std::unordered_set。

# ==================== 8.2.2 字典推导式 ====================
# 字典推导式的形状是 {键表达式: 值表达式 for ...}，键值成对生成。
products = [("A100", 12), ("B201", 0), ("C305", 25)]
stock_map = {code: quantity for code, quantity in products}
print(stock_map)                      # -> {'A100': 12, 'B201': 0, 'C305': 25}

# 带过滤条件时，只留下符合条件的键值对。
available = {code: quantity for code, quantity in products if quantity > 0}
print(available)                      # -> {'A100': 12, 'C305': 25}

# 对值做统一变换，键保持不变。
score_map = {"语文": 88, "数学": 95, "英语": 76}
adjusted = {subject: score + 5 for subject, score in score_map.items()}
print(adjusted)                       # -> {'语文': 93, '数学': 100, '英语': 81}
# // C++: std::map 的遍历是按键排序，Python 字典按插入顺序遍历。

# 交换键和值时要注意：值必须唯一，重复值会让后面的项覆盖前面的项。
subject_by_score = {score: subject for subject, score in score_map.items()}
print(subject_by_score)               # -> {88: '语文', 95: '数学', 76: '英语'}
# 若把两个科目都改成 88，结果中只会留下后出现的那个科目。

# ==================== 8.2.3 简单数据转换场景 ====================
# 场景一：文本数字转成真正的整数，便于后续计算。
raw_scores = [("语文", "88"), ("数学", "95"), ("英语", "76")]
score_int = {subject: int(value) for subject, value in raw_scores}
print(score_int)                      # -> {'语文': 88, '数学': 95, '英语': 76}

# 场景二：一次性完成清洗与大小写统一。
raw_names = [" li ", "WANG", "zhao"]
name_map = {name.strip().lower(): name.strip().upper() for name in raw_names}
print(name_map)                       # -> {'li': 'LI', 'wang': 'WANG', 'zhao': 'ZHAO'}

# 场景三：把 "编码:数量" 文本拆成键值对，先拆分再转换，比压在一行更清楚。
records = ["A100:12", "B201:0", "C305:25"]
parts = [record.split(":") for record in records]
parsed = {code: int(value) for code, value in parts}
print(parsed)                         # -> {'A100': 12, 'B201': 0, 'C305': 25}

# 场景四：两个等长列表直接合成字典，用 strict=True 让长度不一致立刻报错。
codes = ["A100", "B201", "C305"]
quantities = [12, 0, 25]
stock_map = dict(zip(codes, quantities, strict=True))
print(stock_map)                      # -> {'A100': 12, 'B201': 0, 'C305': 25}
# // C++: 需要自己遍历两个容器并按相同下标组装 std::map。

# 常见坑点：
# 1. 直接 print 集合就当作固定输出：集合无序，字符串哈希每次运行都可能不同，
#    需要稳定输出时用 sorted() 或只输出 len()。
# 2. 字典推导式遇到重复键时不会报错，而是后出现的覆盖先出现的，
#    做键值互换前先确认值唯一，否则会丢数据。
# 3. 混淆 {} 的含义：{} 是空字典，空集合必须写 set()，
#    花括号里只有元素没有冒号时才是集合。
# 4. 把列表或字典放进集合或当作字典键：它们不可哈希，会抛 TypeError，
#    应改用元组或字符串作为键。
# 5. 在字典推导式里对同一段文本反复解析：键表达式和值表达式各自执行，
#    容易写错且难维护，建议像 records 示例那样先拆分成中间变量。
