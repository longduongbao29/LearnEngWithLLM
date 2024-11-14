from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate

llm_openai =  ChatOpenAI(model="o1-preview")

prompt = prompt_translating = PromptTemplate.from_template(
    """Yuu are a professor in math. Help user solve problem
Current conversation:  
{chat_history}
Input:  
{input}
""")

history = []
while 1:
    chain = prompt|llm_openai
    inp ={
        "input" : input("Human: "),
        "chat_history": history
    }

    output = chain.invoke(inp).content
    print("AI: ",output)
    history.append({
        "human" : inp["input"],
        "ai" : output
    })