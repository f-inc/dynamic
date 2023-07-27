import { type Config } from '../runners/types';

export interface BaseMessage {
  id?: string;
  content: string;
}

export interface ClientMessage extends BaseMessage {
  config: Config;
}

export interface ServerMessage extends BaseMessage {}

export interface ErrorMessage extends BaseMessage {
  error: Error | string;
}
