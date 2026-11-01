# 第 13 章 函数进阶与模块基础
# 13.4 模块基础
# 学习优先级：P0（核心必学） | 掌握要求：熟练
# 本文件：学习模块概念、两种导入写法、__name__ 入口与导入缓存，并真实导入同目录的 study_tools。

import math
import sys

import study_tools        # 第一次导入：执行 study_tools 的顶层代码，打印加载提示

# ==================== 13.4.1 什么是模块 ====================
# 一个 .py 文件就是一个模块，模块名是去掉 .py 的文件名；模块中的函数和变量都能被导入使用。
# 标准库模块与自定义模块的用法完全一致：先导入，再通过模块名访问其中的名字。
print(f"math 的模块名：{math.__name__}")                 # -> math 的模块名：math
print(f"study_tools 的模块名：{study_tools.__name__}")    # -> study_tools 的模块名：study_tools
print(f"当前脚本的 __name__：{__name__}")                 # -> 当前脚本的 __name__：__main__

# 直接运行脚本时 __name__ 是 "__main__"，被导入时是模块名，这一点在 13.4.3 会用到。
# // C++: #include 在编译期把声明拼进当前文件；import 在运行时查找并加载一个模块对象。

# ==================== 13.4.2 import 与 from ... import ... ====================
# import 模块名：使用时写 模块名.函数名，来源清楚，重名风险低。
print(study_tools.calc_area(2.5, 4.0))                     # -> 10.0

# from 模块名 import 函数名：直接使用函数名，适合频繁调用的少量名字。
from study_tools import round_price
print(round_price(12.3489))                                # -> 12.35

# as 起别名：模块名较长或与已有名字冲突时使用。
import study_tools as tools
print(tools.round_price(0.9876, 1))                        # -> 1.0

# 模块提供 __all__ 时，可以用 * 导入限定范围内的名字，但正式代码仍不推荐 import *。
print(f"study_tools 公开的接口：{study_tools.__all__}")    # -> study_tools 公开的接口：['calc_area', 'round_price', 'split_evenly']

# 自定义模块不需要安装，只要文件位于可搜索的目录中即可导入。
# 运行脚本时，脚本所在目录会自动加入 sys.path[0]，
# 因此 13.4_modules.py 与 study_tools.py 放在同一目录就能直接导入，与当前工作目录无关。
# // C++: 第三方库需要通过包管理器或头文件路径配置，Python 只需模块在搜索路径中。

# ==================== 13.4.3 自定义模块与导入缓存 ====================
# 模块第一次导入后会被放进 sys.modules；再次导入直接复用，不会重复执行顶层代码。
import study_tools        # 第二次导入：不会再打印“模块被首次加载”

print(f"模块是否已缓存：{'study_tools' in sys.modules}")   # -> 模块是否已缓存：True
# 开发时改了模块代码，需要重启解释器或使用 importlib.reload 才能看到新内容。
# // C++: 修改头文件后重新编译即可；Python 的模块缓存属于运行时状态。

# study_tools.py 末尾有 if __name__ == "__main__": 代码块：
# 直接运行 study_tools.py 时，__name__ 是 "__main__"，演示代码会执行；
# 被本文件导入时，__name__ 是 "study_tools"，演示代码被跳过，因此上面没有出现演示输出。
print(f"study_tools 的 __name__：{study_tools.__name__}")   # -> study_tools 的 __name__：study_tools

# 常见坑点：
# 1. 用标准库同名文件，例如在项目目录建 random.py 或 math.py。
#    现象：import random 导入的是自己的文件，标准库函数全部找不到。
#    原因：脚本所在目录在 sys.path 中优先于标准库目录。
#    正确做法：模块文件使用带业务含义的名字，例如 my_random、study_tools。
# 2. 两个模块互相 import，形成循环导入。
#    现象：导入时报 ImportError 或部分名字为 None。
#    原因：模块在加载过程中又被对方导入，还没执行完。
#    正确做法：把公共依赖抽到第三个模块，或在函数内部延迟导入。
# 3. 在模块顶层写测试代码或耗时操作。
#    现象：导入该模块的程序多出输出或启动变慢。
#    原因：模块顶层代码在第一次导入时必定执行。
#    正确做法：测试代码放进 if __name__ == "__main__": 代码块。
# 4. 使用 from 模块 import * 覆盖已有名字。
#    现象：同名变量或函数被悄悄替换，难以排查。
#    原因：星号导入把多个名字放进当前命名空间。
#    正确做法：明确写出需要的名字，或坚持 import 模块名后加前缀。
# 5. 修改了模块代码但运行结果没有变化。
#    现象：仍然执行旧逻辑。
#    原因：sys.modules 中缓存的模块对象不会自动更新。
#    正确做法：重启解释器；交互环境可用 importlib.reload(module)。
