# 第 15 章 异常处理与基础调试
# 15.2 常见异常类型
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：认识 NameError、TypeError、ValueError、IndexError、KeyError 的触发条件与识别方法。

# ==================== 15.2.1 NameError ====================
# 使用了还没定义的名字，最常见原因是变量名拼错或分支没有执行。
amount = 120
try:
    print(amout)
except NameError as error:
    print("类型：", type(error).__name__)     # -> 类型： NameError
    print("信息：", error)                    # -> 信息： name 'amout' is not defined
# // C++: 未声明的变量直接编译失败；Python 直到执行到那一行才发现名字不存在。
# 因此拼写错误在 Python 里属于运行时异常，而不是编译期错误。

if False:
    discount = 0.8
try:
    print(discount)
except NameError as error:
    print("分支未执行导致未定义：", type(error).__name__)   # -> 分支未执行导致未定义： NameError
# 变量只在某个分支里赋值时，另一个分支使用它就必然报错；应先赋默认值。

# ==================== 15.2.2 TypeError ====================
# 类型不匹配：对不能做该操作的对象用了错误的方法或运算符。
quantity = "3"
price = 2.5
try:
    print(quantity * price)
except TypeError as error:
    print("类型：", type(error).__name__)     # -> 类型： TypeError
    print("信息：", error)                    # -> 信息： can't multiply sequence by non-int of type 'float'
# 更隐蔽的是整数字符串：字符串乘整数会重复字符串而不是做乘法，不报错但结果错误。
print("字符串重复而不是相乘：", "3" * 2)      # -> 字符串重复而不是相乘： 33
print("修正后金额：", int(quantity) * price)   # -> 修正后金额： 7.5

try:
    print(len(42))
except TypeError as error:
    print("对整数取长度：", type(error).__name__)   # -> 对整数取长度： TypeError

# ==================== 15.2.3 ValueError ====================
# 类型正确但内容不合法，典型场景是字符串转数字。
raw_score = "八十八"
try:
    score = int(raw_score)
except ValueError as error:
    print("类型：", type(error).__name__)     # -> 类型： ValueError
    print("信息：", error)                    # -> 信息： invalid literal for int() with base 10: '八十八'
# int() 会忽略首尾空白，但不接受中文数字、小数点或空字符串。
print("带空白的整数：", int(" 88 "))          # -> 带空白的整数： 88

try:
    print(int("88.5"))
except ValueError as error:
    print("小数文本转 int：", type(error).__name__)   # -> 小数文本转 int： ValueError
# 想得到 88.5 应先用 float() 转换；类型选错也会表现为 ValueError。

# ==================== 15.2.4 IndexError 与 KeyError ====================
# 两个都表示“要找的东西不在容器里”：列表按下标越界抛 IndexError，字典按键缺失抛 KeyError。
records = ["A-101", "B-205"]
try:
    print(records[2])
except IndexError as error:
    print("类型：", type(error).__name__)     # -> 类型： IndexError
    print("信息：", error)                    # -> 信息： list index out of range
# 负数下标是合法的，-1 表示最后一个元素；只有超出长度范围才会越界。
print("负数索引取末尾：", records[-1])          # -> 负数索引取末尾： B-205

order = {"item": "显示器", "count": 2}
try:
    print(order["price"])
except KeyError as error:
    print("类型：", type(error).__name__)      # -> 类型： KeyError
    print("信息：", error)                     # -> 信息： 'price'
    print("缺失的键名：", error.args[0])       # -> 缺失的键名： price
# KeyError 的信息是键的 repr，所以带引号；取原始键名应使用 error.args[0]。

print("get 提供默认值：", order.get("price", "未报价"))   # -> get 提供默认值： 未报价
if len(records) > 1:
    print("先判断长度再取值：", records[1])               # -> 先判断长度再取值： B-205

# 常见坑点：
# 1. 打印 KeyError 时看到带引号的 'price' 就以为键里多了引号：那是 repr 的表现；用 error.args[0] 取原始键。
# 2. 先用 if key in data 判断再用 data[key] 取值：多一次查找；直接 data.get(key, 默认值) 更简洁。
# 3. 把 IndexError 和 KeyError 混为一谈：列表按下标、字典按键，异常类型不同，捕获错了就漏处理。
# 4. 用 except Exception 兜住全部异常：连拼写错误也被吞掉，真正的类型问题反而查不出来。
# 5. 认为负下标一定越界：-1、-2 在长度范围内都合法，是否越界要看 len() 而不是看符号。
