# 第 7 章 循环结构
# 7.3 for 循环
# for 适合遍历一组已有的数据，或遍历 range() 产生的整数。

# ==================== 7.3.1 遍历思想 ====================
# for 会依次取得字符串中的每一个字符。
word = "cat"
for character in word:
    print("当前字符：", character)
# C++ 对比：
# std::string word = "cat";
# for (char character : word) {
#     std::cout << character << "\n";
# }
# Python 不需要声明 character 的类型，也不需要手动写下标递增。

# 遍历时可以直接对每个元素进行条件判断。
text = "Python"
for character in text:
    if character == "P":
        print("找到了首字母 P")
# C++ 可在范围 for 的循环体内写 if (character == 'P')。

# ==================== 7.3.2 range() 的使用 ====================
# range(stop)：从 0 开始，到 stop 之前结束，不包含 stop。
for number in range(5):
    print(number)  # 0, 1, 2, 3, 4

# range(start, stop)：从 start 开始，到 stop 之前结束。
print("从 2 到 5：")
for number in range(2, 6):
    print(number)  # 2, 3, 4, 5

# range(start, stop, step)：每次按 step 改变。
print("从 1 开始，每次增加 2：")
for number in range(1, 7, 2):
    print(number)  # 1, 3, 5

print("倒序：")
for number in range(5, 0, -1):
    print(number)  # 5, 4, 3, 2, 1
# C++ 通常写 for (int number = 0; number < 5; ++number)。
# range(5) 的“结束值不包含”与 C++ 的 number < 5 思路一致。

# ==================== 7.3.3 字符串与列表遍历 ====================
# 字符串可以直接遍历。
message = "Hi!"
for character in message:
    print("字符：", character)

# 也可以按索引遍历；len() 返回字符串长度。
for index in range(len(message)):
    print("位置", index, "是", message[index])
# C++ 可使用 for (size_t index = 0; index < message.size(); ++index)。

# 列表将在第 9 章系统学习；这里只用固定列表展示遍历形式。
colors = ["red", "green", "blue"]
for color in colors:
    print("颜色：", color)
# C++ 常见写法：std::vector<std::string> colors; 再用范围 for 遍历。
# 本节重点是“逐个取得元素”，暂不介绍列表方法和列表推导式。


# for _ in range(5):
#     print("home")