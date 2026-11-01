# 第 10 章 集合与字典
# 10.4 嵌套数据结构
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习列表中嵌套字典、字典中嵌套列表以及多层数据的安全访问。

# ==================== 10.4.1 列表中嵌套字典 ====================
# 多条同类记录常用“列表套字典”：列表负责顺序，字典负责带名字的字段。
students = [
    {"id": "S01", "name": "张明", "score": 88},
    {"id": "S02", "name": "李雷", "score": 92},
    {"id": "S03", "name": "王芳", "score": 76},
]
for student in students:
    print(student["id"], student["name"], student["score"])   # -> 见下方三行输出
# -> S01 张明 88
# -> S02 李雷 92
# -> S03 王芳 76
print(students[1]["name"])                  # -> 李雷
# 字段可能缺失时用 get；用 [] 取不存在的字段会抛 KeyError。
print(students[0].get("phone", "未登记"))    # -> 未登记
students[0]["score"] = 90                   # 修改某条记录
students[2]["phone"] = "13800000000"        # 给单条记录追加字段
print(students[2])   # -> {'id': 'S03', 'name': '王芳', 'score': 76, 'phone': '13800000000'}
# // C++: 通常定义 struct Student 保证字段固定；用 map<string, variant> 则字段名无类型检查。
# // Python 的字典允许各条记录字段不同，但这会降低可读性，报表类数据应保持字段一致。

# ==================== 10.4.2 字典中嵌套列表 ====================
# 按分类聚合时常见“字典套列表”：键是分类，值是该分类下的成员列表。
classroom = {"一班": ["张明", "李雷"], "二班": ["王芳", "赵强", "孙悦"]}
print(classroom["一班"][0])                 # -> 张明
print(len(classroom["二班"]))               # -> 3
# setdefault 在键缺失时写入一个空列表并返回它，因此可以直接接着 append。
classroom.setdefault("三班", []).append("周涛")
print(classroom["三班"])                    # -> ['周涛']
print(len(classroom))                       # -> 3
# 把平铺记录按字段分组，是报表与统计中最常见的聚合写法。
records = [("一班", "张明"), ("二班", "王芳"), ("一班", "李雷")]
grouped = {}
for class_name, student_name in records:
    grouped.setdefault(class_name, []).append(student_name)
print(grouped)      # -> {'一班': ['张明', '李雷'], '二班': ['王芳']}
# // C++: 对应 map<string, vector<string>>，插入前要判断键是否存在再 push_back。

# ==================== 10.4.3 多层数据访问 ====================
# 真实单据通常三层以上：订单字典里放客户字典和明细列表。
order = {
    "order_id": "A2024",
    "customer": {"name": "张明", "level": "金卡"},
    "items": [
        {"sku": "P01", "qty": 2, "price": 3.5},
        {"sku": "P02", "qty": 1, "price": 12.0},
    ],
}
print(order["customer"]["name"])            # -> 张明
print(order["items"][1]["sku"])             # -> P02
total = 0
for item in order["items"]:
    total += item["qty"] * item["price"]
print(f"{total:.2f}")                       # -> 19.00
# 不确定的层级用 get 兜底，确定存在的层级才用 []。
print(order["customer"].get("province", "未填写"))   # -> 未填写
coupon = order.get("coupon")
if coupon is None:
    print("未使用优惠券")                    # -> 未使用优惠券
# // C++: 多层嵌套访问同样要逐层判空；C++17 可用 std::optional 表示“可能没有值”。

# 常见坑点：
# 1. 多层下标中任意一层缺失都会报错：列表越界抛 IndexError，字典缺键抛 KeyError。
#    原因：每层都要先成功取值才能继续。正确做法是逐层判断，或对不确定的层使用 get。
# 2. get 只保护它所在的那一层，order["customer"].get("address")["city"] 仍可能报错。
#    原因：第二层下标没有兜底。要逐层判断。
# 3. 直接赋值 second = students[0] 只是起别名；用 .copy() 是浅拷贝，嵌套列表/字典仍共享。
#    需要完全独立时用 copy.deepcopy()，否则改副本会改到原数据。
# 4. 把同一个字典对象 append 进多个位置，修改一处会全部变化。原因：多个位置保存的是同一个对象引用。每次应新建字典。
# 5. 嵌套结构直接 print 可读性差。原因：repr 会把所有层级挤在一行。报表输出应逐条格式化，避免把整块 repr 丢给用户。
