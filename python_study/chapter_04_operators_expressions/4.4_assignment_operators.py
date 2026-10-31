# 第 4 章 运算符与表达式
# 4.4 赋值与复合赋值

# 4.4.1 基础赋值：= 把右侧的值绑定给左侧变量。
score = 80                       # // C++: int score = 80;
print("初始成绩：", score)

# 4.4.2 复合赋值：在原变量基础上运算，再把结果存回去。
score += 5                       # 等同于 score = score + 5
print("加 5 后：", score)        # // C++: score += 5;
score -= 2                       # 等同于 score = score - 2
print("减 2 后：", score)        # // C++: score -= 2;
score *= 2                       # 等同于 score = score * 2
print("乘 2 后：", score)        # // C++: score *= 2;
score /= 2                       # / 的结果是 float，所以 score 现在是浮点数
print("除以 2 后：", score)      # // C++: score /= 2; 若 score 是 int，结果会保留整数类型

# 4.4.3 多变量赋值与交换
# Python 可同时为多个变量赋值，左右项目数量需要对应。
x, y = 3, 7                     # // C++: int x = 3; int y = 7;
print("x, y：", x, y)

# 交换变量无需临时变量。
x, y = y, x                     # // C++: std::swap(x, y);
print("交换后：", x, y)

# Python 支持链式赋值；这里给两个变量分别绑定整数 0。
a = b = 0
print(a, b)
# 对可变对象（如列表）要避免不理解地链式赋值，因为两个名字会指向同一个对象。
