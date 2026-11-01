# 第 16 章 面向对象基础
# 16.3 对象的创建与初始化
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件学习实例化过程、__init__ 的职责、状态初始化的默认参数陷阱以及 __repr__ 的作用。

# ==================== 16.3.1 实例化对象 ====================
# 类名加括号就是实例化：每次调用都新建一个独立对象。
class Product:
    pass


keyboard = Product()
print(type(keyboard).__name__)                               # -> Product
print(isinstance(keyboard, Product))                         # -> True
first_copy = Product()
second_copy = Product()
first_copy.name = "机械键盘"
second_copy.name = "无线鼠标"
print(first_copy.name, second_copy.name)                     # -> 机械键盘 无线鼠标
# // C++: Product keyboard; 在栈上直接构造一个对象，两者在“每调用一次得到新对象”上一致。
# 只写类名不加括号拿到的是类本身，不是实例。
print(Product.__name__, isinstance(Product, Product))        # -> Product False

# ==================== 16.3.2 __init__() ====================
# __init__ 在对象创建后立刻被自动调用，职责只有一件事：给实例属性赋初值。
# 对象本身由 __new__ 创建，所以 __init__ 不是 C++ 意义上的构造函数，且必须返回 None。
class Product:
    def __init__(self, name: str, price: float, stock: int = 0) -> None:
        if price <= 0:
            raise ValueError(f"单价必须大于 0，当前为 {price}")
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price:.2f}, stock={self.stock})"


keyboard = Product("机械键盘", 299.0, 12)
mouse = Product("无线鼠标", 79.5)              # 使用默认参数 stock=0
print(keyboard)                                              # -> Product(name='机械键盘', price=299.00, stock=12)
print(mouse)                                                 # -> Product(name='无线鼠标', price=79.50, stock=0)
print(type(keyboard) is Product)                             # -> True
# 参数顺序与默认值：有默认值的参数必须放在没有默认值的参数后面。
# // C++: 默认实参同样写在声明里，但 C++ 的默认值每次调用单独求值，Python 只求值一次。
# 显式传入非法参数时，__init__ 里的校验会立刻中断创建，对象不会半成品地留下来。
try:
    Product("显示器", -1099.0)
except ValueError as error:
    print(type(error).__name__)                              # -> ValueError
# 若 __init__ 里写了 return 数值，实例化会直接报 TypeError: __init__() should return None。

# ==================== 16.3.3 对象状态初始化与默认参数陷阱 ====================
# 默认参数在“函数定义时”求值一次，可变默认值就会被所有实例共享，这是最典型的坑。
class OrderBad:
    def __init__(self, items: list[str] = []) -> None:       # 错误写法
        self.items = items


bad_first = OrderBad()
bad_second = OrderBad()
bad_first.items.append("Python 编程导论")
print(bad_second.items)                                      # -> ['Python 编程导论']
print(bad_first.items is bad_second.items)                   # -> True
# 两个订单指向同一个列表，一个订单加书，另一个也“自动”多了一本。
class Order:
    def __init__(self, items: list[str] | None = None) -> None:
        self.items = list(items) if items else []            # 每个实例拿到独立列表

    def add(self, title: str) -> None:
        self.items.append(title)

    def __repr__(self) -> str:
        return f"Order(items={self.items!r})"


first_order = Order()
second_order = Order()
first_order.add("Python 编程导论")
print(first_order.items)                                     # -> ['Python 编程导论']
print(second_order.items)                                    # -> []
print(first_order.items is second_order.items)               # -> False
print(repr(first_order))                                     # -> Order(items=['Python 编程导论'])
# // C++: 默认实参每次调用重新求值，不会出现跨对象共享；Python 必须用 None 占位。
# 不写 __repr__ 时，print(keyboard) 只能输出 <__main__.Product object at 0x...>，
# 其中的内存地址每次都不同，无法用于对照输出；自定义 __repr__ 才能稳定可读。
# 记住分工：__init__ 负责状态初始化，__repr__ 负责给人看的字符串表示。

# 常见坑点：
# 1. 现象：两个对象莫名其妙共享同一个列表；原因：可变默认参数 items: list = []；
#    做法：默认值写 None，在函数体内创建新列表。
# 2. 现象：实例化时报 TypeError: __init__() should return None；原因：__init__ 里写了
#    return 数值；做法：__init__ 只赋值，需要返回对象交给 __new__。
# 3. 现象：属性拼写错误后才在别处报 AttributeError；原因：没有统一初始化；
#    做法：所有实例属性都在 __init__ 中赋初值，可给默认值。
# 4. 现象：print(对象) 输出带 0x 地址的字符串，无法对照；原因：没有 __repr__；
#    做法：实现 __repr__，用 f-string 和 !r 输出可读内容。
# 5. 现象：直接给实例属性赋值绕过业务校验，例如 product.price = -5；原因：只在 __init__
#    校验；做法：把校验放进方法，并用 @property 控制写入口（见 16.4、16.6）。
