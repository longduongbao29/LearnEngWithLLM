from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from prompts import prompt_learning,prompt_reviewing, prompt_practicing, prompt_translating, prompt_custom
from agent_tools import save_vocab, check_vocab_exists, load_all_vocabs
from langchain_community.tools import DuckDuckGoSearchRun
import os
from langchain_openai import ChatOpenAI

if "OPENAI_API_KEY" not in os.environ:
    print("API KEY does not exists!")
    


ACTIVITY_PROMPT = {
    "Learning": prompt_learning,
    "Reviewing" : prompt_reviewing,
    "Practicing" : prompt_practicing,
    "Translating" : prompt_translating,
    "Custom" : prompt_custom
}

MAX_ITER = 20
class Agent:
    def __init__(self) -> None:
        self.llm_openai =  ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0.8)
        self.prompt=prompt_learning
        search = DuckDuckGoSearchRun()
        self.tools = [save_vocab, search]      
        self.agent = create_tool_calling_agent(self.llm_openai, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, max_iterations= MAX_ITER)
        self.activity = "Learning"
    
    def switch_act(self,activity_):
        if activity_ != self.activity:
            self.activity = activity_
            self.prompt = ACTIVITY_PROMPT[activity_]
            self.create_agent()
    def llm_setting(self,model, temprature):
        self.llm_openai = ChatOpenAI(model=model, temperature=temprature)
        self.create_agent()
    def create_agent(self):
        self.agent = create_tool_calling_agent(self.llm_openai, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, max_iterations= MAX_ITER)