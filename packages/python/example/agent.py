
import logging
from typing import Union
from dotenv import load_dotenv
from langchain.schema import AgentAction, AgentFinish

load_dotenv()

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from dynamic.classes.dynamic_agent  import DynamicAgent


llm = OpenAI(temperature=0, streaming=True, verbose=True)

tool_list = ["google-serper"]

inline_agent = initialize_agent(
    tools=load_tools(tool_list), llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

streaming_agent = DynamicAgent(
    tool_list=tool_list, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chat_llm = ChatOpenAI(temperature=0, streaming=True)

chat_agent = DynamicAgent(
    tool_list=tool_list,
    llm=chat_llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)