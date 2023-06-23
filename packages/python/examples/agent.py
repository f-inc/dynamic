from dotenv import load_dotenv

load_dotenv()

from dynamic import start_server
from langchain.agents import AgentType
from langchain.llms import OpenAI

from dynamic.classes.agent import DynamicAgent
from dynamic.router import Router, Route


llm = OpenAI(temperature=0, streaming=True, verbose=True)

tool_list = ["google-serper"]

agent = DynamicAgent(
    tool_list=tool_list, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

if __name__ == "__main__":
    router = Router(
        routes=[
            Route(
                handle=agent,
                streaming=True,
                path="agent",
            )
        ]
    )
    start_server(router=router, test_ws=True)
