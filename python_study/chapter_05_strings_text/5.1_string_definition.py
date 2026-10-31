# 第 5 章 字符串与文本处理基础
# 5.1 字符串的定义与表示

# 5.1.1 单引号、双引号与三引号
# 单引号与双引号都能定义字符串；选择不与内容冲突的一种即可。
word = 'Python'                  # // C++: std::string word = "Python";
quote = "It's a book"             # 内容有单引号，所以外层使用双引号
print(word, quote)
# // C++: 字符串通常使用双引号；单引号表示 char，例如 char letter = 'P';

# 三引号可以直接写多行文本，换行会保留在字符串中。
poem = """春天来了
花儿开放"""
print(poem)
# // C++: 可用 raw string literal R"(... )" 或显式写入换行符。

# 5.1.2 转义字符
# 反斜杠引入特殊字符：\n 换行，\t 制表，\\ 表示一个反斜杠。
text = "第一行\n第二行\t结束"
print(text)
print("路径分隔符：C:\\Users\\student")
# // C++: 常见转义如 \n、\t、\\ 也可用于字符串字面量。

# 5.1.3 字符串的不可变性基础
# 字符串创建后不能直接改其中一个字符；修改时应构造新的字符串。
original = "cat"
updated = "b" + original[1:]
print("原字符串：", original)
print("新字符串：", updated)
# // C++: std::string s = "cat"; s[0] = 'b'; C++ 字符串可通过下标修改字符。

# Python 字符串方法也会返回新字符串，不会原地改写 original。
upper_text = original.upper()
print(original, upper_text)
