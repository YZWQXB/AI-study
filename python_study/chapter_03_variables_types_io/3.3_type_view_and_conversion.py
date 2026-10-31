# 第 3 章 变量、数据类型与输入输出
# 3.3 数据类型查看与转换

# 3.3.1 type() 的使用
# type(值) 返回该值的类型对象；初学时常用它确认表达式的结果类型。
number = 12
print(type(number))               # <class 'int'>
print(type(3.5))                  # <class 'float'>
print(type("hello"))              # <class 'str'>
print(type(True))                 # <class 'bool'>
# // C++: 类型通常由声明确定；可用 typeid(number).name() 查询，但输出形式依编译器而异。

# 3.3.2 常见显式类型转换
# int() 将整数文本或数值转换为整数；float() 转换为浮点数。
text_count = "24"
count = int(text_count)           # // C++: int count = std::stoi(text_count);
text_price = "19.95"
price = float(text_price)         # // C++: double price = std::stod(text_price);

# str() 把数值转成字符串，方便输出或与其他文本拼接。
count_text = str(count)           # // C++: std::string count_text = std::to_string(count);
print("数量：" + count_text, "单价：", price)

# bool() 把值转换为布尔值；0 和空字符串为 False，非零数字和非空字符串为 True。
print(bool(0), bool(7))           # False True
print(bool(""), bool("Python"))  # False True
# // C++: 静态转换可写 static_cast<bool>(value)；字符串的“空/非空”通常要显式检查。

# 3.3.3 类型转换中的常见问题
# input() 读取的是字符串，直接与数字做算术会报 TypeError，因此需先转换。
input_text = "18"                # 用固定文本演示，避免运行脚本时要求输入
age = int(input_text)
print(age + 1)

# int() 对浮点数会截掉小数部分，不会四舍五入。
print(int(3.9))                  # 3
print(round(3.9))                # 4；需要四舍五入时使用 round()

# 无法转换的文本会触发 ValueError，例如 int("3.5")；可先分清目标数据格式。
print(int("35"))
# print(int("3.5"))  # 取消注释会发生 ValueError；若文本含小数，应先 float()。
# // C++: std::stoi("3.5") 可能只解析开头的整数部分；解析用户输入要检查格式与结果。
