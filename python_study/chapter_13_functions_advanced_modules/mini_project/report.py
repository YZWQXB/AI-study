# 第 13 章 函数进阶与模块基础
# 13.6 模块化编程实践（mini_project 包）
# 学习优先级：P1（重点掌握） | 掌握要求：会用
# 本文件：报表生成模块，负责把 score_utils 的计算结果组织成文本。

"""报表生成：依赖 score_utils 的统计结果，只负责排版与拼接文本。"""

if __package__:          # 被包导入时使用相对导入，能找到同包的 score_utils
    from .score_utils import average, grade, pass_rate
else:                    # 直接运行本文件时没有父包，退回到同目录导入
    from score_utils import average, grade, pass_rate


def build_report(scores: list[int], title: str = "成绩报表") -> str:
    """返回多行报表文本，包含每位学生的分数、等级和整体统计。"""
    lines = [title, "-" * 28]
    for index, score in enumerate(scores, start=1):
        lines.append(f"第 {index} 位  {score:>4}  {grade(score)}")
    lines.append("-" * 28)
    lines.append(f"平均分：{average(scores):.2f}")
    lines.append(f"及格率：{pass_rate(scores):.2f}%")
    return "\n".join(lines)


# 常见坑点：
# 1. 在包里使用 from score_utils import ... 而不是相对导入。
#    现象：作为包导入时抛出 ModuleNotFoundError。
#    原因：绝对导入会按顶层模块名查找，包内的 score_utils 不会被找到。
#    正确做法：包内模块之间使用 from .score_utils import ... 的形式。
# 2. 报表模块自己重复实现平均分和及格率。
#    现象：两套计算逻辑，口径逐渐不一致。
#    原因：没有复用 score_utils。
#    正确做法：统计逻辑集中在 score_utils，报表只调用它。
# 3. 报表函数直接 print，而不是返回字符串。
#    现象：无法把报表写入文件或发送到其他输出端。
#    原因：输出方式被写死。
#    正确做法：返回拼接好的字符串，由调用方决定打印还是保存。
