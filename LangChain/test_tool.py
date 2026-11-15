from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:  #需要告诉schema类型提示,函数名默认就是add
    #还需要字符串文档,否则报错,原因是过不了schema校验
    """
    两数相加
    :param a: int
    :param b: int
    :return: int
    """
    return a+b

print(add.invoke({"a": 1, "b": 2}))