# 第 4 章 运算符与表达式
# 4.6 表达式综合应用

# 4.6.1 数值表达式：先按优先级计算，也可用括号明确步骤。
price = 12.5
quantity = 4
discount = 5.0
total = price * quantity - discount
print("应付金额：", total)
# // C++: double total = price * quantity - discount;

# 4.6.2 逻辑判断表达式：组合比较条件，得到是否通过的布尔值。
score = 82
attendance = 0.9
is_passed = score >= 60 and attendance >= 0.8
print("是否通过：", is_passed)
# // C++: bool is_passed = score >= 60 && attendance >= 0.8;

# 4.6.3 输入、计算、输出综合实现
# 为了让脚本可直接运行，这里以固定文本模拟 input() 的返回值。
# 实际练习时可将下行改成 user_input = input("请输入商品数量：")。
user_input = "3"
item_count = int(user_input)      # input() 返回字符串，先转换成整数
unit_price = 9.5
total_price = item_count * unit_price
print(f"购买数量：{item_count}，单价：{unit_price:.2f}，总价：{total_price:.2f}")
# // C++: int item_count; std::cin >> item_count; double total = item_count * unit_price;
