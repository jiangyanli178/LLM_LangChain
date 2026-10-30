from langchain.chat_models import init_chat_model

deepseek_model = init_chat_model("deepseek_model",model_provider="deepseek")

print(deepseek_model.invoke("你是谁?").content)