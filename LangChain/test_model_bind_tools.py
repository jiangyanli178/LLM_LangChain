from langchain.chat_models import init_chat_model
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from LangChain.test1 import deepseek_model


#普通版本
@tool
def add_test_one(a: int, b: int) -> int:
    #方法描述 参数 返回值
    """两数相加
    """
    return a+b
print(add_test_one.invoke({"a": 1, "b": 2}))

#添加参数的描述让LLM了解这个工具的参数是什么
@tool
def add_test_two(a:Annotated[int,...,"第一个整数"],
                 b:Annotated[int,...,"第二个整数"]) -> int :
    """两数之和
    """
    return a+b
print(add_test_two.invoke({"a":1,"b":2}))

#用pydantic中的BaseModel通过类来描述字符串文档
class AddInput(BaseModel):
    #对于字符串的描述
    """两数之和
    """
    #对于参数的描述
    a: int = Field(...,description="第一个整数")
    b: int = Field(...,description="第二个整数")
@tool(args_schema=AddInput)
def add_test_three(a: int, b: int) -> int:
    return a+b
print(add_test_three.invoke({"a": 1, "b": 2}))

#以及用LangChain提供的类来定义工具使用StructuredTool
#这里不需要再加@tool了
def add_test_four(a: int, b: int) -> int:
    return a+b
add_test_four_tool = StructuredTool.from_function(
    func = add_test_four,
    name="ADD",
    input_schema = AddInput,
    description= "两数之和"
)
print(add_test_four_tool.invoke({"a": 1, "b": 2}))

#如果还需要返回过程
def add_test_four(a: int, b: int) -> tuple[str, list[int]]:
    nums = [a,b]
    content = f"{nums}两数相加和为{a+b}"
    return content, nums
add_test_four_tool = StructuredTool.from_function(
    func = add_test_four,
    name="ADD",
    input_schema = AddInput,
    description= "两数之和",
    response_format= "content_and_artifact"  #设置工具调用返回的结果格式,这里是把结果和过程分开
)
print(add_test_four_tool.invoke({"a": 1, "b": 2}))
#设置了格式为过程结果分开后,过后需要使用大模型调用方式才能看见过程
print(add_test_four_tool.invoke({
    "name": "ADD",
    "args": {"a": 1, "b": 2},
    "type": "tool_call",
    "id": "111"
}))

#解决了定义工具,然后需要绑定工具
@tool(args_schema=AddInput)
def add_test_five(a: int, b: int) -> int:
    return a+b
@tool
def add_test_six(a: Annotated[int,...,"第一个整数"],
                  b: Annotated[int,...,"第二个整数"]) -> int:
    """两数相乘"""
    return a*b
deepseekModel = init_chat_model(model="deepseek-flash")
deepseekModel_tools = deepseekModel.bind_tools(tools = [add_test_five, add_test_six])
print(deepseekModel_tools.invoke("2+3和5*5分别等于多少"))#打印的其实是AIMessage,不是想要的答案
