export interface Config {
  input: any;
}

export abstract class Runner {
  config: Config;
  handle: any;

  constructor(config: Config, handle: any) {
    this.config = config;
    this.handle = handle;
  }

  abstract run(): void;

  abstract arun(): Promise<void>;
}
