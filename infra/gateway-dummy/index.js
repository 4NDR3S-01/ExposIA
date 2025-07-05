// Gateway de prueba – responde con datos reales SOLO para Presentaciones

const { ApolloServer, gql } = require('apollo-server');
const fetch = require('node-fetch');

const REST_URL = process.env.REST_PRESENTACIONES_URL || 'http://localhost:8000';

const typeDefs = gql`
  type Presentation { id: ID! titulo: String! }
  type Query {
    presentations: [Presentation!]!
    ping: String
  }
`;

const resolvers = {
  Query: {
    ping: () => 'pong',
    presentations: () =>
      fetch(`${REST_URL}/presentaciones`).then(r => r.ok ? r.json() : []),
  },
};

new ApolloServer({ typeDefs, resolvers })
  .listen({ port: 4000 })
  .then(({ url }) => console.log(`⚗️  Dummy Gateway listo en ${url}`));
