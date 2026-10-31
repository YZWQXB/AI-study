# 第 4 章 运算符与表达式
# 4.5 成员运算与身份运算基础

# 4.5.1 in 与 not in：检查一个值是否出现在序列或字符串中。
colors = ["红", "绿", "蓝"]
print("绿" in colors)             # True
print("黄" not in colors)         # True
print("Py" in "Python")           # True
# // C++: 容器通常使用 find() 或算法库的 std::find() 检查元素。

# 4.5.2 is 与 is not：检查两个名字是否指向同一个对象。
value = None
print(value is None)              # True，None 检查推荐写法
print(value is not None)          # False
# // C++: 对指针可比较地址或 nullptr；普通值比较通常用 ==。

# 4.5.3 == 与 is 的区别认知
# == 比较值是否相等；is 比较是否为同一个对象。多数普通值比较应使用 ==。
first = [1, 2]
second = [1, 2]
third = first
print(first == second)            # True：列表内容相等
print(first is second)            # False：这是两个不同列表对象
print(first is third)             # True：third 与 first 指向同一对象
# // C++: std::vector 的 == 比较内容；对象地址可用 &first == &second 检查。

# 不要用 is 比较字符串或数字的值；对象复用细节不应作为程序逻辑依据。
name = "Python"
print(name == "Python")           # 比较文本值，推荐
# print(name is "Python")  # 不要这样写
