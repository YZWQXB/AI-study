# 第 5 章 字符串与文本处理基础
# 5.2 字符串访问

text = "Python"
# 正向索引从 0 开始： P  y  t  h  o  n
# 索引：                0  1  2  3  4  5
# 负向索引从 -1 开始：-6 -5 -4 -3 -2 -1

# 5.2.1 索引：一次访问一个位置的字符。
print(text[0])                    # P，首字符 // C++: text[0]
print(text[3])                    # h        // C++: text[3]
print(text[-1])                   # n，末字符；C++ 需写 text[text.size() - 1]
# 索引超出范围会产生 IndexError；应确认下标小于 len(text)。

# 5.2.2 切片：text[start:stop] 从 start 开始，取到 stop 之前。
print(text[0:3])                  # Pyt，包含 0、1、2，不包含 3
print(text[2:])                   # thon，从位置 2 取到末尾
print(text[:4])                   # Pyth，从开头取到位置 4 之前
print(text[:])                    # 整个字符串
# // C++: text.substr(0, 3) 的第二个参数是长度；Python 切片的 stop 是结束位置。

# 5.2.3 步长与方向：text[start:stop:step] 中 step 决定跳过多少位置。
print(text[::2])                  # Pto，每隔一个字符取一个
print(text[1::2])                 # yhn，从索引 1 开始隔一个取
print(text[::-1])                 # nohtyP，步长为负数表示反向读取
# C++ 没有直接对应的切片语法，通常用循环或反向迭代器。
