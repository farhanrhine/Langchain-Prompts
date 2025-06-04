# static prompt interact with messages.py for storeing previous messages

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

model = ChatOllama(model='tinydolphin')

chat_history = [
    SystemMessage(content="You are a helpful AI assistant. Answer questions clearly and concisely, in plain English.")

]

while True:
    user_input = input('You: ')
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'exit':
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)

print(chat_history)