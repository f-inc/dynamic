"""
Example Script
"""
import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import NLAToolkit

from dynamic.runners.langchain import AgentRunner, ChainRunnerConfig

if __name__ == "__main__":
    llm = OpenAI(
        client=None,
        temperature=0.9,
    )
    tools = NLAToolkit.from_llm_and_url(llm, "https://api.speak.com/openapi.yaml").get_tools()

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    agent_input = dict(input="What does \"donde esta la biblioteca?\" mean? And what is a way to respond to this?")
    config = ChainRunnerConfig(agent_input=agent_input)

    runner = AgentRunner(agent, config)

    print("Runner created and running...")
    asyncio.run(runner.run())