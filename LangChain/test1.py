from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv("../.env")
deepseek_model = init_chat_model("deepseek-flash",
                                 model_provider="deepseek",
                                 temperature = 0.3)
print(deepseek_model.invoke("你是谁?").content)

# 定义模型模拟器,init也就是初始化的意思
config_model = init_chat_model(temperature = 0.3)
# messages = [
#     SystemMessage(content = "请补全一段故事,20字以内"),
#     HumanMessage(content = "一只猫正在__?")
# ]
# # .invoke()的config参数才真正意义商定义了模型
# config_model.invoke(input = messages,config={"configurable":{"model":"deepseek-flash"}})
print(config_model.invoke(input = messages,
                          config={"configurable":{"model":"deepseek-flash"}}).content)

test_model = init_chat_model(model = "deepseek-flash",
                             model_provider="deepseek",
                             temperature = 0.3,
                             max_tokens = 1024,
                             # 需要使用invoke方法里面的config来修改参数时,已经定好的参数修改不了,需要使用以下参数来定义需要放行的参数
                             # 另外这里逗号不能去,去除了python就会认为这不是一个元组,是一个字符串
                             configurable_fields = ("max_tokens",),
                             # 定义完需要放行的参数后,还需要给他加上一个头字段用于区分,头字段自己写看得懂就行
                             config_prefix = "first"
                             )
print(test_model.invoke(input = messages,
                        config={
                            "configurable":{"first_max_tokens":1000},
                        }
                        ).content)
