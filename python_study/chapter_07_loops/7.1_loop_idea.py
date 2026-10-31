# 第 7 章 循环结构
# 7.1 循环思想与适用场景
# 本文件学习重复执行、计数累加遍历，以及设计循环的三个基本步骤。

# ==================== 7.1.1 重复执行问题 ====================
# 不使用循环时，相同结构需要复制多次，修改起来很麻烦。
print("第 1 次：复习变量")
print("第 2 次：复习变量")
print("第 3 次：复习变量")
print("--- 使用循环 ---")
repeat = 1
while repeat <= 3:
    print("第", repeat, "次：复习变量")
    repeat = repeat + 1
# C++ 也用 while 或 for 解决重复执行问题。
# Python 用缩进表示循环体；C++ 用花括号表示循环体。

# ==================== 7.1.2 计数、累加与遍历 ====================
# 计数：每轮把 count 增加 1。
count = 1
while count <= 3:
    print("当前计数：", count)
    count = count + 1

# 累加：把每轮数据加到 total 中。
total = 0
number = 1
while number <= 4:
    total = total + number
    number = number + 1
print("1 到 4 的总和：", total)
# C++ 对比：
# int total = 0;
# for (int number = 1; number <= 4; ++number) total += number;
# Python 没有 ++ 运算符，要写 number += 1 或 number = number + 1。

# 遍历：依次处理字符串中的每一个字符。
word = "code"
for character in word:
    print("正在处理：", character)
# C++ 可写 for (char character : word)；Python for 直接取得元素。

# ==================== 7.1.3 循环设计的基本步骤 ====================
# 步骤 1：确定初值；步骤 2：写继续条件；步骤 3：在循环体中更新。
step = 1  # 初值
while step <= 3:  # 条件
    print("步骤", step)  # 循环体
    step = step + 1  # 更新
print("循环结束时 step：", step)
# 若忘记更新 step，step 会一直为 1，条件永远成立，形成死循环。
# C++ for 常把初值、条件、更新写在一起；while 中同样必须保证有更新。
# 练习：把 <= 3 改成 <= 5，并预测最后的 step 值。
