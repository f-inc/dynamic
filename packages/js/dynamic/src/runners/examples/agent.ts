/**
 * File has issue with SerpAPI, issue filed here: https://github.com/hwchase17/langchainjs/issues/2118
 * Until then, hold off on using this example script.
 */
import 'dotenv/config';

import { type Config } from '../types';
import { AgentRunner } from '../langchain';

import { OpenAI } from 'langchain';
import { initializeAgentExecutorWithOptions } from 'langchain/agents';
import { SerpAPI } from 'langchain/tools';
import { Calculator } from 'langchain/tools/calculator';

// Langchain Setup
const llm = new OpenAI({
  temperature: 0,
  //   verbose: true,
});
const tools = [
  new SerpAPI(process.env.SERPAPI_API_KEY, {
    location: 'San Francisco, California, USA',
    hl: 'en',
    gl: 'us',
  }),
  new Calculator(),
];

initializeAgentExecutorWithOptions(tools, llm, {
  agentType: 'zero-shot-react-description',
  verbose: true,
}).then((agent) => {
  console.log(agent);
  const input = 'Who is the US President? What is age squared?';
  const config: Config = { input };
  const runner = new AgentRunner(agent, config);
  runner.run().then((val: any) => {
    console.log('Agent Output:', val);
  });
});

// const onFullfilled = (val: AgentExecutor) => val;
// const onRejection = (reason: any): any => console.log('reason', reason);
// agent = agent.then(onFullfilled, onRejection);

// Dynamic
