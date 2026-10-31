# 第 3 章 变量、数据类型与输入输出
# 3.1 变量与命名规则

# 3.1.1 变量的概念与作用
# 变量是给数据起的名字，方便后续读取、计算或更新。
# Python 赋值时，名字会绑定到一个对象；通常不必提前声明类型。
student_name = "林同学"          # // C++: std::string student_name = "林同学";
student_age = 18                 # // C++: int student_age = 18;
print(student_name, student_age)

# Python 的名字可以在之后绑定到不同类型的对象；C++ 普通变量的类型固定。
value = 10                       # // C++: int value = 10;
value = "十"                     # // C++: 不能把 int value 重新赋成 std::string
print("value 当前表示：", value)

# 3.1.2 标识符命名规则
# 标识符可含字母、数字、下划线，不能以数字开头，且区分大小写。
user2_score = 95                 # 合法：数字不在开头
_user_note = "练习中"            # 合法：以下划线开头
User2_score = 88                 # 与 user2_score 是不同名字
print(user2_score, User2_score, _user_note)

# 以下是非法名称示例，不能直接运行：
# 2user = "错误：不能以数字开头"
# user-name = "错误：连字符不是标识符字符"
# for = 1  # 错误：for 是 Python 关键字
# C++ 同样不允许标识符以数字开头，也不允许把关键字作为变量名。

# 3.1.3 语义化命名习惯
# 名字尽量描述用途；Python 通常用小写字母和下划线（snake_case）。
# userAge 虽可运行，但更推荐 user_age；避免使用 x1、a2 等含义不清的名字。
item_price = 12.5                # // C++ 常见风格: itemPrice
item_count = 3
total_price = item_price * item_count
print(f"商品总价：{total_price}")
