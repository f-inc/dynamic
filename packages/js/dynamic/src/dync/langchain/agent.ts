// langchain
import {
  InitializeAgentExecutorOptions,
  initializeAgentExecutorWithOptions,
} from 'langchain/agents';
import { BaseLanguageModel } from 'langchain/dist/base_language';
import { Tool } from 'langchain/dist/tools/base';

export class DynamicAgent {
  tools: Tool[];
  llm: BaseLanguageModel;
  options: InitializeAgentExecutorOptions;

  constructor(
    tools: Tool[],
    llm: BaseLanguageModel,
    options: InitializeAgentExecutorOptions
  ) {
    this.tools = tools;
    this.llm = llm;
    this.options = options;
  }

  initAgentWithWebSocket(socket: WebSocket) {
    return initializeAgentExecutorWithOptions(
      this.tools,
      this.llm,
      this.options
    );
  }
}
