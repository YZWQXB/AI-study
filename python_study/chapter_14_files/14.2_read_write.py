# 第 14 章 文件操作
# 14.2 文件读写操作
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：掌握打开与关闭文件、读取文本内容、写入与追加内容的完整流程。

from pathlib import Path
import tempfile

# ==================== 14.2.1 打开与关闭文件 ====================
# open() 返回文件对象；mode 决定用途，encoding 决定字符与字节之间的转换方式。
with tempfile.TemporaryDirectory() as temp_dir:
    todo_path = Path(temp_dir) / "todo.txt"
    handle = todo_path.open("w", encoding="utf-8")
    handle.write("买牛奶\n写周报\n")
    print("关闭前 closed：", handle.closed)      # -> 关闭前 closed： False
    handle.close()
    print("关闭后 closed：", handle.closed)      # -> 关闭后 closed： True
    print("文件行数：", len(todo_path.read_text(encoding="utf-8").splitlines()))  # -> 文件行数： 2
# close() 除了释放句柄，还会把缓冲区里尚未写出的内容刷新到磁盘。
# // C++: std::ofstream 需要 close() 或等对象析构；忘记关闭同样可能丢数据。

with tempfile.TemporaryDirectory() as temp_dir:
    note_path = Path(temp_dir) / "note.txt"
    with note_path.open("w", encoding="utf-8") as handle:
        handle.write("安排一次周会\n")
    print("with 结束后 closed：", handle.closed)   # -> with 结束后 closed： True
# with 会自动调用 close()，即使代码块中途出错也会关闭（14.4 详细讲）。

# ==================== 14.2.2 读取文本内容 ====================
# Path.read_text 一次读完全部内容；行尾换行符会原样保留。
with tempfile.TemporaryDirectory() as temp_dir:
    stock_path = Path(temp_dir) / "stock.csv"
    stock_path.write_text("苹果,3\n香蕉,2\n橙子,5\n", encoding="utf-8")

    whole = stock_path.read_text(encoding="utf-8")
    print("读取整段内容：")
    print(whole, end="")
    # 输出：
    # 苹果,3
    # 香蕉,2
    # 橙子,5

    lines = stock_path.read_text(encoding="utf-8").splitlines()
    print("行数：", len(lines))        # -> 行数： 3
    print("第一行：", lines[0])        # -> 第一行： 苹果,3
# splitlines() 会去掉行尾换行符，得到干净的行列表；直接用 read_text 得到的字符串仍带 "\n"。

    with stock_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            print("原始行：", repr(line))
    # 输出：
    # 原始行： '苹果,3\n'
    # 原始行： '香蕉,2\n'
    # 原始行： '橙子,5\n'

    with stock_path.open("r", encoding="utf-8") as handle:
        print("readline 一次读一行：", handle.readline().strip())   # -> readline 一次读一行： 苹果,3
# 文件对象本身可迭代，逐行读取不会一次性把大文件全部装进内存。

    stock = {}
    for line in lines:
        name, amount = line.split(",")
        stock[name] = int(amount)
    print("库存合计：", sum(stock.values()))   # -> 库存合计： 10
# 从文本回到结构化数据：按分隔符拆分，再把字符串转成整数。

# ==================== 14.2.3 写入与追加内容 ====================
# Path.write_text 等价于 open("w")，每次调用都会整体覆盖。
with tempfile.TemporaryDirectory() as temp_dir:
    record_path = Path(temp_dir) / "record.txt"
    record_path.write_text("第一条：开始处理\n", encoding="utf-8")
    with record_path.open("a", encoding="utf-8") as handle:
        handle.write("第二条：处理完成\n")
    print("追加后内容：")
    print(record_path.read_text(encoding="utf-8"), end="")
    # 输出：
    # 第一条：开始处理
    # 第二条：处理完成

    record_path.write_text("重写后的唯一内容\n", encoding="utf-8")
    print("覆盖后内容：", record_path.read_text(encoding="utf-8").strip())   # -> 覆盖后内容： 重写后的唯一内容
# write_text 第二次调用后旧内容全部消失；想保留旧内容必须用 "a" 模式。

    log_path = Path(temp_dir) / "trade.log"
    with log_path.open("a", encoding="utf-8") as handle:
        for message in ("买入 100 股", "卖出 60 股", "查询持仓"):
            handle.write(message + "\n")
    print("日志行数：", len(log_path.read_text(encoding="utf-8").splitlines()))   # -> 日志行数： 3
# 在循环外打开文件、循环内只做写入，比每轮反复打开关闭更节省资源。

    try:
        log_path.read_text(encoding="ascii")
    except UnicodeDecodeError as error:
        print("用 ascii 读取中文日志：", type(error).__name__)   # -> 用 ascii 读取中文日志： UnicodeDecodeError
# 读取时的 encoding 必须与写入时一致，否则抛 UnicodeDecodeError；正确写法是继续用 "utf-8"。

# 常见坑点：
# 1. 只 write() 不 close() 就以为数据已落盘：缓冲区可能还没刷新，程序异常退出时内容会丢失；用 with 或显式 close()。
# 2. 读到的行带着 "\n" 拿去比较或转换，导致结果不对；先 splitlines() 或 strip() 再处理。
# 3. 想修改文件中间某一行却用 "a" 模式：追加只能写在末尾；改写要读入全部内容后重新写回。
# 4. 以为 write_text 是追加：它每次都覆盖，追加必须 open("a")。
# 5. 文本模式读写二进制数据：会出现乱码或 UnicodeDecodeError；二进制用 "rb"/"wb" 与 read_bytes/write_bytes。
