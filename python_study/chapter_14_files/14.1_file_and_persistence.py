# 第 14 章 文件操作
# 14.1 文件与数据持久化
# 学习优先级：P0（核心必学） | 掌握要求：理解
# 本文件：认识文件保存数据的作用、路径的组成方式以及文本与二进制文件的区别。

from pathlib import Path
import tempfile

# ==================== 14.1.1 文件的作用 ====================
# 变量只存在内存里，程序结束就消失；写进文件的数据才能被下一次运行读到。
memo = "周五前提交季度报表"
print("内存中的备忘：", memo)                      # -> 内存中的备忘： 周五前提交季度报表

with tempfile.TemporaryDirectory() as temp_dir:
    memo_path = Path(temp_dir) / "memo.txt"
    memo_path.write_text(memo + "\n", encoding="utf-8", newline="\n")
    print("文件名：", memo_path.name)               # -> 文件名： memo.txt
    print("占用字节：", memo_path.stat().st_size)    # -> 占用字节： 28
    reloaded = memo_path.read_text(encoding="utf-8").rstrip("\n")
    print("重新读取：", reloaded)                   # -> 重新读取： 周五前提交季度报表
    # newline="\n" 关闭 Windows 默认的换行转换，写出的字节在不同平台上一致，便于对照。
# 同一个变量在两次运行之间不会自动保留，文件才是跨进程、跨时间的数据载体。
# // C++: std::ofstream 写完再用 std::ifstream 读回；C++ 需要自行处理编码与换行转换。

# ==================== 14.1.2 文件路径基础 ====================
# 路径决定文件放在哪里；用 pathlib 拼接路径比手写分隔符更安全。
base = Path("records")
memo_path = base / "2026" / "memo.txt"
print("相对路径：", memo_path.as_posix())       # -> 相对路径： records/2026/memo.txt
print("文件名：", memo_path.name)               # -> 文件名： memo.txt
print("主名：", memo_path.stem)                 # -> 主名： memo
print("扩展名：", memo_path.suffix)             # -> 扩展名： .txt
print("父目录：", memo_path.parent.as_posix())  # -> 父目录： records/2026
# // C++: std::filesystem::path 的 filename()、stem()、extension()、parent_path() 作用相同。
# 相对路径以“当前工作目录”为基准；启动目录一变，同一段代码指向的位置也会变。
# Windows 的绝对路径形如 D:/work/notes.txt，用 Path("D:/work") / "notes.txt" 同样可以拼接。

with tempfile.TemporaryDirectory() as temp_dir:
    folder = Path(temp_dir) / "exports"
    folder.mkdir()
    (folder / "draft.txt").write_text("草稿一份\n", encoding="utf-8")
    print("目录是否存在：", folder.exists())                    # -> 目录是否存在： True
    print("文件是否存在：", (folder / "draft.txt").exists())     # -> 文件是否存在： True
    print("其他文件是否存在：", (folder / "other.txt").exists())  # -> 其他文件是否存在： False

# ==================== 14.1.3 文本文件与二进制文件初识 ====================
# 文本文件按字符存储，必须知道编码才能正确解码；二进制文件按字节存储，图片、压缩包都属于这一类。
with tempfile.TemporaryDirectory() as temp_dir:
    text_path = Path(temp_dir) / "note.txt"
    text_path.write_text("中文内容\n", encoding="utf-8", newline="\n")
    raw = text_path.read_bytes()
    print("文本文件的字节：", raw)       # -> 文本文件的字节： b'\xe4\xb8\xad\xe6\x96\x87\xe5\x86\xa5\xe5\xae\xb9\n'
    print("解码回文本：", raw.decode("utf-8").rstrip())   # -> 解码回文本： 中文内容
    print("字节总数：", len(raw))        # -> 字节总数： 13
# 一个汉字在 utf-8 中占 3 字节，4 个汉字加 1 个换行正好 13 字节。

    data_path = Path(temp_dir) / "record.bin"
    data_path.write_bytes(bytes([120, 45, 3]))
    print("二进制内容：", data_path.read_bytes())   # -> 二进制内容： b'x-\x03'
    try:
        data_path.open("rb", encoding="utf-8")
    except ValueError as error:
        print("二进制模式带 encoding：", type(error).__name__)   # -> 二进制模式带 encoding： ValueError

    gbk_path = Path(temp_dir) / "gbk.txt"
    gbk_path.write_bytes("中文内容".encode("gbk"))
    try:
        gbk_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        print("用错编码读取：", type(error).__name__)              # -> 用错编码读取： UnicodeDecodeError
    print("按正确编码读取：", gbk_path.read_text(encoding="gbk"))  # -> 按正确编码读取： 中文内容
# 编码不一致时不会得到“乱码”，而是直接抛 UnicodeDecodeError；读写的 encoding 必须成对出现。

# 常见坑点：
# 1. 把临时目录的完整路径写进注释当作固定结果：换一台机器路径就不同。正确做法是只打印文件名或相对路径。
# 2. 用字符串相加拼路径（"records" + "/" + "memo.txt"）：遇到分隔符或特殊字符会出错；应使用 Path / Path("a") / "b"。
# 3. 读写中文时不写 encoding：不同平台默认编码不同，可能报错或写出乱码；文本读写始终显式指定 encoding="utf-8"。
# 4. 用 read_text 去读图片或压缩包：二进制文件应使用 read_bytes 或 "rb" 模式，否则会抛 UnicodeDecodeError。
# 5. 离开 TemporaryDirectory 块后继续用旧路径：目录已被删除，再访问会抛 FileNotFoundError；临时文件只在块内有效。
