import { Config } from '../types';
import { CallableRunner } from '..';

const add = ({ a, b }: { a: number; b: number }): number => a + b;

const config: Config = {
  input: {
    a: 1,
    b: 2,
  },
};

const runner = new CallableRunner(add, config);

console.log('runner.run(): ', runner.run());
