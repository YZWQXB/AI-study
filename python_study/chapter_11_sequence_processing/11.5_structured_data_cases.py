# 第 11 章 序列与基础数据处理
# 11.5 结构化数据处理案例
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：完成成绩单分析、文本词频统计和销售报表整理三个结构化数据案例。

from itertools import batched

# ==================== 11.5.1 成绩单分析 ====================
# 成绩单是“列表套字典”，分析流程固定为：遍历汇总、找最值、算比率、分档统计。
records = [
    {"id": "S01", "name": "张明", "score": 88},
    {"id": "S02", "name": "李雷", "score": 92},
    {"id": "S03", "name": "王芳", "score": 58},
    {"id": "S04", "name": "赵强", "score": 95},
]
total = 0
for record in records:
    total += record["score"]
average = total / len(records)
print(f"平均分：{average:.2f}")              # -> 平均分：83.25
# 找最高分记录：遍历时同步保存整条记录，而不是只存分数。
top_record = records[0]
for record in records:
    if record["score"] > top_record["score"]:
        top_record = record
print(f"最高分：{top_record['name']} {top_record['score']}")   # -> 最高分：赵强 95
# 及格率：统计满足条件的条数，再除以总条数。
passed_count = 0
for record in records:
    if record["score"] >= 60:
        passed_count += 1
print(f"及格率：{passed_count / len(records):.1%}")   # -> 及格率：75.0%
# 分档统计：先建好带默认值的字典，再按阈值累加人数。
bands = {"优秀": 0, "及格": 0, "不及格": 0}
for record in records:
    score = record["score"]
    if score >= 90:
        bands["优秀"] += 1
    elif score >= 60:
        bands["及格"] += 1
    else:
        bands["不及格"] += 1
print(bands)        # -> {'优秀': 2, '及格': 1, '不及格': 1}
# // C++: 结构体数组配合 range-for 也能完成，分档字典对应 map<string, int>。

# ==================== 11.5.2 文本词频入门 ====================
# 词频统计三步：统一大小写、去掉标点、按空格切分后计数。
text = "Python is easy. Python is powerful. Data analysis uses Python."
normalized = text.lower().replace(".", "")
words = normalized.split()
print(len(words))                           # -> 10
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)       # -> {'python': 3, 'is': 2, 'easy': 1, 'powerful': 1, 'data': 1, 'analysis': 1, 'uses': 1}
print(len(counts))                          # -> 7
# 排序输出高频词：把 (次数, 单词) 元组排序，次数相同时再按单词比较。
pairs = []
for word, count in counts.items():
    pairs.append((count, word))
ranked = sorted(pairs, reverse=True)
print(ranked[:2])                           # -> [(3, 'python'), (2, 'is')]
# // C++: map<string, int> 统计后转 vector<pair<int, string>> 再 sort，思路完全相同。
# 实际项目可用 collections.Counter 简化计数，但统计原理仍是哈希表中的 get 累加。

# ==================== 11.5.3 简单报表整理 ====================
# 原始销售流水是 (区域, 商品, 金额) 元组列表，报表按区域汇总金额。
sales = [
    ("华东", "P01", 1200),
    ("华南", "P02", 3400),
    ("华东", "P02", 2600),
    ("华北", "P01", 1800),
]
region_totals = {}
sku_totals = {}
for region, sku, amount in sales:
    region_totals[region] = region_totals.get(region, 0) + amount
    sku_totals[sku] = sku_totals.get(sku, 0) + amount
print(region_totals)    # -> {'华东': 3800, '华南': 3400, '华北': 1800}
print(sku_totals)       # -> {'P01': 3000, 'P02': 6000}
# 输出报表：逐行格式化，金额统一右对齐，最后给出总计。
print("区域 | 销售额")                      # -> 区域 | 销售额
for region, amount in region_totals.items():
    print(region, "|", amount)              # -> 见下方三行报表
# -> 区域 | 销售额
# -> 华东 | 3800
# -> 华南 | 3400
# -> 华北 | 1800
print(f"总计：{sum(region_totals.values())}")   # -> 总计：9000
# 分批处理长流水：itertools.batched 按固定大小切分，适合分页展示或分批写库。
print("分页明细")                          # -> 分页明细
for page_no, page in enumerate(batched(sales, 2), start=1):
    print("第", page_no, "页")              # -> 见下方分页输出
    for region, sku, amount in page:
        print(region, sku, amount)          # -> 见下方明细行
# -> 分页明细
# -> 第 1 页
# -> 华东 P01 1200
# -> 华南 P02 3400
# -> 第 2 页
# -> 华东 P02 2600
# -> 华北 P01 1800
# // C++: 分页通常按迭代器区间切片；Python 3.12 的 batched 直接产出固定大小的元组。
# 最后一批可能不足 size 个元素，统计时要按实际长度处理。

# 常见坑点：
# 1. 统计词频前不统一大小写和标点，Python 与 python、easy 与 easy. 会被算成不同的词。
#    原因：比较的是完整字符串。正确做法是先 lower()，再替换标点。
# 2. split() 会合并连续空白，split(" ") 会保留空字符串。原因：无参数 split 按任意空白切分。
#    清洗文本通常用无参数的 split()。
# 3. 排序时只按次数排，并列顺序依赖次要键。原因：元组排序会比较后一个元素。
#    正式报表要明确并列规则，避免结果不可解释。
# 4. 金额用 float 累加存在精度误差。原因：二进制浮点无法精确表示部分小数。展示可格式化，财务结算应用整数分或 Decimal。
# 5. batched 的最后一批可能不足指定大小。原因：元素总数不一定整除批大小。按批处理时不能假设每批长度都相同。
