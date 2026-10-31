# 第 4 章 运算符与表达式
# 4.3 逻辑运算符

# 4.3.1 and：两侧条件都为真时，整体才为真。
has_id = True
is_adult = True
can_register = has_id and is_adult
print("可以登记：", can_register)
# // C++: bool can_register = has_id && is_adult;

# and 会短路：左侧为假时，右侧不再计算，因为整体结果已确定为假。
number = 0
print(number != 0 and 10 / number > 1)  # False，不会执行除法
# // C++: number != 0 && 10 / number > 1，同样会短路

# 4.3.2 or：至少一侧条件为真时，整体为真。
is_weekend = False
is_holiday = True
can_rest = is_weekend or is_holiday
print("可以休息：", can_rest)
# // C++: bool can_rest = is_weekend || is_holiday;

# or 也会短路：左侧为真时，右侧不再计算。
print(True or 10 / 0 > 1)          # True，右侧除法不会执行

# 4.3.3 not：把真变假，把假变真。
is_locked = False
print("是否未锁定：", not is_locked)
# // C++: !is_locked

# and 比 or 优先级高；条件组合较多时，用括号表达意图。
print(True or False and False)    # True，即 True or (False and False)
print((True or False) and False)  # False
# // C++: 优先级也有区别于括号的规则，但加括号同样能让表达式更清楚。
