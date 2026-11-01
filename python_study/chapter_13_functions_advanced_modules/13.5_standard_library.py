# 第 13 章 函数进阶与模块基础
# 13.5 常用标准库入门
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：学习 math、random 和 datetime 三个常用标准库，并保证输出结果可复现。

import math

# ==================== 13.5.1 math ====================
# math 提供浮点数学函数和常量，结果都是平台一致的数值。
print(f"pi = {math.pi:.4f}")                     # -> pi = 3.1416
print(f"sqrt(144) = {math.sqrt(144)}")           # -> sqrt(144) = 12.0
print(f"ceil(3.2) = {math.ceil(3.2)}")           # -> ceil(3.2) = 4
print(f"floor(3.8) = {math.floor(3.8)}")         # -> floor(3.8) = 3
print(f"两点距离 = {math.hypot(3, 4)}")          # -> 两点距离 = 5.0

# 实际场景：圆柱形储罐的容积估算。
radius = 2.5
height = 6.0
volume = math.pi * radius ** 2 * height
print(f"储罐容积：{volume:.2f}")                 # -> 储罐容积：117.81
# // C++: 需要 #include <cmath>，调用 std::sqrt、std::ceil、std::floor，常量用 M_PI 或自定义。

# ==================== 13.5.2 random ====================
# random 产生伪随机数；固定种子后序列完全可复现，便于教学和测试。
import random

random.seed(2026)
print(f"抽取奖品：{random.choice(['水杯', '笔记本', '键盘'])}")    # -> 抽取奖品：水杯
print(f"骰子点数：{random.randint(1, 6)}")                        # -> 骰子点数：3
print(f"抽样名单：{random.sample(['甲', '乙', '丙', '丁'], 2)}")   # -> 抽样名单：['甲', '丁']

names = ["甲", "乙", "丙"]
random.shuffle(names)
print(f"打乱后：{names}")                                        # -> 打乱后：['甲', '乙', '丙']
# 不设种子时每次运行结果不同；需要可复现就调用 random.seed(固定值)。
# random 不适合生成密码、令牌等安全用途，安全场景应使用 secrets 模块。
# // C++: 对应 <random> 中的 std::mt19937 与分布类，同样可以设置种子复现序列。

# ==================== 13.5.3 datetime ====================
# 用固定日期构造对象，而不是读取当前时间，保证每次运行输出一致。
from datetime import date, datetime, timedelta

bill_date = date(2026, 3, 15)
due_date = bill_date + timedelta(days=20)
print(f"账单日：{bill_date}")                    # -> 账单日：2026-03-15
print(f"到期日：{due_date}")                     # -> 到期日：2026-04-04
print(f"到期日星期序号：{due_date.weekday()}")   # -> 到期日星期序号：5
# weekday() 以周一为 0，因此 5 表示周六。

days_left = (date(2026, 12, 31) - bill_date).days
print(f"距年底天数：{days_left}")                # -> 距年底天数：291

created = datetime(2026, 5, 1, 9, 30)
print(f"创建时间：{created}")                    # -> 创建时间：2026-05-01 09:30:00
print(f"格式化日期：{created.strftime('%Y/%m/%d')}")    # -> 格式化日期：2026/05/01
# 真实项目里才用 datetime.now() 读取当前时间；教学文件用固定值避免结果随运行时间变化。
# // C++: 对应 <chrono> 中的 time_point 与日期库；格式化需要额外库或手动拼接。

# 常见坑点：
# 1. 直接写 from math import * 或 from random import *。
#    现象：sqrt、choice 等名字铺满命名空间，容易与自定义函数重名。
#    原因：星号导入会引入模块的全部公开名字。
#    正确做法：使用 import math 后写 math.sqrt，或只导入需要的名字。
# 2. 使用随机数却没有设置种子。
#    现象：每次运行输出不同，测试和教学无法对比结果。
#    原因：random 默认用系统状态初始化种子。
#    正确做法：需要复现时在开头调用 random.seed(固定整数)。
# 3. 用 random 生成密码、验证码或令牌。
#    现象：随机序列可被预测，存在安全风险。
#    原因：random 是伪随机数生成器，不适合安全用途。
#    正确做法：改用 secrets 模块提供的安全随机函数。
# 4. 用 datetime.now() 或 date.today() 直接生成演示数据。
#    现象：输出随运行日期变化，今天的“到期日”明天就不同。
#    原因：读取了系统当前时间。
#    正确做法：用 date(2026, 3, 15) 这类固定日期构造对象。
# 5. 把日期当字符串做加减。
#    现象："2026-03-15" + 20 抛出 TypeError。
#    原因：字符串没有日期语义。
#    正确做法：先用 date 构造对象，再用 timedelta 计算，最后按需格式化。
