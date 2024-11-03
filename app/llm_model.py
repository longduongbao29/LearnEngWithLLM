import os
from langchain_openai import ChatOpenAI

if "OPENAI_API_KEY" not in os.environ:
    print("API KEY does not exists!")
    
llm_openai =  ChatOpenAI(model="gpt-4o", temperature=0.5)

