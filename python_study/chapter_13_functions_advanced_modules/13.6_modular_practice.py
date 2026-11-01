# 第 13 章 函数进阶与模块基础
# 13.6 模块化编程实践
# 学习优先级：P1（重点掌握） | 掌握要求：会用
# 本文件：通过 mini_project 包演示拆分工具函数、组织业务逻辑和简单项目结构。

from mini_project import score_utils
from mini_project.report import build_report

# ==================== 13.6.1 拆分工具函数 ====================
# 通用计算放进 score_utils，业务入口只导入并调用，不在入口文件里重复实现。
scores = [78, 91, 64]
print(f"平均分：{score_utils.average(scores):.2f}")        # -> 平均分：77.67
print(f"及格率：{score_utils.pass_rate(scores):.2f}%")     # -> 及格率：100.00%
print(f"等级：{score_utils.grade(78)}")                    # -> 等级：C
# // C++: 通常把工具函数声明在头文件、实现放在源文件；Python 用模块文件直接组织函数。

# ==================== 13.6.2 组织业务逻辑 ====================
# 业务入口负责准备数据、调用包内函数、决定输出方式，本身不含计算细节。
def find_failing(scores: list[int], passing: int = 60) -> list[int]:
    """业务侧补充：找出所有不及格分数。"""
    return [score for score in scores if score < passing]

scores = [78, 91, 64, 52, 88]
print(build_report(scores))
# 输出十行：
# 成绩报表
# ----------------------------
# 第 1 位    78  C
# 第 2 位    91  A
# 第 3 位    64  C
# 第 4 位    52  D
# 第 5 位    88  B
# ----------------------------
# 平均分：74.60
# 及格率：80.00%

print(f"不及格分数：{find_failing(scores)}")        # -> 不及格分数：[52]

# build_report 返回字符串，调用方可以选择打印或写入文件；
# 报表排版只改 report.py，统计口径只改 score_utils.py，职责边界清晰。
# // C++: 对应“工具函数库 + 业务主程序”的分层，入口只负责流程编排。

# ==================== 13.6.3 简单项目目录初步 ====================
# chapter_13_functions_advanced_modules/
#   13.6_modular_practice.py    业务入口：准备数据、调用包、输出结果
#   mini_project/
#     __init__.py               标记目录为包，导入包时先执行
#     score_utils.py            纯计算工具，不打印、不依赖业务
#     report.py                 报表排版，依赖 score_utils
# 入口文件导入的是包，而不是单个文件：
# from mini_project import score_utils       导入包内的模块对象
# from mini_project.report import build_report   从包内模块导入具体函数
# 运行脚本时脚本所在目录会自动加入 sys.path[0]，所以无论从哪个工作目录运行都能找到 mini_project。
# 若项目更大，可把入口文件移出包外，再用 python -m 包.模块 的方式运行。

# 常见坑点：
# 1. 把入口文件放进包里，又用 python 直接运行它。
#    现象：from mini_project import ... 抛出 ModuleNotFoundError。
#    原因：直接运行时 sys.path[0] 是包内目录，找不到上一级的包名。
#    正确做法：入口文件放在包外，或用 python -m mini_project.report 运行。
# 2. 包内模块使用 from score_utils import average 这样的绝对导入。
#    现象：导入 report 时报找不到 score_utils。
#    原因：绝对导入按顶层模块名查找，包内模块不会自动出现在顶层。
#    正确做法：包内使用相对导入 from .score_utils import ...。
# 3. 工具函数、报表函数和业务代码全部写在一个文件里。
#    现象：文件越来越长，统计规则变化时容易改到排版代码。
#    原因：没有按“计算、展示、流程”分层。
#    正确做法：按职责拆成模块，入口文件只负责编排。
# 4. 修改包内代码后直接重新导入，发现仍是旧行为。
#    现象：输出与新代码不一致。
#    原因：sys.modules 缓存了已导入的模块对象。
#    正确做法：重启解释器，或在交互环境中用 importlib.reload。
# 5. 让工具模块依赖业务数据，例如在 score_utils 里读取固定的班级列表。
#    现象：工具函数无法复用于其他数据源。
#    原因：数据来源写死在工具层。
#    正确做法：数据通过参数传入，工具层只处理传入的内容。
