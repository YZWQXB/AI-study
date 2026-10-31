# 第 5 章 字符串与文本处理基础
# 5.5 文本编码初步

# 5.5.1 Unicode 基本概念
# Unicode 为世界各地的字符分配统一编号，Python 的 str 用于表示 Unicode 文本。
message = "中文 Python"
print(message)
print(len(message))               # Python 按 Unicode 码位计数；不同语言对“用户可见字符”的定义更复杂
# // C++: std::string 通常保存字节；处理 Unicode 文本需要明确采用的编码和库。

# 5.5.2 编码与解码认知
# 编码：把文本 str 转为字节 bytes；解码：按相同编码把 bytes 还原成文本。
text = "你好"
encoded = text.encode("utf-8")    # str -> bytes
restored = encoded.decode("utf-8") # bytes -> str
print("文本：", text)
print("UTF-8 字节：", encoded)
print("解码还原：", restored)
# // C++: 常见做法是用字符串库按 UTF-8 编码/解码；char* 本身不自动表达字符编码。

# 5.5.3 常见乱码问题初识
# 乱码常见原因是写入和读取时选用了不同编码；解码时必须使用实际数据的编码。
utf8_bytes = "中文".encode("utf-8")
correct_text = utf8_bytes.decode("utf-8")
print("正确解码：", correct_text)

# 错误编码可能产生乱码，也可能抛 UnicodeDecodeError；这里用 errors 参数只演示可见现象。
wrong_text = utf8_bytes.decode("latin-1")
print("用错误编码解释的文本：", wrong_text)
# 文件读写文本时可明确指定 encoding="utf-8"，避免依赖系统默认编码。
# // C++: 读取文件字节后，需知道原编码并使用匹配的转换方式。
