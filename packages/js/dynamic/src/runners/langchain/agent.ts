// dynamic
import { Runner, type Config } from '../types';
import { DynamicAgent } from '../../dync/langchain/agent';
import { type AgentExecutor } from 'langchain/agents';

export class AgentRunner extends Runner {
  websocket?: WebSocket;
  streaming: boolean; // marker to indicate agent will stream its tokens

  constructor(
    handle: DynamicAgent | AgentExecutor,
    config: Config,
    websocket?: WebSocket,
    streaming?: boolean
  ) {
    super(handle, config);
    this.streaming = streaming ?? false;
    if (this.streaming) {
      if (!(this.handle instanceof DynamicAgent)) {
        throw new Error(
          `"handle" expected DynamicAgent, recieved ${typeof this.handle}`
        );
      }
      if (websocket == null) {
        throw new Error(
          'DynamicAgent marked as `streaming` without a websocket.'
        );
      }
      this.streaming = true;
      this.websocket = websocket;
    }
  }

  run(): any {
    const { input } = this.config;
    return this.handle.run(input);
  }

  async arun(): Promise<any> {
    const { streaming, websocket } = this;
    if (!(websocket && streaming) || !(this.handle instanceof DynamicAgent)) {
      throw new Error(
        'This is not a streaming agent, please use run() and not arun().'
      );
    }
    const handle = await this.handle.initAgentWithWebSocket(websocket);

    const { input } = this.config;
    return await handle.run(input);
  }
}
