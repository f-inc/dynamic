from dotenv import load_dotenv

load_dotenv()

from dynamic import start_server
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler, StreamingStdOutCallbackHandler
)

from dynamic.classes.agent import DynamicAgent


llm = OpenAI(temperature=0, streaming=True, verbose=True)

tool_list = ["google-serper"]

agent = DynamicAgent(
    tool_list=tool_list, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

if __name__ == "__main__":
    start_server(routes={"agent": agent}, test_ws=True)
