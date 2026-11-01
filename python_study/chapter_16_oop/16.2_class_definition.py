# 第 16 章 面向对象基础
# 16.2 类的定义与使用
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件学习类的语法、属性与方法的写法，以及 self 为什么必须显式出现在参数列表里。

# ==================== 16.2.1 类的基本语法 ====================
# class 类名: 后面跟缩进的类体；类体不能为空，暂时没内容就写 pass。
class Book:
    pass


reading_book = Book()
reading_book.title = "Python 编程导论"      # 给这个对象挂属性
reading_book.author = "张老师"
print(reading_book.title)                                    # -> Python 编程导论
print(reading_book.author)                                   # -> 张老师
print(isinstance(reading_book, Book))                        # -> True
# // C++: struct 的成员必须在编译期声明；Python 允许运行时给对象添加属性。
# 访问不存在的属性会抛 AttributeError，不会自动补一个默认值。
try:
    print(reading_book.price)            # 这一行会抛出 AttributeError，不产生输出
except AttributeError as error:
    print(type(error).__name__)                              # -> AttributeError
# 命名约定：类名 PascalCase，变量与方法名 snake_case。

# ==================== 16.2.2 属性与方法 ====================
# 定义在类里的函数叫方法；方法通过对象调用，读写的是“这个对象”的属性。
class Course:
    def summary(self) -> str:
        return f"{self.name}：{self.hours} 学时，主讲 {self.teacher}"

    def add_hours(self, hours: int) -> None:
        self.hours += hours             # 修改调用它的那个对象的属性


data_structure = Course()
data_structure.name = "数据结构"
data_structure.hours = 48
data_structure.teacher = "陈老师"
print(data_structure.summary())                              # -> 数据结构：48 学时，主讲 陈老师
data_structure.add_hours(8)
print(data_structure.summary())                              # -> 数据结构：56 学时，主讲 陈老师
# 方法和属性绑在对象上，属性名用点号访问；C++ 用 -> 或 . 访问成员。
network_course = Course()
network_course.name = "计算机网络"
network_course.hours = 32
network_course.teacher = "周老师"
print(network_course.summary())                              # -> 计算机网络：32 学时，主讲 周老师
print(data_structure.hours)                                  # -> 56
# 同一个类的两个对象各自保存状态，互不干扰。

# ==================== 16.2.3 self 的含义 ====================
# self 就是“调用这个方法的对象”，等价于 C++ 成员函数里的 this；
# 区别是 C++ 的 this 是隐式参数，Python 必须把它写在参数列表第一位。
print(Course.summary(data_structure))                        # -> 数据结构：56 学时，主讲 陈老师
print(data_structure.summary())                              # -> 数据结构：56 学时，主讲 陈老师
# 两种写法完全等价，第二种是语法糖：解释器自动把对象塞进 self。
print(Course.summary(data_structure) == data_structure.summary())   # -> True


class Payment:
    def set_amount(self, amount: float) -> None:
        self.amount = amount            # 写入的是当前对象的属性

    def describe(self) -> str:
        return f"支付 {self.amount:.2f} 元"


first_payment = Payment()
second_payment = Payment()
first_payment.set_amount(128.5)
second_payment.set_amount(36.0)
print(first_payment.describe())                              # -> 支付 128.50 元
print(second_payment.describe())                             # -> 支付 36.00 元
# 同一个方法，self 分别指向不同的对象，因此读到不同的状态。
# 漏写 self 时，解释器仍然会把对象作为第一个实参传进去，于是参数数量对不上。
class BrokenBook:
    def summary():                      # 故意漏写 self
        return "无 self 的方法"


try:
    BrokenBook().summary()
except TypeError as error:
    print(type(error).__name__)                              # -> TypeError
# // C++: 成员函数不写 this 也能编译通过；Python 里方法不带 self 是运行期才暴露的错误。
# self 不是关键字，写成 this 也能跑，但会让所有人阅读时代价变大，永远用 self。

# 常见坑点：
# 1. 现象：调用实例方法报 TypeError: takes 0 positional arguments but 1 was given；
#    原因：定义时漏写 self；做法：实例方法的第一个参数固定写 self。
# 2. 现象：Course.summary() 报缺少参数；原因：通过类名调用方法不会自动传对象；
#    做法：写 course.summary() 或 Course.summary(course)。
# 3. 现象：方法里改了属性，对象却没变化；原因：写成局部变量 name = "新值"；
#    做法：明确写 self.name = "新值"。
# 4. 现象：一访问属性就 AttributeError；原因：对象没有初始化过这个属性；
#    做法：在 __init__ 里统一初始化（见 16.3）。
# 5. 现象：给对象赋值时属性名拼错，程序不报错但读不到值；原因：Python 会顺手新建
#    一个同名属性；做法：属性名集中初始化，必要时用 __slots__ 限制（见 16.5）。
