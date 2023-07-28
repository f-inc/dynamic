// dynamic
import { Runner, type Config } from '../types';
import { DynamicAgent } from '../../dync/langchain/agent';
import { type AgentExecutor } from 'langchain/agents';

export class AgentRunner extends Runner {
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
      if (!(handle instanceof DynamicAgent)) {
        throw new Error(
          `"handle" expected DynamicAgent, recieved ${typeof handle}`
        );
      }
      if (websocket == null) {
        throw new Error(
          'DynamicAgent marked as `streaming` without a websocket.'
        );
      }
      this.handle = handle.initAgentWithWebSocket(websocket);
      this.streaming = true;
    }
  }

  run(): any {
    const { input } = this.config;
    return this.handle.run(input);
  }

  async arun(): Promise<any> {
    if (!this.streaming) {
      throw new Error(
        'This is not a streaming agent, please use run() and not arun().'
      );
    }

    const { input } = this.config;
    return this.handle.arun(input);
  }
}
