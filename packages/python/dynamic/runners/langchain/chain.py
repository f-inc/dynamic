from dataclasses import dataclass
from typing import Any, Union, Dict

# dyanmic
from dynamic.runners.runner import Runner

# langchain
from langchain.chains.base import Chain


@dataclass
class ChainRunnerConfig:
    prompt_input: Union[str, Dict[str, str]]

class ChainRunner(Runner):
    def __init__(self, handle: Chain, config: ChainRunnerConfig):
        if not isinstance(handle, Chain):
            raise ValueError(f"ChainRunner requires handle to be a Langchain Chain. Instead got {type(handle)}.")
        
        super(ChainRunner, self).__init__(handle, config)
    
    def run(self):
        prompt_input = self.config.prompt_input
        return self.handle.run(prompt_input)
    
if __name__ == "__main__":
    print("Importing deps...")
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

    print("Testing Runner...")
    
    config = ChainRunnerConfig(prompt_input="running shoes")

    runner = ChainRunner(handle=chain, config=config)

    print("Runner created and running...")
    print(runner.run())