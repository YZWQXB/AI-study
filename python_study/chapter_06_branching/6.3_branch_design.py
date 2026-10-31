# 第 6 章 分支结构
# 6.3 分支设计方法
# 本文件学习多条件组合、嵌套分支和守卫式判断。

# ==================== 6.3.1 多条件组合判断 ====================
# and：两边都为真才为真；or：至少一边为真；not：把真值反转。
age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("年龄和票证都满足，允许入场")
else:
    print("入场条件不满足")
# C++ 对比：Python and 对应 C++ &&。
# if (age >= 18 && has_ticket) { ... }

is_weekend = True
is_holiday = False
if is_weekend or is_holiday:
    print("今天可以休息")
# C++ 对应：if (is_weekend || is_holiday) { ... }

is_locked = False
if not is_locked:
    print("账户当前未锁定")
# C++ 对应：if (!is_locked) { ... }
# Python 使用英文单词 and/or/not；不要写 &&、||、!。

# ==================== 6.3.2 嵌套分支 ====================
# 外层条件成立后，才会继续判断内层条件。
account_enabled = True
password_correct = False
if account_enabled:
    print("账户状态正常")
    if password_correct:
        print("登录成功")
    else:
        print("密码不正确")
else:
    print("账户已停用")
# C++ 通过花括号嵌套表示同样关系：
# if (account_enabled) {
#     if (password_correct) { ... }
#     else { ... }
# } else { ... }
# Python 通过增加缩进表示内层；内层 if 必须比外层多缩进一级。

# 嵌套层数不宜过深，否则不易阅读；先写清楚条件归属。
member = True
age = 16
if member:
    if age < 18:
        print("会员中的未成年人")
    else:
        print("会员中的成年人")
else:
    print("非会员")

# ==================== 6.3.3 守卫式判断初步 ====================
# 先处理不满足前置条件的情况，让后面的正常路径更清楚。
stock = 0
requested = 3
if requested <= 0:
    print("购买数量必须大于 0")
elif stock <= 0:
    print("商品暂时缺货")
elif requested > stock:
    print("库存不足")
else:
    print("可以完成购买")
# 这是当前章节中的“守卫式”思想：先排除不合法或不能继续的情况。
# C++ 可以使用 if / else if / else 写同样结构。
# 在后续函数章节中，守卫式判断经常写成“条件不满足就 return”；本文件暂不引入函数。

# 练习：依次修改 requested 和 stock，观察哪一个条件会最先被处理。
