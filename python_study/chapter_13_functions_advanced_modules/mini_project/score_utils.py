# 第 13 章 函数进阶与模块基础
# 13.6 模块化编程实践（mini_project 包）
# 学习优先级：P1（重点掌握） | 掌握要求：会用
# 本文件：成绩统计工具函数，只负责计算，不打印也不依赖具体业务。

"""成绩统计工具：平均分、及格率与等级判断。"""


def average(scores: list[int]) -> float:
    """返回平均分并保留两位小数；空列表返回 0.0。"""
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def pass_rate(scores: list[int], passing: int = 60) -> float:
    """返回及格率，用 0 到 100 的百分数值表示；空列表返回 0.0。"""
    if not scores:
        return 0.0
    passed = sum(1 for score in scores if score >= passing)
    return round(passed / len(scores) * 100, 2)


def grade(score: int) -> str:
    """按分数返回等级 A、B、C、D。"""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 60:
        return "C"
    return "D"


# 常见坑点：
# 1. 在工具函数里直接 print。
#    现象：报表和测试都需要重新解析输出文本。
#    原因：工具函数承担了展示职责。
#    正确做法：只 return 数值，由 report 模块负责格式化。
# 2. 除零前没有检查空列表。
#    现象：传入空列表时抛出 ZeroDivisionError。
#    原因：len(scores) 为 0 时仍然做除法。
#    正确做法：先判断 if not scores，返回约定的 0.0。
# 3. 把等级划分的阈值散落在多个函数中。
#    现象：调整及格线时只改了一处，统计结果前后矛盾。
#    原因：阈值被写成字面量。
#    正确做法：把阈值作为参数传入或提取为常量。
