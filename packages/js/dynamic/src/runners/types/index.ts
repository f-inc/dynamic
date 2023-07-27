export interface Config {
  input: object | string;
}

export abstract class Runner {
  config: Config;
  handle: any;

  constructor(handle: any, config: Config) {
    this.config = config;
    this.handle = handle;
  }

  abstract run(): any;

  abstract arun(): any;
}
