// dynamic
import { DynamicAgent } from "./../../../dynamic/src/dync/langchain/agent";

// fastify
import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Resource } from "fastify-autoroutes";

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
  new SerpAPI(undefined, {
    location: "San Francisco, California, USA",
    hl: "en",
    gl: "us",
  }),
  new Calculator(),
];

const agentHandler = async () => {
  return new DynamicAgent(tools, model, {
    agentType: "zero-shot-react-description",
    verbose: true,
  });
};

/** Define Route */

export default (fastify: FastifyInstance) =>
  <Resource>{
    get: {
      handler: () => null,
      wsHandler: agentHandler,
    },
  };
