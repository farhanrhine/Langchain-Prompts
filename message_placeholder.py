from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. chat template
chat_template = ChatPromptTemplate([
    ('system','You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'), # this bring previous interactions messages in the current chat for context
    ('human','{query}')
])

chat_history = []
# 2. load chat history
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

print(chat_history)

# 3. create prompt
prompt = chat_template.invoke({'chat_history':chat_history, 'query':'Where is my refund'})

print(prompt)