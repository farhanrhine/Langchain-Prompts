# types of messages 
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(model='tinydolphin')

#inputs
messages=[
    SystemMessage(content='You are a helpful assistant'),
    HumanMessage(content='Tell me about LangChain')
]
# call the model
result = model.invoke(messages)
# convert the message as AI messsages
messages.append(AIMessage(content=result.content))

print(messages)

