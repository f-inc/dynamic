export interface Config {
  input: object | string;
}

export abstract class Runner {
  config: Config;
  handle: any;

  constructor(handle: any, config: Config) {
    this.handle = handle;
    this.config = config;
  }

  abstract run(): any;

  abstract arun(): any;
}
