// langchain
import {
  type InitializeAgentExecutorOptions,
  initializeAgentExecutorWithOptions,
  type AgentExecutor,
} from 'langchain/agents';
import { type BaseLanguageModel } from 'langchain/dist/base_language';
import {
  BaseCallbackHandler,
  type NewTokenIndices,
} from 'langchain/dist/callbacks';
import { type Tool } from 'langchain/dist/tools/base';
import { type ServerMessage } from '../../types';

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

  async initAgentWithWebSocket(socket: WebSocket): Promise<AgentExecutor> {
    return await initializeAgentExecutorWithOptions(
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
    const message: ServerMessage = {
      content: token,
    };
    this.websocket.send(JSON.stringify(message));
  }
}
