# 第 5 章 字符串与文本处理基础
# 5.4 字符串格式化进阶

# 5.4.1 宽度与对齐
# f-string 格式说明符可设定最小宽度；< 左对齐，> 右对齐，^ 居中。
name = "小林"
print(f"|{name:<8}|")             # 左对齐，字段宽度至少为 8
print(f"|{name:>8}|")             # 右对齐
print(f"|{name:^8}|")             # 居中
# // C++: std::setw() 与 std::left/std::right 可控制输出宽度和对齐。

# 5.4.2 数值格式化
price = 12.5
ratio = 0.875
print(f"价格：{price:.2f}")         # 固定显示两位小数：12.50
print(f"比例：{ratio:.1%}")         # 百分比格式：87.5%
print(f"金额：{1234567.8:,.2f}")    # 逗号分组并保留两位小数
# // C++: iostream 可用 std::fixed、std::setprecision 等控制数值格式。

# 5.4.3 常见输出模板设计
# 用固定标签和对齐宽度能让多条信息更容易阅读。
items = [("苹果", 3, 2.5), ("香蕉", 2, 4.0)]
print(f"{'商品':<8}{'数量':>6}{'单价':>10}")
for item_name, quantity, unit_price in items:
    print(f"{item_name:<8}{quantity:>6}{unit_price:>10.2f}")
# // C++: 可用 std::setw() 输出列；Python 的 f-string 把模板与变量放在一起。
