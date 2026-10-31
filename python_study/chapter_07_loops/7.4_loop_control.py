# 第 7 章 循环结构
# 7.4 循环控制语句
# 本文件学习 break、continue、pass 和循环 else。

# ==================== 7.4.1 break ====================
# break 立即结束最近的一层循环，不再处理剩余元素。
for number in range(1, 6):
    if number == 4:
        print("遇到 4，停止搜索")
        break
    print("检查：", number)
print("break 后继续执行循环外代码")
# C++ 的 break 也结束最近的一层循环。

# while 中也可以使用 break。
count = 1
while True:
    print("处理次数：", count)
    if count == 2:
        break
    count += 1
# while True 本身是无限循环，必须依靠 break；C++ 中 while (true) 同理。

# ==================== 7.4.2 continue ====================
# continue 跳过本轮剩余代码，进入下一轮。
for number in range(1, 6):
    if number == 3:
        print("跳过 3")
        continue
    print("处理：", number)
# C++ continue 的效果相同；在 while 中要注意更新语句不能被跳过。

# ==================== 7.4.3 pass ====================
# pass 是“什么也不做”的占位语句。
# Python 的代码块不能为空，暂时不写处理逻辑时必须放 pass。
for number in range(1, 4):
    if number == 2:
        pass  # 以后可以在这里补充对 2 的处理
    print("当前值：", number)
# C++ 可以写空花括号 {}，例如 if (number == 2) { }。
# pass 不会跳过循环，也不会结束循环；continue 才会跳过本轮。

# ==================== 7.4.4 循环 else ====================
# for/while 后的 else 只在循环“自然结束”时执行。
# 如果循环被 break 中断，else 不执行。
for number in range(2, 5):
    print("检查：", number)
else:
    print("循环自然结束，因此执行 else")

for number in range(2, 5):
    if number == 3:
        print("循环被 break 中断")
        break
else:
    print("这一行不会执行")
# C++ 没有与 Python 循环 else 完全相同的语法。
# C++ 通常用 bool found = false，再在循环后 if (!found) 处理未找到情况。
# 练习：把 break 条件改为 number == 5，观察 else 是否执行。
