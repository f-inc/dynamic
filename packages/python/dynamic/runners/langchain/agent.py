from dataclasses import dataclass
from typing import Any, Union, Dict

# dyanmic
from dynamic.runners.runner import Runner

# langchain
from langchain.agents import Agent, AgentExecutor

@dataclass
class AgentConfig:
    agent_input: Union[str, Dict[str, str]]

class AgentRunner(Runner):
    def __init__(self, handle: Union[Agent, AgentExecutor], config: AgentConfig):
        if not (isinstance(handle, Agent) or isinstance(handle, AgentExecutor)):
            raise ValueError(f"AgentRunner requires handle to be a Langchain Agent or AgentExecutor. Instead got {type(handle)}.")
        
        super(AgentRunner, self).__init__(handle, config)

    def run(self):
        agent_input = self.config.agent_input
        return self.handle.run(agent_input)

if __name__ == "__main__":
    print("Importing deps...")
    from dotenv import load_dotenv

    load_dotenv()

    from langchain.agents import load_tools
    from langchain.agents import initialize_agent
    from langchain.agents import AgentType
    from langchain.llms import OpenAI
    from langchain.agents.agent_toolkits import NLAToolkit


    llm = OpenAI(
        client=None,
        temperature=0.9,
    )
    tools = NLAToolkit.from_llm_and_url(llm, "https://api.speak.com/openapi.yaml").get_tools()

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    agent_input = dict(input="What does \"donde esta la biblioteca?\" mean? And what is a way to respond to this?")
    config = AgentConfig(agent_input=agent_input)

    runner = AgentRunner(agent, config)

    print("Runner created and running...")
    print(runner.run())

