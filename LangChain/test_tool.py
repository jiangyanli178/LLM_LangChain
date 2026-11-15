from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:  #需要告诉schema类型提示,函数名默认就是add
    #还需要字符串文档,否则报错,原因是过不了schema校验
    # 推荐谷歌风格文档字符串
    #方法描述 参数 返回值
    """两数相加

    args:
        a: 第一个整数
        b: 第二个整数

    returns:
        返回一个整数
    """
    return a+b

print(add.invoke({"a": 1, "b": 2}))