# 第 17 章 Python 基础规范与良好习惯
# 17.3 初学者常见反模式
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件用订单、结算、成绩场景展示复制粘贴、深层嵌套、命名混乱与宽泛异常捕获的重构前后。

# ==================== 17.3.1 复制粘贴式编程 ====================
# 重构前：三个城市的运费规则几乎一模一样，只改了重量数据。
beijing_weight = 2.0
if beijing_weight > 1:
    beijing_fee = round(10.0 + (beijing_weight - 1) * 5, 2)
else:
    beijing_fee = 10.0

shanghai_weight = 0.5
if shanghai_weight > 1:
    shanghai_fee = round(10.0 + (shanghai_weight - 1) * 5, 2)
else:
    shanghai_fee = 10.0

shenzhen_weight = 6.3
if shenzhen_weight > 1:
    shenzhen_fee = round(10.0 + (shenzhen_weight - 1) * 5, 2)
else:
    shenzhen_fee = 10.0

print(beijing_fee, shanghai_fee, shenzhen_fee)               # -> 15.0 10.0 36.5
# 重构后：规则只写一次，数据通过参数传进来，顺便补上重构前缺失的参数校验。
def shipping_fee(weight: float) -> float:
    if weight <= 0:
        raise ValueError(f"重量必须大于 0，当前为 {weight}")
    if weight <= 1:
        return 10.0
    return round(10.0 + (weight - 1) * 5, 2)


print(shipping_fee(2.0), shipping_fee(0.5), shipping_fee(6.3))   # -> 15.0 10.0 36.5
print((beijing_fee, shanghai_fee, shenzhen_fee)
      == (shipping_fee(2.0), shipping_fee(0.5), shipping_fee(6.3)))   # -> True
# 判断是否该抽函数：同样的逻辑出现两次以上，或者改规则时必须同步改多处。
# // C++: 同样把重复的 if-else 提炼成 double shippingFee(double weight)；
# // 复制粘贴在 C++ 里同样会被编译器帮倒忙（改一处漏一处不会报错）。

# ==================== 17.3.2 过深嵌套 ====================
# 重构前：四层 if 嵌套，正常路径藏在最深处，else 分支离条件很远。
def can_checkout_bad(user_active: bool, is_member: bool, stock: int, quantity: int) -> str:
    if user_active:
        if stock > 0:
            if quantity <= stock:
                if is_member:
                    return "会员可下单"
                else:
                    return "普通用户可下单"
            else:
                return "库存不足"
        else:
            return "商品缺货"
    else:
        return "账户未激活"


# 重构后：守卫式提前返回，把异常情况逐个挡在门口，主流程留在函数末尾。
def can_checkout(user_active: bool, is_member: bool, stock: int, quantity: int) -> str:
    if not user_active:
        return "账户未激活"
    if stock <= 0:
        return "商品缺货"
    if quantity <= 0:
        return "数量必须大于 0"
    if quantity > stock:
        return "库存不足"
    return "会员可下单" if is_member else "普通用户可下单"


checkout_cases = [
    (True, True, 10, 2),
    (True, False, 10, 2),
    (True, True, 3, 5),
    (True, True, 0, 1),
    (False, True, 10, 2),
]
print([can_checkout(*case) for case in checkout_cases])
# -> ['会员可下单', '普通用户可下单', '库存不足', '商品缺货', '账户未激活']
# 除新增的“数量必须大于 0”外，重构前后所有分支结果完全一致。
# 嵌套超过三层通常说明条件太多；先把“不满足就结束”的情况提到前面。
# // C++: 同样可以用 guard clause + return，收益在于主路径缩进层级变浅。

# ==================== 17.3.3 变量命名混乱 ====================
# 重构前：data、tmp、flag 三个名字都没说明含义，也不知道单位。
data = [78, 55, 91]
tmp = 0
for x in data:
    tmp += x
flag = tmp / len(data) >= 60
print(tmp, flag)                                             # -> 224 True
# 重构后：名字直接表达“课程成绩、总分、是否班级达标”。
course_scores = [78, 55, 91]
total_score = sum(course_scores)
is_class_passed = total_score / len(course_scores) >= 60
print(total_score, is_class_passed)                          # -> 224 True
# 命名还包括避免覆盖内置名字：局部变量用了 list，这个作用域里 list 就不再是类型。
def shadow_demo() -> None:
    list = [3, 1, 2]                                         # 覆盖了内置名 list
    print(len(list))                                         # -> 3
    try:
        list("abc")                                          # 这里的 list 是列表对象
    except TypeError as error:
        print(type(error).__name__)                          # -> TypeError


shadow_demo()
# // C++: 命名冲突由作用域与类型系统约束，Python 的内置名可以被变量覆盖，只能靠自觉避免。

# ==================== 17.3.4 宽泛异常捕获 ====================
# 重构前：except Exception 把所有错误都变成 0，包括写错变量名这种真正的 bug。
def total_amount_bad(quantity_text: str, unit_price: float) -> float:
    try:
        return int(quantity_text) * unit_pirce          # 故意拼错：unit_pirce
    except Exception:
        return 0.0


print(total_amount_bad("3", 9.5))                            # -> 0.0
# 结果看起来“正常”，其实是拼写错误被吞掉了，排查会从业务逻辑一路找错方向。
# 重构后：只在真正可能失败的地方捕获具体异常，并把错误原因说清楚。
def parse_quantity(text: str) -> int:
    cleaned = text.strip()
    if not cleaned.isdigit():
        raise ValueError(f"数量必须是正整数，当前输入：{cleaned!r}")
    return int(cleaned)


for raw_text in ["3", " 8 ", "abc", "-2", ""]:
    try:
        print(f"解析成功：{parse_quantity(raw_text)}")
    except ValueError as error:
        print(f"解析失败：{error}")
# 输出五行：
# -> 解析成功：3
# -> 解析成功：8
# -> 解析失败：数量必须是正整数，当前输入：'abc'
# -> 解析失败：数量必须是正整数，当前输入：'-2'
# -> 解析失败：数量必须是正整数，当前输入：''
# 捕获的原则：能处理的错误才捕获，捕获后必须给出明确结果或重新抛出。
# // C++: catch (...) 对应 Python 的裸 except，都会把真正的程序缺陷藏起来。

# 常见坑点：
# 1. 现象：三个分支改了两个，另一个还按旧规则算；原因：复制粘贴后没同步；
#    做法：抽成一个函数，把变化的部分变成参数。
# 2. 现象：代码越改越往右缩进，正常逻辑看不出来；原因：条件用嵌套表达；
#    做法：用守卫式判断提前 return，把正常路径放平。
# 3. 现象：看代码时完全猜不到 data / tmp / flag 是什么；原因：名字没有业务含义；
#    做法：用 course_scores / total_score / is_class_passed 这类可读名字。
# 4. 现象：程序不报错但结果总是 0；原因：except Exception 吞掉了拼写错误；
#    做法：只捕获 ValueError 等预期异常，让 NameError 等缺陷暴露出来。
# 5. 现象：变量名为 list/sum/dict 后调用同名内置函数报 TypeError；
#    原因：内置名被覆盖；做法：换个名字，如 items、total_score。
