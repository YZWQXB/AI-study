# 第 14 章 文件操作
# 14.4 上下文管理基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：理解 with 语句的释放时机，掌握异常路径下的资源回收，并与 C++ RAII 对照。

from pathlib import Path
from contextlib import suppress
import tempfile


class SectionLogger:
    """记录任务进入与退出标记的上下文管理器。"""

    def __init__(self, path: Path) -> None:
        self.path = path

    def __enter__(self):
        self.handle = self.path.open("a", encoding="utf-8")
        self.handle.write("[进入任务]\n")
        return self.handle

    def __exit__(self, exc_type, exc_value, traceback_obj) -> bool:
        self.handle.write("[退出任务]\n")
        self.handle.close()
        name = exc_type.__name__ if exc_type else "None"
        print("  __exit__ 收到的异常：", name)
        return False


with tempfile.TemporaryDirectory() as temp_dir:
    # ==================== 14.4.1 with 语句 ====================
    # with 进入代码块时获取资源，离开时保证释放；异常也走同一条退出路径。
    report_path = Path(temp_dir) / "report.txt"
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("月度报表草稿\n")
    print("离开 with 后 closed：", handle.closed)                         # -> 离开 with 后 closed： True
    print("文件内容：", report_path.read_text(encoding="utf-8").strip())   # -> 文件内容： 月度报表草稿
    # // C++: 文件流离开作用域时由析构函数关闭，这就是 RAII；Python 用 with + __exit__ 达到同样效果。
    # 手动 open 想要同样安全，就必须写 try/finally，把 close() 放进 finally。
    handle = report_path.open("r", encoding="utf-8")
    try:
        first_line = handle.readline().strip()
    finally:
        handle.close()
    print("try/finally 读取：", first_line)      # -> try/finally 读取： 月度报表草稿

    # ==================== 14.4.2 自动释放资源 ====================
    # 代码块中途抛异常时，with 仍然会关闭文件，异常继续向外传播。
    try:
        with report_path.open("a", encoding="utf-8") as handle:
            handle.write("第二行\n")
            raise RuntimeError("模拟写入中出错")
    except RuntimeError as error:
        print("捕获异常：", error)                 # -> 捕获异常： 模拟写入中出错
    print("异常后文件是否关闭：", handle.closed)    # -> 异常后文件是否关闭： True
    print("异常前写入的内容：")
    print(report_path.read_text(encoding="utf-8").strip())
    # 输出：
    # 月度报表草稿
    # 第二行
    # 已写入的内容在 close() 时刷新到磁盘，不会因为后续异常而整段丢失。

    with SectionLogger(report_path) as logger_handle:
        logger_handle.write("执行数据导出\n")
    print("任务日志内容：")
    print(report_path.read_text(encoding="utf-8").strip())
    # 输出：
    # 月度报表草稿
    # 第二行
    # [进入任务]
    # 执行数据导出
    # [退出任务]
    # __enter__ 的返回值就是 as 后面的对象；这里返回文件对象，调用方才能继续写入。
    # __exit__ 返回 False 表示不吞异常；返回 True 会把异常“按下去”，调用方将看不到它。

    try:
        with SectionLogger(report_path) as logger_handle:
            logger_handle.write("执行数据清理\n")
            raise ValueError("数据不合法")
    except ValueError as error:
        print("外层捕获：", error)               # -> 外层捕获： 数据不合法
    last_line = report_path.read_text(encoding="utf-8").splitlines()[-1]
    print("出错后日志最后一行：", last_line)      # -> 出错后日志最后一行： [退出任务]
    # 即使任务失败，退出标记仍然被写入：这正是 with 在异常路径上的价值。

    with suppress(FileNotFoundError):
        (Path(temp_dir) / "no_such.txt").read_text(encoding="utf-8")
    print("suppress 之后继续执行")               # -> suppress 之后继续执行
    # suppress 等价于“__exit__ 返回 True”，只用于明确知道可以忽略的异常。
    # finally 做不到这一点：finally 里的代码无论是否出错都会执行，但异常照样向外传播。

    # ==================== 14.4.3 文件处理规范 ====================
    # with 只负责释放文件，不负责创建目录；目录不存在时要先建好。
    target = Path(temp_dir) / "exports" / "2026"
    target.mkdir(parents=True, exist_ok=True)
    (target / "summary.txt").write_text("汇总完成\n", encoding="utf-8")
    print("子目录写入成功：", (target / "summary.txt").exists())          # -> 子目录写入成功： True
    print("汇总内容：", (target / "summary.txt").read_text(encoding="utf-8").strip())   # -> 汇总内容： 汇总完成
# 规范写法：pathlib 拼路径、显式 encoding、with 管理句柄、二进制用 "rb"/"wb"、写完立即离开代码块。

# 常见坑点：
# 1. 手动 open 后在异常路径上忘记 close：句柄泄漏且缓冲区内容可能丢失；统一用 with，异常也会释放。
# 2. 在 __exit__ 里无条件 return True：异常被静默吞掉，程序看似稳定，实际掩盖了真正的错误。
# 3. 以为 __enter__ 一定返回 self：返回 self 和返回内部资源对象是两回事，as 拿到的就是 __enter__ 的返回值。
# 4. 认为 with 会自动建目录：目录不存在照样抛 FileNotFoundError，需要 Path.mkdir(parents=True, exist_ok=True)。
# 5. 把 suppress 当成通用的“忽略错误”：只应屏蔽已确认可忽略的异常，否则会漏掉需要处理的问题。
