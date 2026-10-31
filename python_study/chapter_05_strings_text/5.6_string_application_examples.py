# 第 5 章 字符串与文本处理基础
# 5.6 字符串应用案例

# 5.6.1 用户信息格式化输出
# 把姓名、年龄、城市放进统一模板；示例数据固定，运行时不会收集个人信息。
name = "李同学"
age = 19
city = "杭州"
profile = f"姓名：{name} | 年龄：{age} | 城市：{city}"
print(profile)
# // C++20: std::format("姓名：{} | 年龄：{} | 城市：{}", name, age, city)

# 5.6.2 简单文本清洗
raw_line = "  Python,  入门课程  "
clean_line = raw_line.strip()      # 去掉首尾空白
clean_line = clean_line.replace(",", "，")
print(clean_line)
# split() 可以去除多余空格产生的空项，再用 join() 统一为单空格。
raw_words = "  learn   Python   today  "
words = raw_words.split()
normalized = " ".join(words)
print(normalized)
# // C++: 可用 stringstream 提取词语，再用单空格重新连接。

# 5.6.3 口令规则校验基础
# 教学示例只检查长度和是否同时含字母与数字；真实系统还需安全存储与安全认证。
# 示例口令为演示数据，不应使用真实密码。
password = "learn2026"
has_minimum_length = len(password) >= 8
has_letter = False
has_digit = False

# 用基础 for 循环逐个检查字符，不使用生成器表达式。
for character in password:
    if character.isalpha():
        has_letter = True
    if character.isdigit():
        has_digit = True

if has_minimum_length and has_letter and has_digit:
    print("示例口令符合基础规则")
else:
    print("示例口令不符合基础规则")
# // C++: 可遍历 std::string 检查长度、字母和数字；Unicode 文本需注意字符分类与编码。
