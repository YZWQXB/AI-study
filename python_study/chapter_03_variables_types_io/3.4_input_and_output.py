# 第 3 章 变量、数据类型与输入输出
# 3.4 输入与输出

# 3.4.1 input() 获取用户输入
# input() 显示提示并读取一整行；无论用户输入数字还是文字，返回值都是 str。
# 取消下面两行注释后运行，程序会等待你输入姓名。
# user_name = input("请输入姓名：")
# print("你好，", user_name)
# // C++: std::string user_name; std::getline(std::cin, user_name);

# 输入数字时，要把字符串显式转换成 int 或 float。
# 示例用固定文本确保脚本可以直接运行；真实输入时可改为 input("请输入年龄：")。
age_text = "18"
age = int(age_text)              # // C++: int age; std::cin >> age;
print("明年年龄：", age + 1)

# 3.4.2 print() 输出内容
# print() 默认输出内容后换行；可传入字符串、数字等常见值。
print("Python 学习开始")
print(2026)
# // C++: std::cout << "Python 学习开始" << std::endl; / std::cout << 2026 << std::endl;

# 3.4.3 多个值的输出方式
# print() 可接收多个值，默认用空格分隔；sep 可指定分隔符。
student_name = "林同学"
score = 96
print("姓名", student_name, "成绩", score)
print("2026", "10", "30", sep="-")
# // C++: std::cout << "姓名 " << student_name << " 成绩 " << score << '\\n';

# end 用于指定末尾字符；这里将两次 print() 合并到同一行。
print("进度：", end="")
print("完成")
