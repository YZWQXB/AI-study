# 第 14 章 文件操作
# 14.3 文件读写模式
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：对比 r、w、a、x、b 五种模式的打开条件、覆盖与追加行为。

from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    # ==================== 14.3.1 读模式 r ====================
    # "r" 只读；文件必须已存在，否则抛 FileNotFoundError。
    data_path = Path(temp_dir) / "data.txt"
    data_path.write_text("第一版内容\n", encoding="utf-8")
    with data_path.open("r", encoding="utf-8") as handle:
        print("读模式读取：", handle.read().strip())    # -> 读模式读取： 第一版内容

    missing_path = Path(temp_dir) / "missing.txt"
    try:
        with missing_path.open("r", encoding="utf-8") as handle:
            handle.read()
    except FileNotFoundError as error:
        print("读模式打开不存在的文件：", type(error).__name__)   # -> 读模式打开不存在的文件： FileNotFoundError
# // C++: std::ifstream 打开失败时 is_open() 返回 false，不会抛异常，必须手动检查。

    # ==================== 14.3.2 写模式 w 与独占创建 x ====================
    # "w" 先清空文件再写；文件不存在则创建，因此“打开即截断”。
    with data_path.open("w", encoding="utf-8") as handle:
        handle.write("第二版内容\n")
    print("w 模式再次写入：", data_path.read_text(encoding="utf-8").strip())   # -> w 模式再次写入： 第二版内容
# 第一次的“第一版内容”已经被截断，无法从文件里找回。
# 需要保留旧内容时不能用 "w"；需要“绝不覆盖已有文件”时用 "x"。

    unique_path = Path(temp_dir) / "unique.txt"
    try:
        with unique_path.open("x", encoding="utf-8") as handle:
            handle.write("独占创建成功\n")
        print("x 模式首次创建：", "成功")            # -> x 模式首次创建： 成功
        with unique_path.open("x", encoding="utf-8") as handle:
            handle.write("重复创建\n")
    except FileExistsError as error:
        print("x 模式重复创建：", type(error).__name__)   # -> x 模式重复创建： FileExistsError

    # ==================== 14.3.3 追加模式 a ====================
    # "a" 在文件末尾追加，不清空；文件不存在时会自动创建。
    log_path = Path(temp_dir) / "app.log"
    log_path.write_text("启动服务\n", encoding="utf-8")
    for event in ("加载配置", "连接数据库"):
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(event + "\n")
    print("追加后的行数：", len(log_path.read_text(encoding="utf-8").splitlines()))   # -> 追加后的行数： 3
# 追加顺序就是写入顺序，日志文件通常用 "a" 模式维护。

    auto_path = Path(temp_dir) / "auto.txt"
    with auto_path.open("a", encoding="utf-8") as handle:
        handle.write("第一条记录\n")
    print("a 模式自动创建文件：", auto_path.exists())   # -> a 模式自动创建文件： True
# 与 "w" 不同，"a" 打开一个不存在的文件不会报错，也不会产生“截断”动作。

    # ==================== 14.3.4 二进制模式 b ====================
    # 加上 "b" 表示按字节读写，此时不能带 encoding 参数。
    photo_path = Path(temp_dir) / "photo.bin"
    with photo_path.open("wb") as handle:
        handle.write(b"\x89PNG\r\n")
    print("二进制文件大小：", photo_path.stat().st_size)   # -> 二进制文件大小： 6

    with photo_path.open("rb") as handle:
        head = handle.read(4)
    print("前四个字节：", head)                  # -> 前四个字节： b'\x89PNG'
    try:
        photo_path.open("rb", encoding="utf-8")
    except ValueError as error:
        print("b 模式带 encoding：", type(error).__name__)   # -> b 模式带 encoding： ValueError
# // C++: 对应 std::ios::binary 标志；二进制读写用的仍是同一套流对象，差别在于是否做编码转换。

# 常见坑点：
# 1. 用 "w" 打开已有文件：打开瞬间内容就被清空，原数据无法恢复；改写前先确认是否真的需要覆盖。
# 2. 用 "r" 打开可能不存在的文件：抛 FileNotFoundError；不确定时先 exists() 检查，或用 try 按 EAFP 处理。
# 3. 把 "x" 当成“可写”：它只能创建新文件，文件已存在就抛 FileExistsError，常用于避免误覆盖配置。
# 4. 在 "rb"/"wb" 上加 encoding：直接抛 ValueError，二进制模式没有编码概念。
# 5. 混用 "r+" 与 "w+"：两者都可读写，但 "w+" 打开时就截断文件，"r+" 要求文件已存在；用错会静默丢数据。
