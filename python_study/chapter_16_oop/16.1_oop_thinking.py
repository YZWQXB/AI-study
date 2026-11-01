# 第 16 章 面向对象基础
# 16.1 面向对象思想
# 学习优先级：P1（重点掌握） | 掌握要求：理解
# 本文件用学生成绩管理场景对比面向过程与面向对象，理解对象抽象以及类与对象的关系。

# ==================== 16.1.1 对象抽象 ====================
# 对象把“数据”和“操作这些数据的行为”收在一起；字典只装数据，处理函数必须另写。
student_record = {"name": "李明", "class_name": "三年二班", "score": 86}
print(student_record["name"], student_record["score"])       # -> 李明 86
# // C++: struct Student { std::string name; std::string class_name; double score; };


def describe(record: dict[str, object]) -> str:
    """面向过程的写法：数据放在外面，函数从外部拿数据算。"""
    return f"{record['name']} 就读 {record['class_name']}，成绩 {record['score']}"


print(describe(student_record))                              # -> 李明 就读 三年二班，成绩 86
# 这种写法能运行，但换一个学生就要记住字典的键名，行为也不会跟着数据走。
# 面向对象的第一步是“抽象”：找出一个学生真正需要的属性（姓名、班级、成绩）
# 以及真正需要的行为（描述自己、修改成绩），把它们绑定成一个整体。

# ==================== 16.1.2 类与对象的关系 ====================
# 类是模板，描述“应该有哪些属性和行为”；对象是按模板造出来的具体实例。
class Student:
    """学生模板：本小节先不写属性和方法，16.2 再补上。"""
    pass


first_student = Student()          # 实例化：按模板造出一个对象
second_student = Student()
first_student.name = "王芳"        # 给具体对象挂数据
second_student.name = "赵强"
print(type(first_student).__name__)                          # -> Student
print(first_student.name, second_student.name)               # -> 王芳 赵强
print(first_student is second_student)                       # -> False
# // C++: Student a; Student b; 两个变量各自持有一份独立的数据。
# 一个类可以创建任意多个对象，每个对象的属性互不影响。
students = [Student(), Student(), Student()]
print(len(students))                                         # -> 3
# 只写类名 Student（不加括号）得到的是类对象本身，不是某个具体学生。
print(Student.__name__, isinstance(Student, Student))        # -> Student False

# ==================== 16.1.3 面向对象与面向过程对比 ====================
# 需求：统计班级成绩的平均分，并列出及格学生的姓名。
# 面向过程做法：数据是列表里的字典，函数从参数里拿数据。
class_records = [
    {"name": "李明", "score": 86},
    {"name": "王芳", "score": 72},
    {"name": "赵强", "score": 58},
]


def average_score(records: list[dict[str, object]]) -> float:
    total = 0.0
    for record in records:
        total += record["score"]
    return total / len(records)


def passed_names(records: list[dict[str, object]], passing: int = 60) -> list[str]:
    return [record["name"] for record in records if record["score"] >= passing]


print(f"平均分：{average_score(class_records):.1f}")         # -> 平均分：72.0
print(passed_names(class_records))                           # -> ['李明', '王芳']
# 面向对象做法：把数据和行为放进同一个对象，调用方只需知道对象能做什么。
class ScoreBoard:
    def __init__(self, records: list[dict[str, object]]) -> None:
        self.records = records          # self 的详细用法见 16.2

    def average(self) -> float:
        return sum(float(record["score"]) for record in self.records) / len(self.records)

    def passed_names(self, passing: int = 60) -> list[str]:
        return [str(record["name"]) for record in self.records if record["score"] >= passing]


board = ScoreBoard(class_records)
print(f"平均分：{board.average():.1f}")                      # -> 平均分：72.0
print(board.passed_names())                                  # -> ['李明', '王芳']
print(board.passed_names(80))                                # -> ['李明']
# // C++: 面向对象版本等价于 class ScoreBoard { double average(); ... };
# // 差别在于 C++ 成员必须先声明类型，Python 的属性可以运行时挂上。
# 两者的差别不是“谁更强”，而是关注点：面向过程以步骤为中心，参数在函数之间传递；
# 面向对象以对象为中心，数据和行为绑定，调用写成 board.average()。
# 后续小节会补上：self（16.2）、初始化（16.3）、封装与继承（16.4）、类级别能力（16.5）。

# 常见坑点：
# 1. 现象：print(Student.name) 报 AttributeError；原因：属性挂在了实例上而不是类上；
#    做法：先用 Student() 创建对象，再对对象赋值。
# 2. 现象：以为 Student 就是对象；原因：混淆类对象与实例；做法：类由 class 定义，
#    实例由 Student() 创建，可以用 isinstance 判断。
# 3. 现象：把类写成一个“函数集合”，函数之间靠全局变量传递数据；原因：只搬代码没做抽象；
#    做法：先确定对象的属性，再把修改这些属性的行为放进同一个类。
# 4. 现象：类名写成 student 或 Studentclass；原因：没遵守命名约定；做法：类名用
#    PascalCase（如 Student、ScoreBoard），函数与变量用 snake_case。
# 5. 现象：两个对象改了同一个值；原因：误以为同类对象共享状态；做法：状态写在实例属性上，
#    只有确实需要共享的数据才放到类属性（见 16.5）。
