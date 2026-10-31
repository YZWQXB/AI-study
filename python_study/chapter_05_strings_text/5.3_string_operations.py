# 第 5 章 字符串与文本处理基础
# 5.3 字符串常用操作

# 5.3.1 查找与统计
text = "banana"
print(text.find("na"))            # 2：第一次出现的位置
print(text.find("xy"))            # -1：没找到
print(text.count("a"))            # 3：字符 a 出现次数
# // C++: std::string::find() 找不到返回 std::string::npos；计数常需手写循环。

# 5.3.2 替换与清洗
sentence = "  Hello, Python!  "
cleaned = sentence.strip()         # 去掉两端空白，内部空格保留
print(cleaned)
replaced = cleaned.replace("Python", "C++")
print(replaced)
print(sentence)                    # 原字符串不变，方法返回新字符串
# // C++: std::string 没有同名 strip；去空白通常需遍历，替换常用 find/replace。

# 5.3.3 分割与拼接
csv_line = "red,green,blue"
colors = csv_line.split(",")      # 按逗号分割为字符串列表
print(colors)
joined = " | ".join(colors)        # 用分隔符把列表项目连接成字符串
print(joined)
# // C++: 可用 std::getline(istringstream, item, ',') 分隔；连接通常用循环。

# 5.3.4 大小写转换
word = "Hello Python"
print(word.upper())                # HELLO PYTHON
print(word.lower())                # hello python
print(word.title())                # Hello Python
# 这些方法返回新字符串，word 本身仍然是 "Hello Python"。
# // C++: 常用大小写转换通常需配合循环和 std::toupper/std::tolower。
