# 第 16 章 面向对象基础
# 16.6 基础对象建模案例
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件用学生、商品、银行账户三个真实场景，练习校验、业务方法与只读属性。

# ==================== 16.6.1 学生类设计 ====================
# 建模要点：属性私有化（_scores）、修改走业务方法、对外只读、非法成绩立刻拒绝。
class Student:
    def __init__(self, student_id: str, name: str) -> None:
        self.student_id = student_id
        self.name = name
        self._scores: list[int] = []

    @property
    def scores(self) -> list[int]:
        return list(self._scores)            # 返回副本，外部改动影响不到内部状态

    def add_score(self, score: int) -> None:
        if not 0 <= score <= 100:
            raise ValueError(f"成绩必须在 0 到 100 之间，当前为 {score}")
        self._scores.append(score)

    @property
    def average(self) -> float:
        if not self._scores:
            return 0.0                       # 没有成绩时不要除零
        return sum(self._scores) / len(self._scores)

    @property
    def is_passed(self) -> bool:
        return self.average >= 60

    def __repr__(self) -> str:
        return f"Student(id={self.student_id!r}, name={self.name!r}, scores={self._scores})"


student = Student("2024001", "李明")
student.add_score(86)
student.add_score(72)
student.add_score(58)
print(student)                                               # -> Student(id='2024001', name='李明', scores=[86, 72, 58])
print(f"{student.average:.1f}")                              # -> 72.0
print(student.is_passed)                                     # -> True
print(student.scores)                                        # -> [86, 72, 58]
# @property 让调用方写 student.average 而不是 student.average()，读起来像属性，内部是方法。
# // C++: 对应 double average() const 与 std::vector<int> scores() const。
copied_scores = student.scores
copied_scores.append(200)                                    # 改副本，内部不受影响
print(student.scores)                                        # -> [86, 72, 58]
try:
    student.add_score(120)
except ValueError as error:
    print(error)                                             # -> 成绩必须在 0 到 100 之间，当前为 120

# ==================== 16.6.2 商品类设计 ====================
# 建模要点：构造时校验单价与库存，卖出与补货都走方法，库存对外只读。
class Product:
    def __init__(self, name: str, price: float, stock: int) -> None:
        if price <= 0:
            raise ValueError(f"单价必须大于 0，当前为 {price}")
        if stock < 0:
            raise ValueError(f"库存不能为负，当前为 {stock}")
        self.name = name
        self.price = price
        self._stock = stock

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def is_available(self) -> bool:
        return self._stock > 0

    def sell(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError(f"销量必须为正整数，当前为 {quantity}")
        if quantity > self._stock:
            raise ValueError(f"{self.name} 库存不足：库存 {self._stock}，需求 {quantity}")
        self._stock -= quantity
        return round(self.price * quantity, 2)

    def restock(self, quantity: int) -> int:
        if quantity <= 0:
            raise ValueError(f"补货数量必须为正整数，当前为 {quantity}")
        self._stock += quantity
        return self._stock

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price:.2f}, stock={self._stock})"


keyboard = Product("机械键盘", 299.0, 12)
print(keyboard)                                              # -> Product(name='机械键盘', price=299.00, stock=12)
print(f"{keyboard.sell(3):.2f}")                             # -> 897.00
print(keyboard.stock)                                        # -> 9
print(keyboard.restock(5))                                   # -> 14
print(keyboard.is_available)                                 # -> True
try:
    keyboard.sell(20)
except ValueError as error:
    print(error)                                             # -> 机械键盘 库存不足：库存 14，需求 20
# 零库存的商品同样受同一套规则保护：卖不出去时给出可读的原因，而不是悄悄返回 0。
mouse = Product("无线鼠标", 79.5, 0)
print(mouse.is_available)                                    # -> False
try:
    mouse.sell(2)
except ValueError as error:
    print(error)                                             # -> 无线鼠标 库存不足：库存 0，需求 2
# // C++: 业务方法返回类型要么是金额，要么抛异常；C++ 常用返回值 + 错误码，
# // Python 更倾向抛出 ValueError，让调用方无法忽略失败。

# ==================== 16.6.3 银行账户类设计 ====================
# 建模要点：余额只读、存取校验、转账复用同账户逻辑并留下可追溯的流水。
class BankAccount:
    def __init__(self, account_no: str, owner: str, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError(f"初始余额不能为负，当前为 {balance}")
        self.account_no = account_no
        self.owner = owner
        self._balance = balance
        self._records: list[str] = []

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def records(self) -> list[str]:
        return list(self._records)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"存款金额必须大于 0，当前为 {amount}")
        self._balance = round(self._balance + amount, 2)
        self._records.append(f"存款 {amount:.2f}，余额 {self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"取款金额必须大于 0，当前为 {amount}")
        if amount > self._balance:
            raise ValueError(f"余额不足：余额 {self._balance:.2f}，取款 {amount:.2f}")
        self._balance = round(self._balance - amount, 2)
        self._records.append(f"取款 {amount:.2f}，余额 {self._balance:.2f}")

    def transfer(self, target: "BankAccount", amount: float) -> None:
        if target.account_no == self.account_no:
            raise ValueError("不能向同一个账户转账")
        self.withdraw(amount)                # 复用取款逻辑，余额不足时不会动对方账户
        target.deposit(amount)
        self._records.append(f"转出 {amount:.2f} 至 {target.account_no}")

    def __repr__(self) -> str:
        return f"BankAccount(no={self.account_no!r}, owner={self.owner!r}, balance={self._balance:.2f})"


payer = BankAccount("622201", "王芳", 1200.0)
payee = BankAccount("622202", "赵强", 300.0)
payer.deposit(500.0)
payer.transfer(payee, 400.0)
print(payer)                                                 # -> BankAccount(no='622201', owner='王芳', balance=1300.00)
print(payee)                                                 # -> BankAccount(no='622202', owner='赵强', balance=700.00)
print(payer.records)                                         # -> ['存款 500.00，余额 1700.00', '取款 400.00，余额 1300.00', '转出 400.00 至 622202']
print(payee.records)                                         # -> ['存款 400.00，余额 700.00']
# 转账复用了 withdraw，因此付款方流水会同时留下“取款”和“转出”两条记录；
# 真实系统通常把流水设计成带类型字段的结构，这里用字符串保持示例简洁。
try:
    payer.withdraw(5000.0)
except ValueError as error:
    print(error)                                             # -> 余额不足：余额 1300.00，取款 5000.00
try:
    payer.transfer(payer, 100.0)
except ValueError as error:
    print(error)                                             # -> 不能向同一个账户转账

# 常见坑点：
# 1. 现象：student._scores.append(120) 不报错，非法数据进了对象；原因：绕过业务方法；
#    做法：所有修改都走 add_score / sell / deposit，并保持下划线约定。
# 2. 现象：返回 student._scores 后外部一改内部也变；原因：直接暴露可变对象；
#    做法：@property 里返回 list(...) 副本。
# 3. 现象：校验只写在 __init__，后续操作又能把状态弄非法；原因：校验没跟着业务方法走；
#    做法：每个修改状态的方法都独立校验参数。
# 4. 现象：余额出现 1299.9999999 之类的小数误差；原因：浮点累加；做法：金额用 round 统一
#    保留两位（工程上建议用 int 以分为单位或 decimal.Decimal）。
# 5. 现象：转账先给对方加钱再扣自己，失败时账目不平；原因：顺序与异常处理缺失；
#    做法：先校验并扣款，再入账，必要时用事务式补偿逻辑。
