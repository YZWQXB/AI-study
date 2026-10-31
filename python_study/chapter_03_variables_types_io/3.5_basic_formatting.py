# 第 3 章 变量、数据类型与输入输出
# 3.5 基础格式化输出

# 格式化是把变量值按指定模板放进文本。下面三种写法均可输出相同信息。
name = "小周"
age = 20

# 3.5.1 % 格式化基础
# %s 表示字符串，%d 表示整数；% 后的值按顺序填入占位符。
print("姓名：%s，年龄：%d" % (name, age))
# // C++: printf("姓名：%s，年龄：%d\\n", name.c_str(), age);

# 3.5.2 format() 基础
# {} 是占位符；format() 按顺序提供对应值。也可以用位置编号明确指定。
print("姓名：{}，年龄：{}".format(name, age))
print("{1}岁的人叫{0}".format(name, age))
# // C++20: std::format("姓名：{}，年龄：{}", name, age)

# 3.5.3 f-string 基础（Python 3.6+）
# 在字符串前加 f，变量名或简单表达式可直接写进大括号。
print(f"姓名：{name}，年龄：{age}")
print(f"明年年龄：{age + 1}")
# // C++20: std::format("姓名：{}，年龄：{}", name, age)

# f-string 可控制小数位数；:.2f 表示保留两位小数。
price = 12.5
print(f"价格：{price:.2f}")
