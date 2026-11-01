# 第 16 章 面向对象基础
# 16.4 封装、继承与多态入门
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件用银行账户与会员场景学习命名约定、@property、继承、super() 与鸭子类型。

# ==================== 16.4.1 封装思想 ====================
# Python 没有 public/private 关键字，靠命名约定：_x 表示内部使用，__x 会触发名称改写。
# 封装的目标是：外部只通过方法改状态，方法内部统一做校验，非法值进不来。
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = balance              # 约定：外部不要直接改，走 deposit / withdraw

    @property
    def balance(self) -> float:
        return self._balance                 # 只读属性，外部用 account.balance 读取

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"存款金额必须大于 0，当前为 {amount}")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"取款金额必须大于 0，当前为 {amount}")
        if amount > self._balance:
            raise ValueError(f"余额不足：余额 {self._balance:.2f}，取款 {amount:.2f}")
        self._balance -= amount
        return self._balance


personal = BankAccount("王芳", 500.0)
print(personal.balance)                                      # -> 500.0
print(personal.deposit(200.0))                               # -> 700.0
print(personal.withdraw(150.0))                              # -> 550.0
# // C++: 通常写 double getBalance() const 与 void deposit(double); Python 用 @property
# // 让“读余额”长得像读属性，但内部仍是一段方法。
# 没有 setter 的 @property 是只读的，强行赋值会被拒绝。
try:
    personal.balance = 9999.0
except AttributeError as error:
    print(type(error).__name__)                              # -> AttributeError
# 双下划线不是“更私有”，而是会改写名字：self.__secret 变成 self._InternalState__secret。
class InternalState:
    def __init__(self) -> None:
        self.__secret = "内部数据"

    def reveal(self) -> str:
        return self.__secret


state = InternalState()
print(state.reveal())                                        # -> 内部数据
print(state._InternalState__secret)                          # -> 内部数据
# // C++: private 成员在编译期禁止访问；Python 只是改名，仍可绕过去，所以是“约定”而非锁。

# ==================== 16.4.2 继承基础 ====================
# 子类复用父类的属性与方法，用 super() 调父类实现；同名方法会覆盖父类版本。
class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.02) -> None:
        super().__init__(owner, balance)          # 父类负责初始化 owner 与 _balance
        self.rate = rate

    def add_interest(self) -> float:
        interest = round(self._balance * self.rate, 2)
        self.deposit(interest)
        return interest

    def withdraw(self, amount: float) -> float:   # 覆盖父类方法，加入手续费
        fee = round(amount * 0.01, 2)
        return super().withdraw(amount + fee)     # 复用父类的校验与扣款


savings = SavingsAccount("李明", 1000.0, 0.025)
print(savings.owner)                                         # -> 李明
print(savings.balance)                                       # -> 1000.0
print(f"{savings.add_interest():.2f}")                       # -> 25.00
print(f"{savings.balance:.2f}")                              # -> 1025.00
print(f"{savings.withdraw(100.0):.2f}")                      # -> 924.00
# 100 元取款收 1 元手续费，所以实际扣掉 101 元。
print(isinstance(savings, BankAccount))                      # -> True
# 方法查找顺序（MRO）：子类自己先找，找不到再沿父类链向上找。
print([cls.__name__ for cls in SavingsAccount.__mro__])      # -> ['SavingsAccount', 'BankAccount', 'object']
# // C++: 继承写法 class SavingsAccount : public BankAccount；多继承在 C++ 里要写虚继承，
# // Python 允许多继承并按 C3 线性化决定查找顺序。

# ==================== 16.4.3 鸭子类型与多态认知 ====================
# 多态：同一段调用代码，对不同对象执行各自的实现。
accounts = [BankAccount("赵强", 320.0), SavingsAccount("王芳", 800.0, 0.03)]
for account in accounts:
    print(f"{account.owner} 余额 {account.balance:.2f}")     # 两行输出，见下方注释块
# 输出两行：
# -> 赵强 余额 320.00
# -> 王芳 余额 800.00
# 鸭子类型：只要对象有需要的属性，就能参与运算，不必是同一个类的子类。
class Wallet:
    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner
        self.balance = balance


def show_balance(item: BankAccount | Wallet) -> str:
    return f"{item.owner} 余额 {item.balance:.2f}"


print(show_balance(Wallet("陈静", 260.0)))                    # -> 陈静 余额 260.00
print(show_balance(accounts[0]))                             # -> 赵强 余额 320.00
# 类型标注只是提示，运行时并不检查；真正的要求是“有 owner 和 balance”。
class Receipt:
    def __init__(self) -> None:
        self.total = 88.0


try:
    show_balance(Receipt())
except AttributeError as error:
    print(type(error).__name__)                              # -> AttributeError
# // C++: 运行时多态需要虚函数 + 基类指针；Python 的调用在运行时按方法名查找，
# // 因此“像鸭子一样叫就是鸭子”，代价是类型错误要到运行时才暴露。

# 常见坑点：
# 1. 现象：外部改了 _balance 后余额与流水对不上；原因：误以为单下划线是私有；
#    做法：把单下划线当约定，只通过方法修改状态，读用 @property。
# 2. 现象：子类里写 self.__x 读不到父类的 __x；原因：名称被改写为 _子类名__x；
#    做法：共享状态用单下划线，或提供方法访问。
# 3. 现象：子类调用父类方法报 AttributeError；原因：忘了 super().__init__()，父类属性没建；
#    做法：子类 __init__ 第一件事就调用 super().__init__(...)。
# 4. 现象：给只读 property 赋值抛 AttributeError: property 'balance' has no setter；
#    原因：@property 没写 setter；做法：需要外部赋值时补 @balance.setter 并做校验。
# 5. 现象：鸭子类型对象少一个属性，程序在深处才崩；原因：运行时不检查协议；
#    做法：在入口处检查必需属性，或抛出带对象信息的明确错误。
