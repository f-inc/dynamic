// langchain
import {
  InitializeAgentExecutorOptions,
  initializeAgentExecutorWithOptions,
} from 'langchain/agents';
import { BaseLanguageModel } from 'langchain/dist/base_language';
import { BaseCallbackHandler, NewTokenIndices } from 'langchain/dist/callbacks';
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

export class WebSocketCallbackHandler extends BaseCallbackHandler {
  name = 'WebSocketCallbackHandler';
  websocket: WebSocket;

  constructor(websocket: WebSocket) {
    super();
    this.websocket = websocket;
  }

  async handleLLMNewToken(
    token: string,
    idx: NewTokenIndices,
    runId: string,
    parentRunId?: string | undefined,
    tags?: string[] | undefined
  ): Promise<void> {
    this.websocket.send(token);
  }
}
