from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from prompts import prompt_vi, prompt_en
from llm_model import llm_openai
from agent_tools import save_vocab, check_vocab_exists, load_vocabs_for_review, load_all_vocabs, get_current_datetime

LANG_PROMPT = {
    "English": prompt_en,
    "Tiếng Việt" : prompt_vi
}

class Agent:
  
    def __init__(self) -> None:
        self.prompt=prompt_en
        self.tools = [save_vocab, check_vocab_exists,  load_vocabs_for_review, load_all_vocabs, get_current_datetime]      
        self.agent = create_tool_calling_agent(llm_openai, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        self.current_lang = "English"
    
    def switch_lang(self,lang):
        if lang != self.current_lang:
            self.current_lang = lang
            self.prompt = LANG_PROMPT[lang]
            self.agent = create_tool_calling_agent(llm_openai, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
