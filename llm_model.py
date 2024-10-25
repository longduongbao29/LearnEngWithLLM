# import getpass
import os
# from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# if "GROQ_API_KEY" not in os.environ:
#     os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    

# llm_groq = ChatGroq(
#     model="llama3-groq-70b-8192-tool-use-preview",
#     temperature=0.5,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

if "OPENAI_API_KEY" not in os.environ:
    print("API KEY does not exists!")
    
llm_openai =  ChatOpenAI(model="gpt-4o", temperature=1)