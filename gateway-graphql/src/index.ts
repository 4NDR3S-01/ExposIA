import express from 'express';
import { ApolloServer } from 'apollo-server-express';
import cors from 'cors';
import dotenv from 'dotenv';
import { typeDefs } from './schema/typeDefs';
import { resolvers } from './resolvers';
import { createContext } from './context';

dotenv.config();

async function startServer() {
  const app = express();
  
  // Configurar CORS
  app.use(cors({
    origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000'],
    credentials: true
  }));

  // Crear servidor Apollo
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: createContext,
    introspection: true,
    playground: true,
  });

  await server.start();
  server.applyMiddleware({ app, path: '/graphql' });

  // Health check endpoint
  app.get('/health', (req, res) => {
    res.json({ 
      status: 'healthy', 
      service: 'ExposIA Gateway GraphQL',
      timestamp: new Date().toISOString()
    });
  });

  const PORT = process.env.PORT || 4000;
  
  app.listen(PORT, () => {
    console.log(`🚀 Gateway GraphQL corriendo en http://localhost:${PORT}${server.graphqlPath}`);
    console.log(`📊 GraphQL Playground disponible en http://localhost:${PORT}${server.graphqlPath}`);
  });
}

startServer().catch(error => {
  console.error('Error al iniciar el servidor:', error);
  process.exit(1);
});