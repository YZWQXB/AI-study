# 第 2 章 开发环境搭建与程序运行
# 2.5 Python 文件与目录基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：用 pathlib 认识 .py 文件、目录结构以及相对/绝对路径。

from pathlib import Path

# ==================== 2.5.1 .py 文件 ====================
# Python 源码文件以 .py 结尾；模块名就是去掉扩展名后的文件名。
# 文件名应使用小写字母和下划线，避免空格与中文，便于 import。
script = Path(__file__)
print("文件名：", script.name)                # -> 文件名： 2.5_files_and_paths.py
print("扩展名：", script.suffix)              # -> 扩展名： .py
print("所在目录：", script.parent.name)        # -> 所在目录： chapter_02_environment
print("解析后是绝对路径：", script.resolve().is_absolute())   # -> 解析后是绝对路径： True

# ==================== 2.5.2 文件夹与项目目录 ====================
# 一个项目通常按章节或功能划分目录，每个目录内的 .py 文件可直接运行。
# 本章目录中放置了 5 个示例文件，可以用 glob 按模式筛选。
chapter_files = sorted(script.parent.glob("2*_*.py"))
print("本章示例文件数量：", len(chapter_files))   # -> 本章示例文件数量： 5
print("目录是否存在：", script.parent.is_dir())   # -> 目录是否存在： True
# // C++: 文件系统操作通常依赖平台 API 或 std::filesystem；Python 的 pathlib 跨平台统一。

# ==================== 2.5.3 相对路径与绝对路径初步 ====================
# 相对路径依赖当前工作目录，绝对路径从根目录开始，不受 cwd 影响。
print("路径拼接：", Path("data", "scores.txt").as_posix())   # -> 路径拼接： data/scores.txt
print("逐级拆分：", Path("archive/2026/report.csv").parts)    # -> 逐级拆分： ('archive', '2026', 'report.csv')
print("替换扩展名：", Path("report.csv").with_suffix(".txt"))  # -> 替换扩展名： report.txt
print("相对上级目录：", Path("..", "python_study").parts)     # -> 相对上级目录： ('..', 'python_study')
# // C++: std::filesystem::path 也提供拼路径、取扩展名等操作，但字符串拼接仍需自己避免。
# 跨平台代码优先使用 Path，不要在字符串里手写反斜杠。

# 常见坑点：
# 1. 在 Windows 字符串里写 "C:\new\table.txt"，\n 和 \t 会被当成转义字符。
# 2. 相对路径基于当前工作目录，而不是脚本所在目录，换一个启动位置就找不到文件。
# 3. 在 REPL 或某些打包环境中没有 __file__，不能无条件依赖它。
# 4. 用字符串相加拼接路径，遇到不同分隔符或空路径时容易出错，应使用 Path / 运算符。
