import { FastifyPluginCallback, FastifyInstance } from 'fastify'
import fp from 'fastify-plugin'

const homeRoute: FastifyPluginCallback = (dynamic: FastifyInstance, opts, done) => {
    dynamic.get('/', (request, reply) => {
        reply.send("Hello World")
    })

    done()
}

export default fp(homeRoute)