# 第 15 章 异常处理与基础调试
# 15.3 异常处理机制
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：掌握 try-except、else/finally、多异常捕获，并认识异常层级与 except* 拓展。

from pathlib import Path
import tempfile

# ==================== 15.3.1 try-except ====================
# 把可能出错的语句放进 try，出错时跳到匹配的 except，程序继续往下执行。
raw_inputs = ["88", "abc", "", "76"]

def parse_score(raw: str) -> int:
    return int(raw)

for raw in raw_inputs:
    try:
        print(f"输入 {raw!r} 解析为 {parse_score(raw)}")
    except ValueError as error:
        print(f"输入 {raw!r} 解析失败：{error}")
# 输出：
# 输入 '88' 解析为 88
# 输入 'abc' 解析失败：invalid literal for int() with base 10: 'abc'
# 输入 '' 解析失败：invalid literal for int() with base 10: ''
# 输入 '76' 解析为 76
# 一条坏数据不会中断整批处理，这是异常处理最常见的用途。

raw = " 88 "
print("LBYL 用 isdigit 判断：", raw.isdigit())     # -> LBYL 用 isdigit 判断： False
print("EAFP 直接转换：", int(raw))                # -> EAFP 直接转换： 88
# EAFP 是“先尝试，出错再处理”，LBYL 是“先检查再执行”；isdigit() 把首尾空白判为不合法，比 int() 更苛刻。
# // C++: 常见风格是先检查返回值或状态码；Python 更常用 EAFP，两种都能用，关键是覆盖所有边界情况。

# ==================== 15.3.2 else 与 finally ====================
# else 只在 try 内没有异常时执行；finally 无论是否出错都会执行。
def parse_with_else(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        print("  解析失败，按 0 分处理")
        return 0
    else:
        print("  解析成功，使用真实分数")
        return value
    finally:
        print("  记录本次解析结果")

for raw in ("88", "abc"):
    print(f"处理输入 {raw!r}：")
    print("  返回：", parse_with_else(raw))
# 输出：
# 处理输入 '88'：
#   解析成功，使用真实分数
#   记录本次解析结果
#   返回： 88
# 处理输入 'abc'：
#   解析失败，按 0 分处理
#   记录本次解析结果
#   返回： 0
# finally 在 return 真正返回之前执行，所以“记录”总出现在“返回”之前。

def risky_task() -> None:
    try:
        raise RuntimeError("任务失败")
    finally:
        print("  finally 仍然执行")

try:
    risky_task()
except RuntimeError as error:
    print("异常没有被 finally 屏蔽：", error)   # -> 异常没有被 finally 屏蔽： 任务失败
# finally 适合做清理（关闭连接、删除临时文件）；它不会吞掉异常，也不会让失败的 try 变成功。

# ==================== 15.3.3 捕获多个异常 ====================
# 多种异常需要相同处理时，把异常类型写成元组。
def read_count(data: dict[str, str], key: str) -> int:
    try:
        return int(data[key])
    except (KeyError, ValueError) as error:
        print("  读取失败：", type(error).__name__)
        return -1

data = {"count": "3", "price": "2.5"}
print("count 结果：", read_count(data, "count"))
print("price 结果：", read_count(data, "price"))
print("owner 结果：", read_count(data, "owner"))
# 输出：
# count 结果： 3
#   读取失败： ValueError
# price 结果： -1
#   读取失败： KeyError
# owner 结果： -1

with tempfile.TemporaryDirectory() as temp_dir:
    config_path = Path(temp_dir) / "timeout.txt"

    def load_timeout(path: Path) -> int:
        try:
            return int(path.read_text(encoding="utf-8").strip())
        except FileNotFoundError:
            print("  配置文件缺失，使用默认 30 秒")
            return 30
        except ValueError:
            print("  配置内容不是整数，使用默认 30 秒")
            return 30

    print("缺失文件：", load_timeout(config_path))     # -> 缺失文件： 30，前面有提示
    config_path.write_text("六十\n", encoding="utf-8", newline="\n")
    print("内容非法：", load_timeout(config_path))     # -> 内容非法： 30，前面有提示
    config_path.write_text("20\n", encoding="utf-8", newline="\n")
    print("内容合法：", load_timeout(config_path))     # -> 内容合法： 20
# 不同异常对应不同补救措施时，就分开写多个 except，而不是塞进同一个分支。

# ==================== 15.3.4 异常层级与 except* 拓展 ====================
# Python 的异常按继承关系组织，子类异常也能被父类的 except 捕获。
print("ZeroDivisionError 属于 ArithmeticError：", issubclass(ZeroDivisionError, ArithmeticError))   # -> True
print("KeyError 属于 LookupError：", issubclass(KeyError, LookupError))                               # -> True
print("FileNotFoundError 属于 OSError：", issubclass(FileNotFoundError, OSError))                     # -> True
# 层级：Exception -> ArithmeticError -> ZeroDivisionError
#       Exception -> LookupError -> IndexError / KeyError
#       Exception -> OSError -> FileNotFoundError

try:
    [1, 2][5]
except LookupError as error:
    print("用父类捕获子类：", type(error).__name__)   # -> 用父类捕获子类： IndexError
# 写 except 时先具体、后宽泛；把 Exception 写在最前面会让后面的分支永远不执行。

try:
    raise ExceptionGroup(
        "批量校验失败",
        [ValueError("数量必须是整数"), TypeError("价格必须是数字")],
    )
except* ValueError as group:
    print("except* 捕获 ValueError：", len(group.exceptions))   # -> except* 捕获 ValueError： 1
except* TypeError as group:
    print("except* 捕获 TypeError：", len(group.exceptions))    # -> except* 捕获 TypeError： 1
# ExceptionGroup 让多个互不相关的失败一起传递，except* 按类型分别处理，未匹配的子异常最后会重新抛出。
# // C++: std::exception 也是基类层次（std::runtime_error、std::out_of_range 等），但一次只能抛出并捕获一个异常。

# 常见坑点：
# 1. except 分支顺序写反：把 Exception 放在前面，后面的具体分支永远不执行；应具体类型在前、宽泛类型在后。
# 2. 把一大段代码都塞进 try：一处出错会跳过后面本应正常执行的语句；try 只包住可能出错的最小片段。
# 3. 在 finally 里写 return 或 continue：原异常会被丢弃，问题被静默隐藏；finally 只做清理，不做流程控制。
# 4. 在 else 里继续写可能出错的代码：else 中的异常不会被同一组 except 捕获，容易漏处理。
# 5. 捕获后只打印“出错了”：没有类型和信息就无法定位；至少记录 type(error).__name__ 与 error 本身。
