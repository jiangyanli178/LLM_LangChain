from langchain_core.tools import tool
from typing_extensions import Annotated


#添加参数的描述让LLM了解这个工具的参数是什么
@tool
def add_test_one(a:Annotated[int,...,"第一个整数"],
                 b:Annotated[int,...,"第二个整数"]) -> int :
    """
     两数之和
    """
    return a+b


print(add_test_one.invoke({"a":1,"b":2}))