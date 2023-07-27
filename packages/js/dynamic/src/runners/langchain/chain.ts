import { Runner, type Config } from '../types';

import { BaseChain } from 'langchain/dist/chains/base';

export class ChainRunner extends Runner {
  constructor(handle: BaseChain, config: Config) {
    if (!(handle instanceof BaseChain)) {
      throw new Error(`"handle" expected BaseChain, recieved ${typeof handle}`);
    }

    super(handle, config);
  }

  run(): void {
    const { input } = this.config;
    return this.handle.run(input);
  }

  async arun(): Promise<void> {
    throw new Error('Method not implemented.');
  }
}
