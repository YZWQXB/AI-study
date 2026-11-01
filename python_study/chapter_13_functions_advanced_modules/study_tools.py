# 第 13 章 函数进阶与模块基础
# 13.4 模块基础（配套模块 study_tools）
# 学习优先级：P1（重点掌握） | 掌握要求：会用
# 本文件：供 13.4_modules.py 导入的工具模块，演示 docstring、__all__ 与 __main__ 入口。

"""订单与几何计算的工具函数集合，供模块导入演示使用。"""

__all__ = ["calc_area", "round_price", "split_evenly"]

# 模块顶层代码在第一次导入时执行一次，这里用于演示导入缓存。
print("study_tools 模块被首次加载")


def calc_area(width: float, height: float) -> float:
    """计算矩形面积，结果保留两位小数。"""
    return round(width * height, 2)


def round_price(price: float, digits: int = 2) -> float:
    """按指定小数位四舍五入价格。"""
    return round(price, digits)


def split_evenly(total: float, people: int) -> tuple[float, float]:
    """把金额平均分摊给若干人，返回 (每人金额, 未分完的余额)。"""
    if people <= 0:
        return 0.0, total
    share = round(total / people, 2)
    remainder = round(total - share * people, 2)
    return share, remainder


if __name__ == "__main__":
    print("直接运行 study_tools，执行演示代码")
    print(f"calc_area(3, 4) = {calc_area(3, 4)}")
    print(f"split_evenly(100, 3) = {split_evenly(100, 3)}")

# 常见坑点：
# 1. 在库模块顶层直接打印或执行耗时操作。
#    现象：任何导入该模块的文件都会多出无关输出，甚至变慢。
#    原因：模块第一次导入时顶层代码必定执行。
#    正确做法：把演示和测试代码放进 if __name__ == "__main__": 代码块。
# 2. 认为所有函数都需要写进 __all__。
#    现象：维护 __all__ 时容易漏掉新函数。
#    原因：不写 __all__ 时，from module import * 会导入所有不以下划线开头的名字。
#    正确做法：只在需要限制导出范围时写 __all__，并保持与公开函数同步。
# 3. 把模块名写成与标准库同名，例如 random.py、math.py。
#    现象：导入标准库时实际导入了自己的文件，出现 AttributeError。
#    原因：脚本所在目录会优先被搜索。
#    正确做法：模块名使用业务前缀，例如 study_tools、score_utils。
