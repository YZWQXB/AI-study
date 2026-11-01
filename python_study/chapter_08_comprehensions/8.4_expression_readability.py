# 第 8 章 推导式与基础表达式优化
# 8.4 表达式可读性优化
# 学习优先级：P1（重点掌握） | 掌握要求：会用
# 本文件：判断推导式该写到什么程度，以及什么时候改回显式循环。

# ==================== 8.4.1 扁平化逻辑 ====================
# 二维数据压平成一维时，多个 for 按“从外到内”书写，与嵌套循环顺序一致。
matrix = [[1, 2, 3], [4, 5, 6]]
flat = [value for row in matrix for value in row]
print(flat)                           # -> [1, 2, 3, 4, 5, 6]
# 读法：先取每一行，再取行里的每个元素；条件可加在最后。
# // C++: 对应两层嵌套 for，外层遍历行，内层遍历行内元素。

# 组合生成也能用同样结构：外层先枚举，内层再枚举，结果是笛卡尔积。
pairs = [(code, size) for code in ["A100", "B201"] for size in ["S", "M"]]
print(pairs)                          # -> [('A100', 'S'), ('A100', 'M'), ('B201', 'S'), ('B201', 'M')]
# 若把两个 for 顺序写反，组合顺序会整体改变，但数据量相同。

# ==================== 8.4.2 避免过度嵌套 ====================
# 下面这行同时包含两层遍历、条件筛选和数值变换，已经很难一眼读懂。
groups = [("一组", [88, 72]), ("二组", [95, 90])]
hard = [value + 5 for _, group_scores in groups for value in group_scores if value >= 80]
print(hard)                           # -> [93, 100, 95]
# 先筛出高分，再做加分，两步分开写，意图更清楚。
high_scores = [value for _, group_scores in groups for value in group_scores if value >= 80]
adjusted = [value + 5 for value in high_scores]
print(adjusted)                       # -> [93, 100, 95]
# // C++: 分成两个容器或两次遍历同样更易读，编译器优化通常能消除额外开销。

# 判断标准：推导式里出现两个以上 for、或同时出现 if 与 if-else 时，
# 就应该拆成多步，或者直接写显式循环。

# 同样一件事，用循环写出来时每一步都有名字，出错时也容易定位。
adjusted_loop = []
for _, group_scores in groups:
    for value in group_scores:
        if value >= 80:
            adjusted_loop.append(value + 5)
print(adjusted_loop)                  # -> [93, 100, 95]

# ==================== 8.4.3 何时使用显式循环 ====================
# 情况一：需要提前结束。推导式无法 break，只能遍历完全部元素。
orders = [("A100", 0), ("B201", 5), ("C305", 18)]
first_out_of_stock = None
for code, quantity in orders:
    if quantity == 0:
        first_out_of_stock = code
        break
print(first_out_of_stock)             # -> A100
# // C++: 找到目标后 break 跳出，Python 在这里用循环写法表达最直接。

# 情况二：需要副作用，例如逐条打印报表。
for index, (code, quantity) in enumerate(orders, start=1):
    print(f"第 {index} 条：{code}，库存 {quantity}")
# 输出：
# 第 1 条：A100，库存 0
# 第 2 条：B201，库存 5
# 第 3 条：C305，库存 18

# 情况三：需要累积多个结果或维护复杂状态。
total_quantity = 0
available_count = 0
for _, quantity in orders:
    total_quantity += quantity
    if quantity > 0:
        available_count += 1
print(total_quantity)                 # -> 23
print(available_count)                # -> 2

# 情况四：每轮可能失败，需要单条处理错误。推导式里一条出错会整体中断。
raw_values = ["12", "abc", "0", "25"]
valid_total = 0
for text in raw_values:
    if not text.isdigit():
        print("跳过非法数据：", text)
        continue
    valid_total += int(text)
print(valid_total)                    # -> 37
# 输出：
# 跳过非法数据： abc

# 结论：推导式适合“把一批数据映射成另一批数据”，
# 循环适合“有顺序、有状态、有中断、有副作用的流程”。

# 常见坑点：
# 1. 扁平化时把两个 for 的顺序写反：外层 for 必须写在前面，
#    顺序颠倒会让结果的分组含义改变。
# 2. 为了追求一行写法堆叠多层 for 与条件：维护成本高，
#    超过两层遍历就应拆成中间变量或显式循环。
# 3. 需要 break 或提前退出的场景用推导式：它必须遍历全部元素，
#    既浪费性能又表达不了“找到即停止”。
# 4. 在推导式内部调用 print 或写文件：副作用与“生成列表”混在一起，
#    应改成显式循环，让数据处理和输出各归其位。
# 5. 用推导式批量解析可能出错的数据：一条异常会让整个表达式失败，
#    逐条处理错误时应使用循环加判断。
