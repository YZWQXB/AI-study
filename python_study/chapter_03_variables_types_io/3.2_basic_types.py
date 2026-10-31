# 第 3 章 变量、数据类型与输入输出
# 3.2 基本数据类型

# 3.2.1 整型 int：表示整数，可用于计数、编号和不带小数的数量。
student_count = 28               # // C++: int student_count = 28;
print("人数：", student_count)

# 3.2.2 浮点型 float：表示带小数的数。二进制浮点数可能无法精确表示某些十进制小数。
height = 1.72                    # // C++: double height = 1.72;
print("身高：", height)
print("0.1 + 0.2 =", 0.1 + 0.2)  # 结果接近 0.3，可能显示为 0.30000000000000004
# // C++: double 也有类似的浮点精度特点；输出时可用格式控制小数位。

# 3.2.3 布尔型 bool：只有 True 和 False，首字母必须大写。
is_enrolled = True               # // C++: bool is_enrolled = true;
is_absent = False                # // C++: bool is_absent = false;
print("已注册：", is_enrolled, "缺席：", is_absent)

# 3.2.4 字符串 str：表示文本。Python 中单个字符也是长度为 1 的字符串。
course_name = "Python 基础"       # // C++: std::string course_name = "Python 基础";
first_letter = "P"               # // C++: char first_letter = 'P';
print(course_name, first_letter)

# 3.2.5 空值 None：表示“目前没有值”，不是数字 0，也不是空字符串。
selected_course = None           # // C++: 可用 std::optional<std::string> 表达“可能没有值”
print("当前选择：", selected_course)
