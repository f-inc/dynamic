import { DynamicAgent } from "dynamic/src/dync/langchain/agent";
import { wsRouteBuilder } from "dynamic/src/routing";

// langchain
import { type Tool } from "langchain/tools";
import { OpenAI } from "langchain/llms/openai";
import { SerpAPI } from "langchain/tools";
import { Calculator } from "langchain/tools/calculator";

/** Defined Agent */

const model = new OpenAI({
  temperature: 0,
  streaming: true,
  verbose: true,
});
const tools: Tool[] = [
  new SerpAPI(process.env.SERPAPI_API_KEY, {
    location: "San Francisco",
    hl: "en",
    gl: "us",
  }),
  new Calculator(),
];

const agent = new DynamicAgent(tools, model, {
  agentType: "zero-shot-react-description",
  verbose: true,
});

export default wsRouteBuilder(agent);
