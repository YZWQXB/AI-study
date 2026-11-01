# 第 15 章 异常处理与基础调试
# 15.6 健壮程序设计
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：把输入容错、文件异常处理、重试与友好提示组合成一个稳定的处理流程。

from pathlib import Path
import tempfile

# ==================== 15.6.1 输入容错设计 ====================
# 校验函数返回“值 + 说明”，让调用方既能继续流程，也能给出具体提示。
def parse_quantity(raw: str) -> tuple[int | None, str]:
    text = raw.strip()
    if not text:
        return None, "输入为空，已跳过"
    try:
        value = int(text)
    except ValueError:
        return None, f"不是整数：{text!r}，已跳过"
    if value <= 0:
        return None, f"数量必须大于 0，收到 {value}，已跳过"
    return value, "校验通过"

raw_quantities = ["120", "", "abc", " -30 ", "0", "88"]
accepted = 0
for raw in raw_quantities:
    value, message = parse_quantity(raw)
    if value is None:
        print(f"  {raw!r} 被拒绝：{message}")
    else:
        accepted += 1
        print(f"  {raw!r} 接受：{value}")
print("通过条数：", accepted)
# 输出：
#   '120' 接受：120
#   '' 被拒绝：输入为空，已跳过
#   'abc' 被拒绝：不是整数：'abc'，已跳过
#   ' -30 ' 被拒绝：数量必须大于 0，收到 -30，已跳过
#   '0' 被拒绝：数量必须大于 0，收到 0，已跳过
#   '88' 接受：88
# 通过条数： 2
# 坏数据只影响自己那一条，不会让整批处理中断。

# ==================== 15.6.2 文件异常处理 ====================
# 读取配置时对“文件缺失”和“内容非法”分别兜底，程序不会因为一个坏配置直接退出。
with tempfile.TemporaryDirectory() as temp_dir:
    config_path = Path(temp_dir) / "config.ini"

    def load_config(path: Path) -> dict[str, int]:
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print("  配置文件不存在，使用默认配置")
            return {"retry_limit": 3, "timeout_seconds": 10}
        result = {}
        for line in text.splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            try:
                result[key.strip()] = int(value.strip())
            except ValueError:
                print(f"  配置项 {key.strip()} 的值无法解析，已忽略")
        return result

    print("读取不存在的配置：")
    print("  结果：", load_config(config_path))
    # 输出：
    # 读取不存在的配置：
    #   配置文件不存在，使用默认配置
    #   结果： {'retry_limit': 3, 'timeout_seconds': 10}

    config_path.write_text("# 服务配置\nretry_limit=5\ntimeout_seconds=三十\n", encoding="utf-8", newline="\n")
    print("读取有脏数据的配置：")
    print("  结果：", load_config(config_path))
    # 输出：
    # 读取有脏数据的配置：
    #   配置项 timeout_seconds 的值无法解析，已忽略
    #   结果： {'retry_limit': 5}

    try:
        (Path(temp_dir) / "logs" / "app.log").write_text("启动\n", encoding="utf-8", newline="\n")
    except FileNotFoundError:
        print("父目录不存在，写入失败：FileNotFoundError")   # -> 父目录不存在，写入失败：FileNotFoundError
    (Path(temp_dir) / "logs").mkdir(parents=True, exist_ok=True)
    (Path(temp_dir) / "logs" / "app.log").write_text("启动\n", encoding="utf-8", newline="\n")
    print("补建目录后写入成功：", (Path(temp_dir) / "logs" / "app.log").exists())   # -> 补建目录后写入成功： True
# 文件异常的处理原则：先判断“缺少什么”，再决定用默认值、提示重试还是终止流程。

# ==================== 15.6.3 用户交互程序优化 ====================
# 逐行导入并说明原因，最后汇总成功与失败数量，比“遇到第一条错误就退出”体验更好。
def import_scores(raw_lines: list[str]) -> tuple[dict[str, int], list[str]]:
    imported = {}
    failed = []
    for number, raw in enumerate(raw_lines, start=1):
        name, _, raw_score = raw.partition(",")
        if not name or not raw_score:
            failed.append(f"第 {number} 行格式不完整")
            print(f"第 {number} 行 {raw!r}：格式不完整，已跳过")
            continue
        try:
            score = int(raw_score)
        except ValueError:
            failed.append(f"第 {number} 行成绩不是整数")
            print(f"第 {number} 行 {raw!r}：成绩不是整数，已跳过")
            continue
        if not 0 <= score <= 100:
            failed.append(f"第 {number} 行成绩超出范围")
            print(f"第 {number} 行 {raw!r}：成绩超出 0 到 100，已跳过")
            continue
        imported[name] = score
        print(f"第 {number} 行 {raw!r}：导入成功")
    return imported, failed

raw_lines = ["张伟,90", "李娜", "王强,八十八", "赵敏,120", "钱多,76"]
imported, failed = import_scores(raw_lines)
print("导入结果：", imported)
print("成功条数：", len(imported), "失败条数：", len(failed))
# 输出：
# 第 1 行 '张伟,90'：导入成功
# 第 2 行 '李娜'：格式不完整，已跳过
# 第 3 行 '王强,八十八'：成绩不是整数，已跳过
# 第 4 行 '赵敏,120'：成绩超出 0 到 100，已跳过
# 第 5 行 '钱多,76'：导入成功
# 导入结果： {'张伟': 90, '钱多': 76}
# 成功条数： 2 失败条数： 3

with tempfile.TemporaryDirectory() as temp_dir:
    result_path = Path(temp_dir) / "imported.txt"
    lines = [f"{name},{score}" for name, score in imported.items()]
    result_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("落盘内容：", result_path.read_text(encoding="utf-8").splitlines())
    # -> 落盘内容： ['张伟,90', '钱多,76']
# 只把成功的数据写进文件，失败明细留在提示与日志里，避免坏数据污染结果文件。

def submit_with_retry(payloads: list[str], retry_limit: int) -> str | None:
    for attempt in range(1, retry_limit + 1):
        payload = payloads[attempt - 1]
        try:
            if not payload.strip():
                raise ValueError("内容为空")
            return payload.strip()
        except ValueError as error:
            print(f"  第 {attempt} 次提交失败：{error}，重试")
    return None

print("最终提交：", submit_with_retry(["", "  ", "张伟,90"], 3))
print("次数耗尽：", submit_with_retry(["", ""], 2))
# 输出：
#   第 1 次提交失败：内容为空，重试
#   第 2 次提交失败：内容为空，重试
# 最终提交： 张伟,90
#   第 1 次提交失败：内容为空，重试
#   第 2 次提交失败：内容为空，重试
# 次数耗尽： None
# 重试必须有上限；次数耗尽后返回 None，由调用方决定提示还是放弃。

# 常见坑点：
# 1. 只捕获 Exception 却什么都不做：错误被吞掉，用户得不到任何提示；至少说明原因或记录日志。
# 2. 一次性读取全部输入且不校验：一条脏数据就让整体失败；应逐条校验、跳过坏数据并汇总。
# 3. 重试没有上限：遇到永久性失败会一直循环；固定重试次数，耗尽后给出明确结果。
# 4. 在 try 中定义变量、在 except 中继续使用：变量可能未赋值，使用时会触发 UnboundLocalError（NameError 的子类）；先给默认值再进入 try。
# 5. 把异常对象原样展示给用户：会暴露内部路径与实现细节；界面给友好提示，细节写日志。
