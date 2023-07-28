import 'dotenv/config';

import { type Config } from '../types';
import { ChainRunner } from '../langchain';

import { LLMChain, OpenAI, PromptTemplate } from 'langchain';
// import { LLMChain } from 'langchain/chains';
// import { OpenAI } from 'langchain/llms';
// import { PromptTemplate } from 'langchain/prompts';

// Langchain Setup
const llm = new OpenAI({
  temperature: 0,
  verbose: true,
});

const prompt = PromptTemplate.fromTemplate(
  `You are a naming consultant for new companies. What is a good name for a company that makes {product}?`
);

const chain = new LLMChain({ llm, prompt });

// Dynamic Runner
const input = 'running shoes';
const config: Config = { input };

const runner: ChainRunner = new ChainRunner(chain, config);

console.log('Runner created and running...');
runner.run().then((output: any) => {
  console.log('Runner Output: ', output);
});
