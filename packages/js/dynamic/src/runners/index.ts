import { Runner } from './types';

class CallableRunner extends Runner {
  run(): any {
    const { config, handle } = this;
    return handle(config.input);
  }

  async arun(): Promise<void> {
    throw new Error('Method not implemented.');
  }
}

export { CallableRunner };
