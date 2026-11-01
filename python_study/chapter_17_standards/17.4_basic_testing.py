# 第 17 章 Python 基础规范与良好习惯
# 17.4 基础测试意识
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件用 assert 对成绩等级、运费计算、数量解析做正常输入、边界情况与错误输入测试。

# 被测函数集中在文件开头，测试代码只通过公开接口调用它们。
def classify_score(score: int) -> str:
    if not 0 <= score <= 100:
        raise ValueError(f"成绩必须在 0 到 100 之间，当前为 {score}")
    if score >= 90:
        return "优秀"
    if score >= 75:
        return "良好"
    if score >= 60:
        return "及格"
    return "不及格"


def calc_shipping_fee(weight: float) -> float:
    if weight <= 0:
        raise ValueError(f"重量必须大于 0，当前为 {weight}")
    if weight <= 1:
        return 10.0
    return round(10.0 + (weight - 1) * 5, 2)


def parse_quantity(text: str) -> int:
    cleaned = text.strip()
    if not cleaned.isdigit():
        raise ValueError(f"数量必须是正整数，当前输入：{cleaned!r}")
    return int(cleaned)


# 两个断言辅助函数：断言失败会抛出 AssertionError，通过时打印 PASS。
def check_equal(actual, expected, label: str) -> None:
    assert actual == expected, f"{label} 断言失败：期望 {expected}，实际 {actual}"
    print(f"PASS {label}")                                   # -> PASS 后接用例说明


def check_error(func, expected_error, label: str) -> None:
    try:
        func()
    except expected_error:
        print(f"PASS {label}")                               # -> PASS 后接用例说明
    else:
        raise AssertionError(f"{label} 断言失败：没有抛出 {expected_error.__name__}")


# ==================== 17.4.1 正常输入测试 ====================
# 用典型输入验证“正常情况下结果对不对”，这是最基础的一层。
check_equal(classify_score(85), "良好", "正常输入：85 分应为良好")
check_equal(classify_score(95), "优秀", "正常输入：95 分应为优秀")
check_equal(calc_shipping_fee(2.4), 17.0, "正常输入：2.4 千克运费 17.0 元")
check_equal(parse_quantity("12"), 12, "正常输入：文本 12 解析为 12")
# // C++: 常用 assert 或断言宏 CHECK_EQ；Python 的 assert 语法更直接，
# // 注意 python -O 会移除 assert，正式项目多用 pytest/单元测试框架。

# ==================== 17.4.2 边界情况测试 ====================
# 边界是最容易出错的地方：区间端点、刚好进入另一档的临界值。
check_equal(classify_score(0), "不及格", "边界：0 分不及格")
check_equal(classify_score(59), "不及格", "边界：59 分不及格")
check_equal(classify_score(60), "及格", "边界：60 分刚好及格")
check_equal(classify_score(89), "良好", "边界：89 分良好")
check_equal(classify_score(90), "优秀", "边界：90 分优秀")
check_equal(classify_score(100), "优秀", "边界：100 分优秀（上界）")
check_equal(calc_shipping_fee(1.0), 10.0, "边界：1.0 千克仍按首重")
check_equal(calc_shipping_fee(1.01), 10.05, "边界：1.01 千克进入续重")
check_equal(parse_quantity(" 8 "), 8, "边界：带空格的 8 也能解析")
# 只测 85 分这种“中间值”会漏掉 60、75、90 这些真正决定分支的数值。

# ==================== 17.4.3 错误输入测试 ====================
# 错误输入测试关注“该失败的时候是否明确失败”，而不是悄悄返回一个默认值。
check_error(lambda: classify_score(101), ValueError, "错误输入：101 分抛出 ValueError")
check_error(lambda: classify_score(-5), ValueError, "错误输入：-5 分抛出 ValueError")
check_error(lambda: calc_shipping_fee(0), ValueError, "错误输入：0 千克抛出 ValueError")
check_error(lambda: parse_quantity("abc"), ValueError, "错误输入：abc 抛出 ValueError")
check_error(lambda: parse_quantity(""), ValueError, "错误输入：空串抛出 ValueError")
# 测试用例只依赖输入与输出，不依赖函数内部的实现细节，重构后仍然有效。
# 建议的顺序：先写正常输入，再补边界，最后补错误输入，每一条都能说明“为什么测它”。
print("全部测试通过")                                        # -> 全部测试通过

# 常见坑点：
# 1. 现象：测试看起来都过了，但线上还是出错；原因：只测了正常输入；
#    做法：正常、边界、错误输入三类都要覆盖。
# 2. 现象：断言写在 print 之后，结果打印对了断言却被人忽略；原因：没有让失败中断；
#    做法：assert 放在前面，失败即抛 AssertionError。
# 3. 现象：测试里写死内部实现（如直接读 list 下标），重构就全红；原因：绕过公开接口；
#    做法：只调用公开函数或属性。
# 4. 现象：python -O 运行时断言全部失效；原因：优化模式会移除 assert；
#    做法：本地自测可以用 assert，正式项目改用测试框架。
# 5. 现象：错误输入测试失败但不清楚原因；原因：只写 except 没写 else；
#    做法：用 else 抛 AssertionError，明确“本应抛出却没有抛出”。
