from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from prompts import prompt_learning,prompt_reviewing, prompt_practicing
from llm_model import llm_openai
from agent_tools import save_vocab, check_vocab_exists, load_vocabs_for_review, load_all_vocabs
from langchain_community.tools import DuckDuckGoSearchRun
ACTIVITY_PROMPT = {
    "Learning": prompt_learning,
    "Reviewing" : prompt_reviewing,
    "Practicing" : prompt_practicing
}

class Agent:
  
    def __init__(self) -> None:
        self.prompt=prompt_learning
        search = DuckDuckGoSearchRun()
        self.tools = [save_vocab, check_vocab_exists,  load_vocabs_for_review, load_all_vocabs,search]      
        self.agent = create_tool_calling_agent(llm_openai, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools)
        self.activity = "Learning"
    
    def switch_act(self,activity_):
        if activity_ != self.activity:
            self.activity = activity_
            self.prompt = ACTIVITY_PROMPT[activity_]
            self.agent = create_tool_calling_agent(llm_openai, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools)
