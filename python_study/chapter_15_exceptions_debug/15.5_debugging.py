# 第 15 章 异常处理与基础调试
# 15.5 调试方法
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：练习打印调试、断点调试的写法，以及 traceback 的阅读顺序。

import traceback

scores = [78, 92, 65, 88]

# ==================== 15.5.1 打印调试 ====================
# 在可疑的环节插入带标签的 print，输出中间值，快速缩小问题范围。
def average_buggy(values: list[int]) -> float:
    total = 0
    for index in range(len(values) - 1):
        total += values[index]
    return total / len(values)

print("错误结果：", average_buggy(scores))        # -> 错误结果： 58.75

def average_traced(values: list[int]) -> float:
    print("调试：输入元素个数", len(values))
    total = 0
    for index in range(len(values) - 1):
        total += values[index]
        print(f"调试：第 {index} 轮取到 {values[index]}，累计 {total}")
    print("调试：循环结束累计", total, "分母", len(values))
    return total / len(values)

print("带调试输出的结果：", average_traced(scores))
# 输出：
# 调试：输入元素个数 4
# 调试：第 0 轮取到 78，累计 78
# 调试：第 1 轮取到 92，累计 170
# 调试：第 2 轮取到 65，累计 235
# 调试：循环结束累计 235 分母 4
# 带调试输出的结果： 58.75
# 中间值显示只累加 3 次、分母却是 4，问题就落在 range(len(values) - 1) 上。

def average_fixed(values: list[int]) -> float:
    return sum(values) / len(values)

print("修正后结果：", average_fixed(scores))      # -> 修正后结果： 80.75
# 调试用 print 要带标签和顺序信息；问题定位后应删掉，或者换成 logging 按级别输出。

# ==================== 15.5.2 断点调试 ====================
# 在可疑语句前调用 breakpoint()，程序会停在那里进入 pdb；教学文件不能等待输入，所以下面只说明写法。
# 实际用法：
# def average_with_breakpoint(values):
#     total = sum(values)
#     breakpoint()          # 停在这里，可输入 p total 观察变量、n 单步、c 继续
#     return total / len(values)
#
# 常用 pdb 命令：l 查看附近代码，p 变量名 打印变量，n 执行下一行，s 进入函数，c 继续运行，q 退出。
# 设置环境变量 PYTHONBREAKPOINT=0 可以让 breakpoint() 直接跳过，方便批量运行时临时关闭断点。
# // C++: 用 gdb 或 IDE 断点；思路一致，都是先停下来再检查变量与调用栈。

def average_with_snapshot(values: list[int]) -> float:
    total = sum(values)
    snapshot = {"total": total, "count": len(values), "result": total / len(values)}
    print("断点处的变量快照：", snapshot)
    return float(snapshot["result"])

print("快照调试结果：", average_with_snapshot(scores))
# 输出：
# 断点处的变量快照： {'total': 323, 'count': 4, 'result': 80.75}
# 快照调试结果： 80.75
# 变量快照相当于“断点那一刻看到的变量表”，没有调试器时也能达到类似效果。

# ==================== 15.5.3 Traceback 阅读 ====================
# traceback 从外到内列出调用过程，最后一行是“异常类型: 信息”，最后一条属于自己的帧最关键。
demo_source = "def parse_score(raw):\n    return int(raw)\n\nparse_score(\"九十分\")\n"
demo_code = compile(demo_source, "<演示代码>", "exec")
try:
    exec(demo_code, {})
except ValueError as error:
    tb = error.__traceback__
    if tb is not None:
        tb = tb.tb_next      # 跳过当前文件里 exec 的那一层，只保留演示代码的帧
    print("错误类型：", type(error).__name__)     # -> 错误类型： ValueError
    print("错误信息：", error)                    # -> 错误信息： invalid literal for int() with base 10: '九十分'
    print("调用链：")
    for frame in traceback.extract_tb(tb):
        print("  文件", frame.filename, "第", frame.lineno, "行，函数", frame.name)
    # 输出：
    #   文件 <演示代码> 第 4 行，函数 <module>
    #   文件 <演示代码> 第 2 行，函数 parse_score
    print("完整 traceback：")
    print("".join(traceback.format_exception(type(error), error, tb)).rstrip())
    # 输出：
    # Traceback (most recent call last):
    #   File "<演示代码>", line 4, in <module>
    #   File "<演示代码>", line 2, in parse_score
    # ValueError: invalid literal for int() with base 10: '九十分'
# 真实运行时 traceback 会带文件绝对路径；对外展示只给摘要，完整内容写进日志。
# 看到 “During handling of the above exception, another exception occurred” 就说明存在异常链：下面是新异常，上面是原始原因。

# 常见坑点：
# 1. 调试 print 不带标签：多个循环的输出混在一起分不清阶段；每行都写明阶段与序号，定位后删除。
# 2. 用 assert 代替输入校验：python -O 会移除 assert，线上校验直接失效；外部输入用显式判断加 raise。
# 3. 忘了删除 breakpoint()：批量运行时程序卡住等待输入；发布前检查，或用 PYTHONBREAKPOINT=0 关闭。
# 4. 只看 traceback 的第一行：真正结论在最后一行；应从末尾的异常类型与信息读起。
# 5. 把完整 traceback 直接展示给用户：暴露本机路径与内部结构；界面给简短提示，细节写日志。
