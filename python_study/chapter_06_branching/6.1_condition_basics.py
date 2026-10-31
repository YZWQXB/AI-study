# 第 6 章 分支结构
# 6.1 条件判断基础
# 学习目标：理解条件表达式、真值和缩进；本文件不使用循环或函数。
# 所有数据均为固定演示值，直接运行即可观察结果，也可修改数据再运行。

# ==================== 6.1.1 条件表达式 ====================
# 条件表达式描述一个能够判断真假的问题。
# Python 的布尔字面量是 True / False；C++ 是 true / false。
score = 75
print("成绩：", score)
print("是否及格：", score >= 60)  # True
print("是否满分：", score == 100)  # False
print("是否不及格：", score < 60)  # False

# 比较结果可以保存到变量，再作为 if 的条件。
is_passed = score >= 60
if is_passed:
    print("成绩达到及格标准")

# C++ 对比：
# bool is_passed = score >= 60;
# if (is_passed) { std::cout << "成绩达到及格标准\n"; }
# Python 不写变量类型、语句末尾不需要分号；if 条件后写冒号。
# == 表示比较，= 表示赋值；不要把两者混淆。
# Python 中 if score = 60: 是语法错误，不要取消注释执行。
# C++ 的 if (score = 60) 却可能合法：先赋值再判断，容易产生错误。

# Python 支持链式比较；C++ 不能直接照搬该写法。
age = 20
print("年龄在 18 到 60 之间：", 18 <= age <= 60)
# C++ 应写 18 <= age && age <= 60。
# C++ 的 18 <= age <= 60 会先计算左侧比较，再拿 bool 与 60 比较。

# ==================== 6.1.2 真值判断规则 ====================
# if 不只接受布尔变量：某些值可直接用于条件，Python 会判断其真值。
# 这里只使用已经学习过的数字、字符串和 None，不提前引入容器。
# 数值 0、0.0，空字符串 ""，None，False 为假。
# 非零数值（包括负数）、非空字符串、True 为真。
print("0 的真值：", bool(0))
print("0.0 的真值：", bool(0.0))
print("负数的真值：", bool(-3))
print("空字符串的真值：", bool(""))
print("文本 0 的真值：", bool("0"))
print("文本 False 的真值：", bool("False"))
print("None 的真值：", bool(None))
# 注意：字符串 "0" 和 "False" 都非空，并不会按文本含义变成假。

name = "小林"
if name:
    print("姓名非空：", name)
# C++ 的整数和浮点数也以零为假、非零为真。
# std::string 不能直接当作 bool 使用，应写 if (!name.empty())。
# Python 的 None 表示无值；C++ 的 nullptr 表示空指针，两者概念并不完全相同。

stock = -2
print("库存数值非零：", bool(stock))
print("库存数量充足：", stock > 0)
# 真值不等于业务条件：库存为负数时仍是真，但不代表有库存。

# ==================== 6.1.3 缩进与代码块 ====================
# 使用 4 个空格缩进；同一个代码块中缩进必须一致，不混用制表符。
# Python 用冒号开启代码块、用缩进表示归属；C++ 用 {} 表示归属。
temperature = 30
if temperature >= 28:
    print("天气较热")
    print("请补充水分")
print("温度检查结束")  # 已退回原缩进，不属于 if
# C++ 对应结构：
# if (temperature >= 28) {
#     std::cout << "天气较热\n";
#     std::cout << "请补充水分\n";
# }
# std::cout << "温度检查结束\n";
# 将 temperature 改为 20：前两句不输出，最后一句仍输出。
# C++ 中缩进主要服务阅读；Python 中缩进本身就是语法的一部分。
# 练习：修改 score、name、temperature，先预测输出，再运行核对。


# if score >= 60:
#     if score >= 90:
#         print("优秀")
#     print("成绩达到及格标准")
# else:
#     print("成绩不及格")