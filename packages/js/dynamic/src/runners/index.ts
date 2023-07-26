import { Runner, Config } from './types';

class CallableRunner extends Runner {
  constructor(config: Config, handle: any) {
    super(config, handle);
  }
  run(): void {
    const { config, handle } = this;
    return handle(config.input);
  }
  arun(): Promise<void> {
    throw new Error('Method not implemented.');
  }
}

export { CallableRunner };
