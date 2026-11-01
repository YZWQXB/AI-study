# 第 10 章 集合与字典
# 10.6 综合应用案例
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：用字典与集合完成学生信息管理、通讯录管理和商品库存管理。

# ==================== 10.6.1 学生信息管理 ====================
# 用“学号 -> 学生字典”保存记录：按学号查询、修改、删除都是平均 O(1)。
students = {
    "S01": {"name": "张明", "score": 88},
    "S02": {"name": "李雷", "score": 92},
}
students["S03"] = {"name": "王芳", "score": 76}     # 新增记录
print(list(students))                               # -> ['S01', 'S02', 'S03']
students["S02"]["score"] = 95                       # 修改嵌套字段
print(students["S02"]["score"])                     # -> 95
removed = students.pop("S03")                       # 删除并保留被删记录
print(removed)                                      # -> {'name': '王芳', 'score': 76}
print(len(students))                                # -> 2
# 统计平均分：遍历 values() 取每条记录的分数字段。
total = 0
for record in students.values():
    total += record["score"]
print(f"{total / len(students):.1f}")               # -> 91.5
# 查询用 get：键不存在返回 None，避免 KeyError 中断程序。
query_id = "S04"
record = students.get(query_id)
if record is None:
    print("查无此人")                                # -> 查无此人
else:
    print(record["name"])                            # 查询命中时才会执行
# // C++: 等价于 unordered_map<string, Student>，查询前通常还要用 find() 判断是否存在。

# ==================== 10.6.2 通讯录管理 ====================
# 姓名作为键，电话和分组作为值；键唯一，同名联系人需要额外编号才能区分。
contacts = {
    "张明": {"phone": "13800000001", "group": "同事"},
    "李雷": {"phone": "13900000002", "group": "同学"},
}
print(contacts["张明"]["phone"])                    # -> 13800000001
contacts["王芳"] = {"phone": "13700000003", "group": "家人"}
contacts["李雷"]["phone"] = "13911112222"           # 修改电话
contacts.setdefault("赵强", {"phone": "未填写", "group": "未分组"})
print(len(contacts))                                # -> 4
print(contacts["赵强"])      # -> {'phone': '未填写', 'group': '未分组'}
# 按分组筛选：遍历 items() 拿到姓名和资料。
keyword = "同学"
matched = []
for name, info in contacts.items():
    if info["group"] == keyword:
        matched.append(name)
print(matched)                                      # -> ['李雷']
del contacts["赵强"]
print(len(contacts))                                # -> 3
# 按分组计数：get 提供初始 0，避免先判断键是否存在。
group_counts = {}
for info in contacts.values():
    group = info["group"]
    group_counts[group] = group_counts.get(group, 0) + 1
print(group_counts)     # -> {'同事': 1, '同学': 1, '家人': 1}
# // C++: map<string, Contact> 删除用 erase(iterator)，按键统计用 counts[group]++。

# ==================== 10.6.3 商品库存管理 ====================
# 库存表按键存放商品字典：名称、库存、单价。
inventory = {
    "P01": {"name": "笔记本", "stock": 12, "price": 3.5},
    "P02": {"name": "签字笔", "stock": 5, "price": 1.2},
    "P03": {"name": "文件夹", "stock": 0, "price": 9.0},
}
print(inventory["P01"]["stock"])                    # -> 12
# 出库要先判断商品是否存在、库存是否足够，再修改数据。
sku = "P02"
quantity = 3
if sku not in inventory:
    print("商品不存在")                              # 该分支不会执行，P02 存在
elif inventory[sku]["stock"] < quantity:
    print("库存不足")                                # 该分支不会执行，库存足够
else:
    inventory[sku]["stock"] -= quantity
    print(f"{inventory[sku]['name']} 剩余 {inventory[sku]['stock']}")   # -> 签字笔 剩余 2
# 入库：新商品整条写入，已有商品只增加库存字段。
inventory["P04"] = {"name": "便签纸", "stock": 20, "price": 2.0}
inventory["P01"]["stock"] += 8
print(inventory["P01"]["stock"])                    # -> 20
# 计算库存总值并提示低库存商品。
total_value = 0
for item in inventory.values():
    total_value += item["stock"] * item["price"]
print(f"库存总值：{total_value:.2f}")                # -> 库存总值：112.40
low_stock = []
for sku, item in inventory.items():
    if item["stock"] < 5:
        low_stock.append((sku, item["stock"], item["name"]))
print(low_stock)    # -> [('P02', 2, '签字笔'), ('P03', 0, '文件夹')]
# // C++: 库存结构可用 struct + map，金额建议用整数分或定点类型避免浮点误差。

# 常见坑点：
# 1. 出库不做检查直接减库存，会因键不存在抛 KeyError，或把库存减成负数。
#    原因：[] 读取和数值运算都不校验业务规则。正确做法是先判存在、再判库存是否足够。
# 2. inventory["P05"] = inventory["P01"] 只是同一个字典的别名，改一个两个都变。
#    原因：赋值复制的是对象引用。要新建字典或深拷贝。
# 3. 金额用 float 连续累加会出现 0.1 + 0.2 这类精度误差。原因：二进制浮点无法精确表示部分小数。
#    输出要格式化，财务计算用 Decimal 或整数分。
# 4. 删除用 pop 可以保留被删数据做回滚或日志。原因：pop 返回被删的值，del 不返回。del 删除后原记录无法恢复。
# 5. 嵌套修改必须逐层写全，inventory["P02"]["stock"] -= 1 才改到原字典。原因：少写一层时操作的是取出的临时值，不会写回原字典。
