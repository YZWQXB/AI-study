# 第 13 章 函数进阶与模块基础
# 13.2 递归基础
# 学习优先级：P1（重点掌握） | 掌握要求：熟练
# 本文件：学习递归的分解思路与终止条件，并用阶乘、斐波那契和目录求和的例子对比迭代写法。

import sys

# ==================== 13.2.1 递归思想 ====================
# 递归是函数直接或间接调用自己，把大问题化成规模更小的同类问题。
def countdown(n: int) -> None:
    if n <= 0:                   # 最小规模直接处理
        print("起飞")
        return
    print(n)
    countdown(n - 1)             # 把 n 的问题交给 n - 1 处理

countdown(5)
# 输出六行：5、4、3、2、1、起飞
# // C++: void countdown(int n) { if (n <= 0) { ... return; } countdown(n - 1); }
# 递归调用并不会立刻返回，而是逐层压栈，到达终止条件后再逐层返回。

# ==================== 13.2.2 终止条件 ====================
# 没有终止条件的递归会一直调用自己，直到超过解释器的递归上限。
def factorial(n: int) -> int:
    if n <= 1:                   # 终止条件：0 和 1 的阶乘都等于 1
        return 1
    return n * factorial(n - 1)

print(factorial(5))              # -> 120
print(factorial(1))              # -> 1
print(factorial(0))              # -> 1
# 计算过程：factorial(5) = 5 * factorial(4) = ... = 5 * 4 * 3 * 2 * 1。
# // C++: long long factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }

# 缺少终止条件的函数，调用一次就会报 RecursionError，下面仅作说明，不参与运行。
# def factorial_bad(n: int) -> int:
#     return n * factorial_bad(n - 1)

print(f"默认递归上限：{sys.getrecursionlimit()}")    # -> 默认递归上限：1000
# 递归层数超过上限时抛出 RecursionError: maximum recursion depth exceeded。
# // C++: 递归过深会造成栈溢出，通常以崩溃结束；Python 由解释器主动检查层数。

# ==================== 13.2.3 简单递归案例 ====================
# 相同计算用迭代实现，便于与递归对照。
def factorial_iter(n: int) -> int:
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result

print(factorial(10), factorial_iter(10))    # -> 3628800 3628800
# 递归写法更接近数学定义，迭代写法没有函数调用开销。

# 斐波那契数列：第 n 项等于前两项之和，前两项为 0 和 1。
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))             # -> 55
# 递归版对同一个 n 会重复计算多次，n 增大后耗时快速增长。

def fibonacci_iter(n: int) -> int:
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous

print(fibonacci_iter(10))        # -> 55
# // C++: 同样存在重复计算问题；实际项目常用迭代、记忆化或矩阵快速幂。

# 目录大小统计：值可能是文件大小，也可能是子目录，结构相同，适合递归分治。
folder = {
    "readme.txt": 2,
    "docs": {"guide.md": 6, "api.md": 4},
    "images": {"logo.png": 3, "icons": {"small.png": 1}},
}

def total_size(node: dict[str, int | dict]) -> int:
    total = 0
    for value in node.values():
        if isinstance(value, dict):
            total += total_size(value)    # 子目录交给同一函数处理
        else:
            total += value                # 文件直接累加大小
    return total

print(f"目录总大小：{total_size(folder)}")        # -> 目录总大小：16

# 递归深度与数据规模成正比：目录嵌套很深时可能触发 RecursionError。
# 这种场景可以改用显式栈或队列的迭代写法；Python 也没有尾递归优化。
# 用递归求和做一次规模对比：递归 100 层可行，而迭代更省栈空间。
def sum_to(n: int) -> int:
    if n == 0:
        return 0
    return n + sum_to(n - 1)

print(sum_to(100), sum(range(1, 101)))           # -> 5050 5050
# // C++: 编译器在优化后可能消除部分尾调用，但不应依赖这一点。

# 常见坑点：
# 1. 忘记写终止条件。
#    现象：抛出 RecursionError: maximum recursion depth exceeded。
#    原因：函数每次都调用自己，规模没有缩小到可直接处理的程度。
#    正确做法：先写出最小规模的处理分支，并确保每次递归都向它靠近。
# 2. 终止条件写错，例如只判断 n == 1，却传入 0 或负数。
#    现象：仍然无限递归，或结果偏大。
#    原因：边界值没有覆盖完整。
#    正确做法：用 n <= 1 这类包含边界的判断，并单独验证 0、1 和负数。
# 3. 递归调用后忘记 return 组合结果。
#    现象：函数返回 None，后续相乘或相加时报 TypeError。
#    原因：只调用了递归函数，没有把返回值参与计算。
#    正确做法：写成 return n * factorial(n - 1) 这样的组合表达式。
# 4. 用递归处理规模很大的线性数据。
#    现象：几千层后抛出 RecursionError，或运行很慢。
#    原因：每层递归都占用调用栈，Python 默认上限约 1000。
#    正确做法：线性问题优先用循环；必须递归时改用显式栈。
# 5. 直接对斐波那契这类问题使用朴素递归。
#    现象：n 取 35 左右就明显卡顿。
#    原因：同一子问题被反复计算，调用次数呈指数增长。
#    正确做法：改用迭代，或缓存已经计算过的结果。
