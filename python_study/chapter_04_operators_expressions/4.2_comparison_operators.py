# 第 4 章 运算符与表达式
# 4.2 比较运算符

# 4.2.1 大小比较：比较数字大小，表达式的结果是 True 或 False。
score = 86
print(score > 60)                 # True  // C++: score > 60
print(score >= 90)                # False // C++: score >= 90
print(score < 100)                # True  // C++: score < 100
print(score <= 86)                # True  // C++: score <= 86

# Python 支持链式比较，含义是两边条件同时成立。
age = 20
print(0 < age < 120)              # True
# // C++: 0 < age && age < 120；不要直接写 0 < age < 120

# 4.2.2 相等与不相等判断
# == 比较两个值是否相等；!= 比较两个值是否不相等。
print(5 == 5)                     # True  // C++: 5 == 5
print(5 != 3)                     # True  // C++: 5 != 3
print("cat" == "dog")             # False // C++: std::string("cat") == "dog"

# = 是赋值，== 才是比较；二者用途不同。
answer = 42                       # 把 42 赋给 answer
print(answer == 42)               # 比较 answer 是否等于 42
# // C++ 同样区分 = 和 ==。

# 4.2.3 比较结果的布尔值语义
# 比较表达式的结果是 bool，可直接用于后续逻辑判断。
passed = score >= 60
print("是否及格：", passed, type(passed))
# // C++: bool passed = score >= 60;

if passed:
    print("成绩合格")
else:
    print("需要继续练习")
# Python 的 if 条件后面写冒号并缩进代码块；C++ 使用括号和花括号。
