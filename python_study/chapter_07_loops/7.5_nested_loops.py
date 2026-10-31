# 第 7 章 循环结构
# 7.5 循环嵌套
# 外层循环控制大步骤，内层循环完成每个大步骤中的重复工作。

# ==================== 7.5.1 嵌套循环执行过程 ====================
# 外层每执行一轮，内层都会从头到尾执行一次。
for row in range(1, 4):
    print("外层第", row, "轮开始")
    for column in range(1, 3):
        print("  内层第", column, "轮")
    print("外层第", row, "轮结束")
# 内层总执行次数为 3 * 2 = 6。
# C++ 嵌套 for 的执行顺序相同：外层进入一轮后，内层完整执行。

# ==================== 7.5.2 图形输出 ====================
# 外层控制行号，内层控制当前行打印几个星号。
for row in range(1, 5):
    for column in range(row):
        print("*", end="")
    print()  # 空 print 负责换行
# 第 1 行 1 个，第 2 行 2 个，以此类推。
# C++ 可用 cout << "*" 输出符号，内层结束后 cout << endl 换行。
# end="" 表示 print 后不换行；默认 print 会换行。

# 矩形图形：每一行都打印 5 个符号。
for row in range(3):
    for column in range(5):
        print("#", end="")
    print()
# row 在本例只控制行数，column 控制每行符号数。

# ==================== 7.5.3 九九乘法表 ====================
# 外层提供被乘数，内层从 1 乘到当前被乘数。
for left in range(1, 10):
    for right in range(1, left + 1):
        print(f"{right}*{left}={right * left}", end="  ")
    print()
# f-string 把变量放进输出文本；C++ 可用多个 <<：
# cout << right << "*" << left << "=" << right * left;
# Python 的 range(left + 1) 结束值不包含，所以这里使用 range(1, left + 1)。
# 练习：修改外层范围，输出 1 到 5 的部分乘法表。
