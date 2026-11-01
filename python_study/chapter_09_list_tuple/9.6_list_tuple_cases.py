# 第 9 章 列表与元组
# 9.6 列表与元组应用案例
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：用列表和元组完成成绩统计、购物车处理和批量数据整理。

# ==================== 9.6.1 成绩统计 ====================
# 用列表存放成绩，先统计总分和平均分，再统计及格率。
scores = [88, 76, 95, 61, 88, 54, 72]
total = sum(scores)
average = total / len(scores)
print(f"人数：{len(scores)}，总分：{total}，平均分：{average:.1f}")
print(f"最高分：{max(scores)}，最低分：{min(scores)}")
passed = [score for score in scores if score >= 60]
print(f"及格人数：{len(passed)}，及格率：{len(passed) / len(scores):.1%}")
# 输出：
# 人数：7，总分：534，平均分：76.3
# 最高分：95，最低分：54
# 及格人数：6，及格率：85.7%

# 分数段统计用字典保存计数，判断从高到低依次进行，避免区间重叠。
levels = {"优秀": 0, "良好": 0, "及格": 0, "不及格": 0}
for score in scores:
    if score >= 90:
        levels["优秀"] += 1
    elif score >= 80:
        levels["良好"] += 1
    elif score >= 60:
        levels["及格"] += 1
    else:
        levels["不及格"] += 1
print(levels)                         # -> {'优秀': 1, '良好': 2, '及格': 3, '不及格': 1}

# 排名用 sorted 生成新列表，保留原始顺序的 scores 以备后用。
ranked = sorted(scores, reverse=True)
print(ranked)                         # -> [95, 88, 88, 76, 72, 61, 54]
print(ranked[:3])                     # -> [95, 88, 88]
# // C++: 需要先 copy 一份 vector 再调用 std::sort，否则原数据会被打乱。

# ==================== 9.6.2 购物车数据处理 ====================
# 每个商品用元组 (名称, 数量, 单价) 表示，整辆购物车是元组列表。
cart = [("苹果", 3, 2.5), ("牛奶", 2, 4.0), ("面包", 1, 6.0)]
total = 0
for name, quantity, unit_price in cart:
    total += quantity * unit_price
print(f"种类：{len(cart)}，合计：{total:.2f} 元")
print(max(cart, key=lambda item: item[2]))
# 输出：
# 种类：3，合计：21.50 元
# ('面包', 1, 6.0)

# 修改数量、删除下架商品、追加新商品，这些都要求购物车是可变的列表。
cart[0] = ("苹果", 5, 2.5)
cart.remove(("面包", 1, 6.0))
cart.append(("鸡蛋", 1, 9.9))
print(cart)                           # -> [('苹果', 5, 2.5), ('牛奶', 2, 4.0), ('鸡蛋', 1, 9.9)]

# 重新计算合计时不要复用旧值，循环重置比增量更新更不容易出错。
total = 0
for name, quantity, unit_price in cart:
    total += quantity * unit_price
print(f"调整后合计：{total:.2f} 元")   # -> 调整后合计：30.40 元

# 逐项打印小计：解包比下标访问更能说明每个字段的含义。
for name, quantity, unit_price in cart:
    print(f"{name}：{quantity} 件，小计 {quantity * unit_price:.2f} 元")
# 输出：
# 苹果：5 件，小计 12.50 元
# 牛奶：2 件，小计 8.00 元
# 鸡蛋：1 件，小计 9.90 元

# ==================== 9.6.3 批量信息整理 ====================
# 原始文本按逗号分隔，逐条解析成 (编码, 库存, 单价) 元组。
raw_lines = ["A100,12,3.5", "B201,0,9.0", "C305,25,2.0", "D407,5,7.5"]
records = []
for line in raw_lines:
    code, quantity_text, price_text = line.split(",")
    records.append((code, int(quantity_text), float(price_text)))
print(records)
# 输出：
# [('A100', 12, 3.5), ('B201', 0, 9.0), ('C305', 25, 2.0), ('D407', 5, 7.5)]

# 按库存从高到低排序，库存为 0 的商品排在最后。
sorted_records = sorted(records, key=lambda item: item[1], reverse=True)
print(sorted_records)
# 输出：
# [('C305', 25, 2.0), ('A100', 12, 3.5), ('D407', 5, 7.5), ('B201', 0, 9.0)]

# 用固定列宽输出报表，元组解包让字段含义一目了然。
print(f"{'编码':<8}{'库存':>6}{'单价':>8}")
for code, quantity, price in sorted_records:
    print(f"{code:<8}{quantity:>6}{price:>8.1f}")
# 输出：
# 编码          库存      单价
# C305        25     2.0
# A100        12     3.5
# D407         5     7.5
# B201         0     9.0

# 只保留有库存的商品，并统计库存总数与平均单价。
in_stock = [record for record in sorted_records if record[1] > 0]
print(len(in_stock))                  # -> 3
print(sum(record[1] for record in in_stock))       # -> 42
print(round(sum(record[2] for record in in_stock) / len(in_stock), 2))  # -> 4.33
# // C++: 需要手写循环累加，Python 可以直接用生成器表达式配合聚合函数。

# 常见坑点：
# 1. 在遍历购物车的同时删除元素：下标会前移导致漏项，
#    需要批量删除时应先构造保留列表，或倒序遍历。
# 2. 平均分直接写 total / len(scores)：成绩列表为空时 len 为 0，
#    会抛 ZeroDivisionError，统计前先判断列表是否非空。
# 3. 用浮点数直接比较金额是否相等：0.1 + 0.2 并不等于 0.3，
#    金额比较或四舍五入应统一用 round()，必要时用 decimal。
# 4. 修改购物车时用 remove 按整个元组匹配：数量或单价稍有不一致就删不掉，
#    更稳妥的做法是按商品编码查找再删除。
# 5. 用 item[1]、item[2] 取字段却不写含义：字段一多就难以维护，
#    遍历时直接解包成有意义的变量名。
