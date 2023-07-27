import { Runner, Config } from '../types';

import { BaseChain } from 'langchain/dist/chains/base';

export class ChainRunner extends Runner {
  constructor(handle: BaseChain, config: Config) {
    super(handle, config);
  }
  run(): void {
    const { input } = this.config;
    return this.handle.run(input);
  }
  arun(): Promise<void> {
    throw new Error('Method not implemented.');
  }
}
