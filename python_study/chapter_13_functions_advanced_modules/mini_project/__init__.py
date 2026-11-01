"""mini_project 包：提供成绩统计工具与报表生成。"""

# 常见坑点：
# 1. 认为 __init__.py 必须写业务代码。
#    现象：导入包时出现不必要的计算或输出。
#    原因：__init__.py 在包第一次导入时执行。
#    正确做法：只放包说明或少量导出，业务逻辑放在具体模块中。
# 2. 把包内的 .py 文件当成顶层模块直接从包目录运行。
#    现象：相对导入抛出 ImportError: attempted relative import with no known parent package。
#    原因：直接运行时该文件没有父包，__package__ 为空。
#    正确做法：从包外导入包，或用 python -m mini_project.report 的方式运行。
# 3. 在 __init__.py 里提前导入所有子模块，造成启动变慢或循环导入。
#    现象：简单的 import mini_project 也触发大量加载。
#    原因：包的初始化代码会连带执行子模块的顶层代码。
#    正确做法：保持 __init__.py 轻量，需要什么就在使用处导入。
