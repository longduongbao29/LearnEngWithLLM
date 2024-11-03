
from agent import agent_executor
from langchain_core.messages import AIMessage, HumanMessage

inp = {}
chat_history = []
while True:
    inp["input"] = input("You: ")
    inp["chat_history"] = chat_history
    response = agent_executor.invoke(inp)
    chat_history.append(HumanMessage(content=inp["input"]))
    chat_history.append(AIMessage(content=str(response["output"])))
    print(f"Agent: {response['output']}")