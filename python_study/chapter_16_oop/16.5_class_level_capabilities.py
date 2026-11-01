# 第 16 章 面向对象基础
# 16.5 类级别能力
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件学习类属性、classmethod、staticmethod，以及 __slots__ 和 dataclass(slots=True)。

from dataclasses import dataclass

# ==================== 16.5.1 类属性 ====================
# 类属性定义在类体中、方法之外，由所有实例共享；实例属性写在 __init__ 里，各自独立。
class Ticket:
    tax_rate = 0.06            # 类属性：所有票共享的税率
    issued_count = 0           # 类属性：发出去的票数

    def __init__(self, price: float) -> None:
        self.price = price               # 实例属性：每张票不同
        Ticket.issued_count += 1         # 必须写类名，写 self 会新建实例属性

    def final_price(self) -> float:
        return round(self.price * (1 + self.tax_rate), 2)


first_ticket = Ticket(100.0)
second_ticket = Ticket(200.0)
print(f"{first_ticket.final_price():.2f}")                   # -> 106.00
print(f"{second_ticket.final_price():.2f}")                  # -> 212.00
print(Ticket.issued_count)                                   # -> 2
print(first_ticket.__dict__)                                 # -> {'price': 100.0}
# 修改类属性会影响所有实例，因为实例查不到该名字时会回到类里找。
Ticket.tax_rate = 0.08
print(f"{first_ticket.final_price():.2f}")                   # -> 108.00
print(f"{second_ticket.final_price():.2f}")                  # -> 216.00
# 通过实例赋值不会改类属性，而是新建一个同名实例属性把它“遮住”。
first_ticket.tax_rate = 0.10
print(first_ticket.tax_rate, Ticket.tax_rate)                # -> 0.1 0.08
print(first_ticket.__dict__)                                 # -> {'price': 100.0, 'tax_rate': 0.1}
# final_price 里读的是 self.tax_rate，属性查找先找实例，所以这张票按 0.10 计算。
print(f"{first_ticket.final_price():.2f}")                   # -> 110.00
# // C++: 静态成员变量属于类，用 Ticket::taxRate 访问，修改后所有对象看到新值；
# // Python 的 look-up 先实例后类，所以实例赋值会遮蔽类属性。

# ==================== 16.5.2 类方法 ====================
# @classmethod 的第一个参数是类本身（约定命名 cls），常用于提供第二种创建方式。
class Member:
    def __init__(self, name: str, level: str) -> None:
        self.name = name
        self.level = level

    @classmethod
    def from_text(cls, text: str) -> "Member":
        name, level = text.split("/")
        return cls(name, level)          # cls 指向实际调用的类，子类调用也返回子类实例

    @classmethod
    def default_level(cls) -> str:
        return "普通会员"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, level={self.level!r})"


member = Member.from_text("李明/黄金会员")
print(member)                                                # -> Member(name='李明', level='黄金会员')
print(Member.default_level())                                # -> 普通会员


class StudentMember(Member):
    pass


student_member = StudentMember.from_text("王芳/学生会员")
print(student_member)                                        # -> StudentMember(name='王芳', level='学生会员')
print(type(student_member).__name__)                         # -> StudentMember
# 工厂方法里写死 Member(...) 就丢了多态性，子类调用会拿到父类实例。
# // C++: 没有 cls 这个概念，通常用静态工厂函数并显式写类名，或用模板参数传递类型。

# ==================== 16.5.3 静态方法 ====================
# @staticmethod 既不接收 self 也不接收 cls，只是挂在类命名空间里的普通函数。
class Coupon:
    prefix = "CP"

    def __init__(self, code: str) -> None:
        if not Coupon.is_valid_code(code):
            raise ValueError(f"优惠码格式错误：{code}")
        self.code = code

    @staticmethod
    def is_valid_code(code: str) -> bool:
        return len(code) == 6 and code.startswith(Coupon.prefix) and code[2:].isalnum()

    def __repr__(self) -> str:
        return f"Coupon(code={self.code!r})"


print(Coupon.is_valid_code("CP2024"))                        # -> True
print(Coupon.is_valid_code("CP24"))                          # -> False
print(Coupon("CP2024"))                                      # -> Coupon(code='CP2024')
print(Coupon("CP2024").is_valid_code("CP8A21"))              # -> True
try:
    Coupon("XX2024")
except ValueError as error:
    print(error)                                             # -> 优惠码格式错误：XX2024
# 工具函数与类强相关但不需要对象状态时用 staticmethod；它能被导入、被测试，也不会误用 self。
# // C++: 对应类的静态成员函数，调用写法一致（Coupon::is_valid_code("CP2024")）。

# ==================== 16.5.4 __slots__ 与 dataclass 精简写法 ====================
# __slots__ 限定实例只能拥有列出的属性，拼错属性名会立刻报错，也省掉 __dict__。
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


point = Point(3, 4)
print(point.x, point.y)                                      # -> 3 4
try:
    point.z = 5                                  # 拼错的属性名会被拒绝
except AttributeError as error:
    print(type(error).__name__)                              # -> AttributeError
print(hasattr(point, "__dict__"))                            # -> False
# dataclass 自动生成 __init__、__repr__ 和 __eq__，适合“主要用来装数据”的类。
@dataclass(slots=True)
class Book:
    title: str
    price: float
    stock: int = 0

    def total_value(self) -> float:
        return round(self.price * self.stock, 2)


book = Book("Python 编程导论", 59.0, 20)
print(book)                                                  # -> Book(title='Python 编程导论', price=59.0, stock=20)
print(Book("C 语言程序设计", 45.0))                          # -> Book(title='C 语言程序设计', price=45.0, stock=0)
print(f"{book.total_value():.2f}")                           # -> 1180.00
print(hasattr(book, "__dict__"))                             # -> False
# // C++: 相当于写了一个带构造函数的 struct，并自动补齐打印与相等比较；
# // slots=True 对应“不允许多余成员”，但代价是不能动态添加属性。

# 常见坑点：
# 1. 现象：计数器一直是 0 或每次都从 1 开始；原因：写成 self.issued_count += 1，
#    给实例新建了同名属性；做法：写 类名.issued_count += 1。
# 2. 现象：给一个对象改类属性后，另一个对象没变；原因：obj.tax_rate = 0.1 只遮蔽实例；
#    做法：要改共享配置就写 Ticket.tax_rate = 0.1。
# 3. 现象：classmethod 里没有 cls，或 staticmethod 里多写了 self；原因：两种装饰器语义混用；
#    做法：类方法固定 (cls, ...)，静态方法就是普通参数列表。
# 4. 现象：子类调用工厂方法却得到父类实例；原因：方法里写死返回 Member(...)；
#    做法：返回 cls(...)，让实际类决定实例类型。
# 5. 现象：加 __slots__ 后代码报 AttributeError，或子类无法再加属性；原因：slots 限定字段；
#    做法：只对有固定字段的类使用，需要额外字段时不要加 slots。
