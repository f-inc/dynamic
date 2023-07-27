// dynamic
import { Runner, type Config } from '../types';
import { DynamicAgent } from '../../dync/langchain/agent';

export class AgentRunner extends Runner {
  streaming: boolean; // marker to indicate agent will stream its tokens

  constructor(
    handle: DynamicAgent,
    config: Config,
    websocket?: WebSocket,
    streaming?: boolean
  ) {
    super(handle, config);
    if (!(handle instanceof DynamicAgent)) {
      throw new Error(
        `"handle" expected DynamicAgent, recieved ${typeof handle}`
      );
    }
    if (streaming) {
      if (!websocket) {
        throw new Error(
          'DynamicAgent marked as `streaming` without a websocket.'
        );
      }
      this.handle = handle.initAgentWithWebSocket(websocket);
      this.streaming = true;
    } else {
      this.streaming = false;
    }
  }

  run() {
    const { input } = this.config;
    return this.handle.run(input);
  }

  async arun() {
    if (!this.streaming) {
      throw new Error(
        'This is not a streaming agent, please use run() and not arun().'
      );
    }

    const { input } = this.config;
    return await this.handle.arun(input);
  }
}
