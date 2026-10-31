# 第 7 章 循环结构
# 7.2 while 循环
# while 适合“只要条件成立就继续”的场景。

# ==================== 7.2.1 基本语法 ====================
# 执行顺序：先判断条件，再执行循环体，再回到条件处重新判断。
count = 1
while count <= 3:
    print("count =", count)
    count += 1
# Python 不支持 ++ 运算符；C++ 常写 ++count。
# C++ 对应结构：
# int count = 1;
# while (count <= 3) {
#     std::cout << count << "\n";
#     ++count;
# }
# Python 的 while 条件后使用冒号，循环体使用缩进；C++ 使用圆括号和花括号。

# 条件一开始为假时，循环体一次也不执行。
count = 5
while count < 3:
    print("这行不会输出")
print("初始条件不成立，循环没有执行")

# ==================== 7.2.2 条件控制循环 ====================
# 循环次数由水位条件决定，不直接写固定次数。
water_level = 0
while water_level < 5:
    water_level += 2
    print("水位：", water_level)
print("达到或超过目标水位：", water_level)
# 2、4、6 是每轮结束后的水位；第 3 轮后水位达到 6，下一轮开始前停止。
# C++ while (water_level < 5) 使用相同的先检查机制。

# 用条件控制倒计时。
remaining = 3
while remaining > 0:
    print("剩余次数：", remaining)
    remaining -= 1
print("次数用完")
# -= 是复合赋值；C++ 和 Python 都支持 -=。

# ==================== 7.2.3 死循环问题分析 ====================
# 死循环通常因为条件一直为真，或者循环变量没有朝结束方向变化。
attempt = 1
while attempt <= 3:
    print("这是有上限的尝试：", attempt)
    attempt += 1  # 忘记这一行会使 attempt 一直为 1
print("循环正常结束")
# 以下是错误思路的文字说明，不执行它：
# while attempt <= 3:
#     print(attempt)
# 如果没有更新 attempt，条件会永远成立。
# C++ while (true) 与 Python while True 都会无限运行，除非 break 或外部中断。
# 本例不运行无限循环，避免教学文件执行后无法正常结束。
