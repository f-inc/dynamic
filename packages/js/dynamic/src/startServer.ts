// fastify
import { type FastifyPluginCallback, type FastifyPluginAsync } from 'fastify'

// dynamic
import dynamic from './dynamic'

const DEFAULT_HOST: string = process.env.HOST ?? '0.0.0.0'
const DEFAULT_PORT: number = parseInt(process.env.PORT ?? '8000')

interface Plugins {
  callback: FastifyPluginCallback | FastifyPluginAsync
  options?: any
}

interface Server {
  plugins: Plugins[]
  host?: string
  port?: number
}

const startServer = (server: Server): void => {
  const { plugins } = server
  const host = server.host ?? DEFAULT_HOST
  const port = server.port ?? DEFAULT_PORT

  if (plugins != null) {
    // adding plugins - includes routes
    plugins.forEach(({ callback }) => {
      dynamic.register(callback)
    })
  }

  // Run the server!
  dynamic.listen({ host, port }, function (err, address) {
    if (err != null) {
      dynamic.log.error(err)
      process.exit(1)
    }
    console.log(`Server is now listening on ${address}`)
  })
}

export default startServer

export type { Plugins, Server }
