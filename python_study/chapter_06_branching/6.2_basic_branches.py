# 第 6 章 分支结构
# 6.2 基本分支结构
# 本文件集中学习 if、if-else、if-elif-else 三种基本分支。

# ==================== 6.2.1 if ====================
# if 只有一个分支：条件为真时执行缩进代码块，为假时跳过。
light_is_green = True
if light_is_green:
    print("绿灯亮起，可以通行")
print("继续观察交通信号")
# C++ 对比：
# if (light_is_green) {
#     std::cout << "绿灯亮起，可以通行\n";
# }
# std::cout << "继续观察交通信号\n";
# Python 的冒号和缩进相当于 C++ 的条件括号与花括号结构。

# 条件为假时，if 代码块中的语句不会执行。
weather_is_bad = False
if weather_is_bad:
    print("建议携带雨具")
print("天气判断完成")

# ==================== 6.2.2 if-else ====================
# if-else 有两个互斥分支：一定执行其中一个。
number = 7
if number % 2 == 0:
    print(number, "是偶数")
else:
    print(number, "是奇数")
# C++ 对比：
# if (number % 2 == 0) {
#     std::cout << "偶数\n";
# } else {
#     std::cout << "奇数\n";
# }
# Python 的 else 也要写冒号，并与对应的 if 对齐。

# 通过 if-else 选择两个值中的一个。
price = 120
if price >= 100:
    shipping = 0
else:
    shipping = 10
print("配送费：", shipping)
# C++ 可声明 int shipping; 再在两个分支中赋值。
# Python 变量不需要预先声明，但两个分支都应保证 shipping 最终有值。

# ==================== 6.2.3 if-elif-else ====================
# 多路选择从上到下检查；执行第一个条件为真的分支后停止继续检查。
score = 82
if score >= 90:
    print("等级：A")
elif score >= 80:
    print("等级：B")
elif score >= 60:
    print("等级：C")
else:
    print("等级：D")
# C++ 对比：elif 没有对应关键字，通常写 else if：
# if (score >= 90) { ... }
# else if (score >= 80) { ... }
# else if (score >= 60) { ... }
# else { ... }
# 分支顺序很重要：如果先判断 score >= 60，82 会提前进入该分支。

# 处理边界值：90 进入 A，80 进入 B，60 进入 C，59 进入 D。
score = 60
if score >= 90:
    print("边界测试：A")
elif score >= 80:
    print("边界测试：B")
elif score >= 60:
    print("边界测试：C")
else:
    print("边界测试：D")
# 练习：分别将 score 改为 90、80、59，观察边界变化。
