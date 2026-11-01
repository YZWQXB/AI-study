# 第 14 章 文件操作
# 14.5 文件操作综合案例
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：用临时目录完成备忘录、成绩汇总和日志记录三个真实场景。

from pathlib import Path
import tempfile


def load_memos(path: Path) -> list[dict[str, str]]:
    """把 "日期|状态|内容" 的文本行解析成字典列表。"""
    memos = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        date, status, content = line.split("|")
        memos.append({"date": date, "status": status, "content": content})
    return memos


def save_memos(path: Path, memos: list[dict[str, str]]) -> None:
    """把字典列表重新写回文本文件，一行一条。"""
    lines = [f"{memo['date']}|{memo['status']}|{memo['content']}" for memo in memos]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_scores(path: Path) -> list[dict[str, object]]:
    """读取 "姓名,语文,数学" 格式的成绩文件。"""
    rows = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        name, chinese, math = line.split(",")
        rows.append({"name": name, "chinese": int(chinese), "math": int(math)})
    return rows


with tempfile.TemporaryDirectory() as temp_dir:
    # ==================== 14.5.1 备忘录系统 ====================
    # 备忘记录包含日期、完成状态和内容，用竖线分隔保存，读回后再解析。
    memo_path = Path(temp_dir) / "memos.txt"
    memo_path.write_text(
        "2026-11-01|未完成|提交季度报表\n"
        "2026-11-02|未完成|预约体检\n"
        "2026-11-03|已完成|整理会议纪要\n",
        encoding="utf-8",
    )
    memos = load_memos(memo_path)
    print("备忘录条数：", len(memos))         # -> 备忘录条数： 3

    memos.append({"date": "2026-11-04", "status": "未完成", "content": "缴纳水电费"})
    memos[0]["status"] = "已完成"
    save_memos(memo_path, memos)
    reloaded = load_memos(memo_path)
    print("保存后重新读取：")
    for memo in reloaded:
        print(f"  {memo['date']} [{memo['status']}] {memo['content']}")
    # 输出：
    #   2026-11-01 [已完成] 提交季度报表
    #   2026-11-02 [未完成] 预约体检
    #   2026-11-03 [已完成] 整理会议纪要
    #   2026-11-04 [未完成] 缴纳水电费

    finished = sum(1 for memo in reloaded if memo["status"] == "已完成")
    print("已完成条数：", finished)          # -> 已完成条数： 2
# // C++: 常见做法是自己定义结构体再逐行解析；这里用 dict 保存同一条记录的多个字段。

    # ==================== 14.5.2 成绩文件管理 ====================
    # 读取原始成绩，计算总分与平均分，再把结果写进新的汇总文件。
    score_path = Path(temp_dir) / "scores.csv"
    score_path.write_text("姓名,语文,数学\n张伟,78,92\n李娜,85,88\n王强,59,52\n", encoding="utf-8")

    summaries = []
    for row in load_scores(score_path):
        total = int(row["chinese"]) + int(row["math"])
        average = total / 2
        status = "合格" if average >= 60 else "补考"
        summaries.append({"name": row["name"], "total": total, "average": average, "status": status})

    summary_path = Path(temp_dir) / "summary.csv"
    lines = ["姓名,总分,平均分,状态"]
    for item in summaries:
        lines.append(f"{item['name']},{item['total']},{item['average']:.1f},{item['status']}")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("成绩汇总（3 人）：")
    for item in summaries:
        print(f"  {item['name']} 总分 {item['total']} 平均 {item['average']:.1f} 状态 {item['status']}")
    # 输出：
    #   张伟 总分 170 平均 85.0 状态 合格
    #   李娜 总分 173 平均 86.5 状态 合格
    #   王强 总分 111 平均 55.5 状态 补考
    class_average = sum(float(item["average"]) for item in summaries) / len(summaries)
    print("班级平均分：", f"{class_average:.1f}")   # -> 班级平均分： 75.7

    rows = summary_path.read_text(encoding="utf-8").splitlines()
    print("汇总文件行数：", len(rows))       # -> 汇总文件行数： 4
    print("汇总文件第二行：", rows[1])        # -> 汇总文件第二行： 张伟,170,85.0,合格
# 写入前先把表头放进列表，再 join 成一个字符串，可以避免每行都 open 一次文件。

    # ==================== 14.5.3 简单日志记录 ====================
    # 日志使用追加模式，程序每发生一件事就追加一行，历史记录不会被覆盖。
    log_path = Path(temp_dir) / "app.log"

    def write_log(path: Path, moment: str, level: str, message: str) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(f"{moment} {level} {message}\n")

    write_log(log_path, "2026-11-01 08:00:00", "INFO", "服务启动")
    write_log(log_path, "2026-11-01 08:01:10", "INFO", "加载配置完成")
    write_log(log_path, "2026-11-01 08:02:35", "WARN", "缓存命中率偏低")
    write_log(log_path, "2026-11-01 08:03:00", "INFO", "开始导出报表")
    write_log(log_path, "2026-11-01 08:03:40", "ERROR", "导出报表失败")

    log_lines = log_path.read_text(encoding="utf-8").splitlines()
    counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
    for line in log_lines:
        level = line.split(maxsplit=3)[2]
        if level in counts:
            counts[level] += 1
    print("日志共", len(log_lines), "条：INFO", counts["INFO"], "条，WARN", counts["WARN"], "条，ERROR", counts["ERROR"], "条")
    # -> 日志共 5 条：INFO 3 条，WARN 1 条，ERROR 1 条

    print("ERROR 明细：")
    for line in log_lines:
        if " ERROR " in line:
            print("  ", line)
    # 输出：
    #    2026-11-01 08:03:40 ERROR 导出报表失败
    print("最后一条：", log_lines[-1])   # -> 最后一条： 2026-11-01 08:03:40 ERROR 导出报表失败
# 统计时只关心级别列，所以用固定分隔符写入比自由格式更利于后续分析。

# 常见坑点：
# 1. 用 write_text 保存备忘列表：每次都会覆盖全部内容，新增条目全部丢失；追加式数据要用 "a" 或读全量后整体重写。
# 2. 解析文本时直接 split 不校验字段数：遇到脏行会抛 ValueError 让整个程序退出；先判断行是否为空，必要时用 try。
# 3. 把浮点数原样写入文件后直接字符串比较：格式不一致（85.0 与 85）会造成误判；统一用格式化或转成数值再比较。
# 4. 日志中途改用 "w" 模式：历史记录被清空，排查问题失去线索；日志文件固定使用 "a"。
# 5. 忘记关闭文件就读取同一路径：某些平台上缓冲区未刷新，读到的内容可能比预期少；写入后立即离开 with 再读。
