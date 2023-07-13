from dotenv import load_dotenv

load_dotenv()

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from langchain.chains import LLMChain

llm = OpenAI(
    client=None,
    temperature=0.9,
)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)