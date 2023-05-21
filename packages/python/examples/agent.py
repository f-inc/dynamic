from dotenv import load_dotenv

load_dotenv()

from dynamic import start_server
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = OpenAI(
    client=None,
    temperature=0.9,
)
tools = load_tools([])

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if __name__ == "__main__":
    start_server(routes={"agent": agent})
