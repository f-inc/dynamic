from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

from dynamic.runners.langchain.chain import ChainRunner, ChainRunnerConfig

load_dotenv()

if __name__ == "__main__":
    llm = OpenAI(
        client=None,
        temperature=0.9,
    )
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    print("Testing Runner...")
    
    config = ChainRunnerConfig(prompt_input="running shoes")

    runner = ChainRunner(handle=chain, config=config)

    print("Runner created and running...")
    print(runner.run())