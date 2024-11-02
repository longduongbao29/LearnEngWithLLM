from llm_model import llm_openai
from prompts import prompt_learning,prompt_reviewing
from agent_tools import save_vocab, check_vocab_exists, load_vocabs_for_review, load_all_vocabs,switch_activity

tools = [save_vocab, check_vocab_exists,  load_vocabs_for_review, load_all_vocabs, switch_activity]      
llm_with_tools = llm_openai.bind_tools(tools)
def llm_invoke(input, activity = "Learning"):
    prompt = prompt_learning  
    if activity == "Reviewing":
        prompt = prompt_reviewing
    chains = prompt | llm_with_tools
    response = chains.invoke(input=input)
    return response