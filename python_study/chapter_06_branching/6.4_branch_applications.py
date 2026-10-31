# 第 6 章 分支结构
# 6.4 分支应用案例
# 本文件使用分支结构完成成绩判断、登录认证和简单菜单。

# ==================== 6.4.1 成绩等级判断 ====================
# 先检查范围，再从高到低判断等级。
score = 76
if score < 0 or score > 100:
    print("成绩超出有效范围")
elif score >= 90:
    print("成绩等级：优秀")
elif score >= 80:
    print("成绩等级：良好")
elif score >= 60:
    print("成绩等级：及格")
else:
    print("成绩等级：需要继续努力")
# C++ 对比：
# if (score < 0 || score > 100) { ... }
# else if (score >= 90) { ... }
# Python 的 or 对应 C++ 的 ||，elif 对应 C++ 的 else if。
# 如果把 score >= 60 放在第一位，76 会直接得到“及格”，所以顺序必须从高到低。

# ==================== 6.4.2 登录认证逻辑 ====================
# 固定文本只用于教学，不要在真实项目中明文保存真实密码。
saved_name = "student"
saved_password = "python123"
entered_name = "student"
entered_password = "python123"
if entered_name == saved_name:
    if entered_password == saved_password:
        print("登录成功")
    else:
        print("口令错误")
else:
    print("账户不存在")
# C++ 可使用 std::string，并使用 == 比较字符串内容：
# if (entered_name == saved_name) {
#     if (entered_password == saved_password) { ... }
# }
# Python 字符串 == 比较内容；不要用 is 比较字符串内容。
# 真实系统还需要哈希存储、失败次数限制和安全的身份认证机制。

# 也可以用 and 写成单层分支；嵌套结构在这里更能展示认证步骤。
if entered_name == saved_name and entered_password == saved_password:
    print("单层判断：凭据同时正确")
else:
    print("单层判断：凭据不完整")

# ==================== 6.4.3 简单菜单选择程序 ====================
# 输出菜单后，用固定字符串模拟用户选择。
# 实际练习时，可以改为 choice = input("请选择：")。
print("1. 查看余额")
print("2. 存入金额")
print("3. 退出")
choice = "2"
if choice == "1":
    print("当前余额：100 元")
elif choice == "2":
    print("进入存款操作")
elif choice == "3":
    print("已选择退出")
else:
    print("无效选项")
# C++ 可以用 if / else if，也可以在整数选项上使用 switch：
# switch (choice) {
# case 1: ...; break;
# case 2: ...; break;
# case 3: ...; break;
# default: ...;
# }
# Python 没有传统 C++ 风格的 switch 语法；当前使用 if/elif 最基础、最直观。
# 本例暂不使用循环，所以菜单只处理一次选择。
