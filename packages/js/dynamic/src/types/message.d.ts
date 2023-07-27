export interface BaseMessage {
  id?: string;
  content: string;
}

export interface ClientMessage extends BaseMessage {
  config: any;
}

export interface ServerMessage extends BaseMessage {}

export interface ErrorMessage extends BaseMessage {
  error: Error | string;
}
