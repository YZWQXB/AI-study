# 第 12 章 函数基础
# 12.3 参数与返回值
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习位置参数的传递顺序、返回值的设计方式，以及多返回值与元组解包。

# ==================== 12.3.1 位置参数 ====================
# 调用时实参按位置依次绑定到形参，顺序错误不会报错，但会算出错误结果。
def calc_shipping(weight: float, distance: int) -> float:
    return round(weight * 2.5 + distance * 0.8, 2)

print(calc_shipping(3.0, 120))       # -> 103.5
print(calc_shipping(120, 3.0))       # -> 302.4，参数顺序错误导致成本被放大
# // C++: double calcShipping(double weight, int distance); 同样按位置匹配，顺序写反也会算错。

# 实参个数必须与形参一致，缺少或多出都会抛出 TypeError。
# print(calc_shipping(3.0))          # TypeError: missing 1 required positional argument
# print(calc_shipping(3.0, 120, 5))  # TypeError: takes 2 positional arguments but 3 were given

# 形参名只在函数内部使用，调用者传入的是位置上的值，传入变量的名字不影响结果。
package_weight = 2.0
transport_distance = 80
print(calc_shipping(package_weight, transport_distance))    # -> 69.0

# Python 的参数按对象引用传递：引用本身按值复制，可变对象被原地修改会影响调用者。
def add_label(labels: list[str], label: str) -> None:
    labels.append(label)

order_labels = ["加急"]
add_label(order_labels, "易碎")
print(order_labels)                  # -> ['加急', '易碎']
# // C++: 想修改原对象需要 std::vector<std::string>& labels；Python 没有引用符号。

# 不可变对象（int、float、str）重新赋值时只是让局部名字指向新对象，函数外不受影响。
def raise_price(price: float) -> None:
    price = price + 10               # 局部名字改指向新对象，外部变量仍是原值
    print(f"函数内价格：{price}")

price = 50.0
raise_price(price)                   # -> 函数内价格：60.0
print(f"函数外价格：{price}")        # -> 函数外价格：50.0
# // C++: 参数按值传递时函数内拿到副本；按引用传递才会影响调用方。

# ==================== 12.3.2 返回值设计 ====================
# 好的做法是函数只负责计算并返回结果，打印与使用由调用方决定。
def net_salary(gross: float, insurance_rate: float) -> float:
    """返回实发工资：应发工资扣除社保比例后的金额。"""
    return round(gross * (1 - insurance_rate), 2)

print(net_salary(8000, 0.105))       # -> 7160.0
# 同一结果可以用于打印、累加或写入文件，函数本身不绑定某一种展示方式。
# // C++: double netSalary(double gross, double insuranceRate); 用 return 把结果交给调用方。

# 把“计算”和“打印”混在一起时，调用方拿不到返回值，只能在屏幕上看见结果。
def print_salary(gross: float) -> None:
    print(f"实发工资：{net_salary(gross, 0.105):.2f}")

result = print_salary(8000)          # -> 实发工资：7160.00
print(f"print_salary 的返回值：{result}")    # -> print_salary 的返回值：None
# 展示类函数返回 None 是可以的，但不要指望它还能参与计算。

# 用 int | None 标注“可能找不到结果”的情况，调用方必须区分 0 和“没有找到”。
def find_student(scores: list[int], target: int) -> int | None:
    for index, score in enumerate(scores):
        if score == target:
            return index
    return None

scores = [78, 91, 64]
print(find_student(scores, 91))      # -> 1
print(find_student(scores, 59))      # -> None
# // C++: 常见做法是返回 -1 或 std::optional<int>；Python 用 None 表达“没有值”。

# ==================== 12.3.3 多返回值基础 ====================
# return 后写多个值，实际返回的是一个元组，接收处可以直接解包。
def summarize(scores: list[int]) -> tuple[int, float, int]:
    total = sum(scores)
    return total, total / len(scores), max(scores)

total, average, highest = summarize([78, 91, 64])
print(f"总分：{total}")               # -> 总分：233
print(f"平均分：{average:.2f}")       # -> 平均分：77.67
print(f"最高分：{highest}")           # -> 最高分：91

result = summarize(scores)
print(result)                         # -> (233, 77.66666666666667, 91)
print(type(result))                   # -> <class 'tuple'>
# 元组不可修改；想让调用方只取部分结果时，用 _ 占位忽略不需要的值。
_, average_only, _ = summarize([60, 72])
print(f"只取平均分：{average_only:.2f}")    # -> 只取平均分：66.00
# // C++: 可用 std::tuple 配合 std::tie 或 C++17 结构化绑定：
# // auto [total, average, highest] = summarize(scores);

# 常见坑点：
# 1. 位置参数顺序写反，程序不报错但结果错误。
#    现象：运费、工资等数值明显偏离预期。
#    原因：同类型参数按位置绑定，解释器无法判断语义。
#    正确做法：同类参数较多时改用关键字传参（13.1 讲解），并保持调用顺序一致。
# 2. 在函数内部直接修改传入的列表，调用方的数据被意外改变。
#    现象：函数外的列表多出元素或被清空。
#    原因：Python 按对象引用传递，列表是可变对象。
#    正确做法：需要保留原数据时先复制一份，例如 items = list(items)。
# 3. 以为函数内给参数重新赋值能改变外部变量。
#    现象：函数外仍然是旧值。
#    原因：赋值只是让局部名字指向新对象。
#    正确做法：用 return 把新值交回调用方，由调用方重新绑定。
# 4. 用 0 表示“没有找到”，与真实值为 0 的情况混淆。
#    现象：调用方无法判断失败还是结果为零。
#    原因：返回值缺少独立的失败标记。
#    正确做法：返回 int | None，或返回 (是否成功, 值) 这样的组合。
# 5. 多返回值时忘记解包，把整个元组当成单个数值参与运算。
#    现象：抛出 TypeError，例如 tuple 与 int 相加报错。
#    原因：return a, b 返回的是元组。
#    正确做法：写成 x, y = func()，或先接收元组再按索引取值。
