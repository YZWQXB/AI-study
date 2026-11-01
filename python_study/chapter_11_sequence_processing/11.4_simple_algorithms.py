# 第 11 章 序列与基础数据处理
# 11.4 简单算法训练
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：手动实现最值、平均值、次数统计以及排名与分组的常见算法。

# ==================== 11.4.1 最大值、最小值与平均值 ====================
# 最值算法：先假设第一个元素是最大/最小，再逐个比较；并列时保留先出现的。
scores = [88, 92, 76, 95, 92]
max_score = scores[0]
min_score = scores[0]
for score in scores[1:]:
    if score > max_score:
        max_score = score
    if score < min_score:
        min_score = score
print(max_score, min_score)                 # -> 95 76
print(max(scores), min(scores))             # -> 95 76
# 平均值要先过滤缺失值（None），否则加法会抛 TypeError。
raw_scores: list[int | None] = [88, None, 92, 76]
total = 0
valid_count = 0
for score in raw_scores:
    if score is None:
        continue
    total += score
    valid_count += 1
print(valid_count)                          # -> 3
print(f"{total / valid_count:.2f}")         # -> 85.33
# // C++: 可用 std::numeric_limits<int>::min() 作初值；Python 直接用第一个元素更安全。
# 若用 0 初始化最大值，遇到全负数的数据就会得到错误结果。

# ==================== 11.4.2 次数统计 ====================
# 用字典累计次数：键是元素，值是出现次数，一次遍历为 O(n)。
words = ["python", "data", "python", "ai", "python", "data"]
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)       # -> {'python': 3, 'data': 2, 'ai': 1}
# 需要排序时，把 (次数, 元素) 元组放进列表再 sorted；reverse=True 得到次数从高到低。
pairs = []
for word, count in counts.items():
    pairs.append((count, word))
ranked = sorted(pairs, reverse=True)
print(ranked)       # -> [(3, 'python'), (2, 'data'), (1, 'ai')]
print(ranked[0][1])                         # -> python
# // C++: 对应 map<string, int> 计数，再转成 vector<pair<int, string>> 排序。
# 标准库 collections.Counter 可以一行完成计数，后续章节会接触，这里先用字典理解原理。

# ==================== 11.4.3 排名与分组基础 ====================
# 名次算法：名次 = 1 + 分数比自己高的人数；并列时两名次相同，下一名会跳号。
class_scores = {"张明": 88, "李雷": 92, "王芳": 76, "赵强": 92}
for name, score in class_scores.items():
    rank = 1
    for other_score in class_scores.values():
        if other_score > score:
            rank += 1
    print(f"{name}: {score} 分，第 {rank} 名")    # -> 见下方四行输出
# -> 张明: 88 分，第 3 名
# -> 李雷: 92 分，第 1 名
# -> 王芳: 76 分，第 4 名
# -> 赵强: 92 分，第 1 名
# 分组：按分数段把学生归入不同档位，先用 setdefault 建空列表再 append。
scores = [88, 92, 76, 95, 63, 58]
bands = {"优秀": [], "及格": [], "不及格": []}
for score in scores:
    if score >= 90:
        bands["优秀"].append(score)
    elif score >= 60:
        bands["及格"].append(score)
    else:
        bands["不及格"].append(score)
print(bands)        # -> {'优秀': [92, 95], '及格': [88, 76, 63], '不及格': [58]}
for band, values in bands.items():
    print(band, len(values))                    # -> 见下方三行输出
# -> 优秀 2
# -> 及格 3
# -> 不及格 1
# // C++: 分组对应 map<string, vector<int>>；阈值判断用 if / else if 链。

# 常见坑点：
# 1. 用 max_score = 0 初始化，全负数或全 0 的数据会得到错误结果。原因：0 不是数据中的元素。用第一个元素初始化。
# 2. 平均值计算前不检查数据量，空列表或全为 None 时会除零。原因：有效数据个数可能为 0。先确认 valid_count > 0。
# 3. 排名用 > 比较时并列同分共享名次，下一名跳号（1、1、3）。原因：名次按“分数更高的人数”计算。
#    需要密集排名（1、1、2）要单独处理。
# 4. 对每个元素都调用 list.count() 统计次数是 O(n^2)。原因：每次 count 都要完整扫描一遍列表。用字典一次遍历即可。
# 5. 分组时直接写 bands[band].append(value)，键不存在会抛 KeyError。原因：字典没有自动建列表。应先用 setdefault 初始化。
