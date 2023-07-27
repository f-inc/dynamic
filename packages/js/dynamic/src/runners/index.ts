import { Runner, type Config } from './types';

class CallableRunner extends Runner {
  constructor(handle: any, config: Config) {
    super(config, handle);
  }

  run(): any {
    const { config, handle } = this;
    return handle(config.input);
  }

  async arun(): Promise<void> {
    throw new Error('Method not implemented.');
  }
}

export { CallableRunner };
