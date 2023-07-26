import { Config } from '../types';
import { CallableRunner } from '..';

const add = (a: number, b: number) => a + b;

const config: Config = {
  input: {
    a: 1,
    b: 2,
  },
};

const runner = new CallableRunner(config, add);

console.log('runner.run(): ', runner.run());
