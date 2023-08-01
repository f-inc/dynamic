// langchain
import {
  type InitializeAgentExecutorOptions,
  initializeAgentExecutorWithOptions,
  type AgentExecutor,
} from 'langchain/agents';
import { type BaseLanguageModel } from 'langchain/base_language';
import { BaseCallbackHandler, type NewTokenIndices } from 'langchain/callbacks';
import type { Tool } from 'langchain/tools';
import { type ServerMessage } from '../../types';
import BaseDync from '..';

export class DynamicAgent extends BaseDync {
  tools: Tool[];
  llm: BaseLanguageModel;
  options: InitializeAgentExecutorOptions;

  constructor(
    tools: Tool[],
    llm: BaseLanguageModel,
    options: InitializeAgentExecutorOptions
  ) {
    super();
    this.tools = tools;
    this.llm = llm;
    this.options = options;
  }

  async initAgentWithWebSocket(socket: WebSocket): Promise<AgentExecutor> {
    if (!('streaming' in this.llm)) {
      throw new Error(
        'LLM has not been declared as streaming, make sure you add the `streaming` option to your llm instance, if possible.'
      );
    }

    const wsCallbackHandler = new WebSocketCallbackHandler(socket);
    this.llm.callbacks = [wsCallbackHandler];

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
