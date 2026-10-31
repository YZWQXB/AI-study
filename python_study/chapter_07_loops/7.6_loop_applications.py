# 第 7 章 循环结构
# 7.6 循环综合应用
# 本文件把条件、循环、变量和基础输入思想组合起来。

# ==================== 7.6.1 猜数字游戏 ====================
# 为保证教学文件直接运行，这里使用固定猜测值，并逐次调整猜测。
# import random
# secret_number = random.randint(1, 10)
guess = 3
while guess != secret_number:
    if guess < secret_number:
        print("猜小了")
        guess += 1
    else:
        print("猜大了")
        guess -= 1
    print("下一次演示猜测：", guess)
print("猜中了：", secret_number)
# 真实交互时可以把 guess = 3 改为 int(input("请输入猜测："))。
# C++ 对比：int guess; cin >> guess;，再使用 while 和 if 比较。
# 本例没有使用随机数，随机数会在后续标准库内容中学习。

# ==================== 7.6.2 简单账户重试逻辑 ====================
# 限制最多尝试 3 次；成功时 break，次数耗尽时由循环 else 提示。
correct_pin = "2468"
attempt = 1
max_attempts = 3
entered_pin = "0000"  # 固定错误示例；不要放入真实口令
while attempt <= max_attempts:
    print("第", attempt, "次验证")
    if entered_pin == correct_pin:
        print("验证成功")
        break
    else:
        print("验证失败")
    attempt += 1
else:
    print("尝试次数已用完")
# C++ 通常用 for/while、break 和 bool 状态变量完成相同逻辑。
# C++ 没有 Python 的循环 else，因此可在循环结束后判断成功标志。
# 真实系统不应明文保存口令，还应设计安全的失败处理策略。

# ==================== 7.6.3 批量数据处理入门 ====================
# 列表将在第 9 章系统学习；这里仅用固定列表展示逐项处理。
scores = [78, 55, 91, 63]
total = 0
passed_count = 0
for score in scores:
    total += score
    if score >= 60:
        passed_count += 1
    print("处理成绩：", score)
print("总分：", total)
print("及格人数：", passed_count)
# C++ 可使用 vector<int> scores，并用范围 for 遍历：
# for (int score : scores) {
#     total += score;
#     if (score >= 60) ++passed_count;
# }
# Python 的列表写法简洁，但列表方法、切片和推导式不在本章展开。

# 这个案例体现批处理的基本步骤：
# 1. 准备一组数据；2. 逐项取出；3. 对每项计算；4. 汇总并输出结果。
