const { ApolloServer } = require('apollo-server');
const fs = require('fs');
const path = require('path');
const resolvers = require('./resolvers');
require('dotenv').config();

// Cargar el esquema GraphQL
const typeDefs = fs.readFileSync(path.join(__dirname, 'schema.graphql'), 'utf8');

// Configurar el servidor Apollo
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true, // Habilitar introspección para GraphQL Playground
  playground: true,    // Habilitar GraphQL Playground
  formatError: (error) => {
    // Log detallado de errores para debugging
    console.error('GraphQL Error:', {
      message: error.message,
      locations: error.locations,
      path: error.path,
      extensions: error.extensions
    });
    
    // Retornar error formateado para el cliente
    return {
      message: error.message,
      code: error.extensions?.code || 'INTERNAL_ERROR',
      path: error.path
    };
  },
  context: ({ req }) => {
    // Aquí puedes agregar contexto como autenticación
    return {
      headers: req.headers,
      timestamp: new Date().toISOString()
    };
  }
});

// Iniciar el servidor
const PORT = process.env.PORT || 4000;

server.listen({ port: PORT }).then(({ url }) => {
  console.log('🚀 ExposIA API Gateway iniciado!');
  console.log(`📡 GraphQL endpoint: ${url}`);
  console.log(`🎮 GraphQL Playground: ${url}`);
  console.log('🔗 Microservicios conectados:');
  console.log(`  📝 PHP (Presentaciones): ${process.env.PHP_API_URL || 'http://localhost:8001/api'}`);
  console.log(`  🎯 TypeScript (Prácticas): ${process.env.NEST_API_URL || 'http://localhost:3000'}`);
  console.log(`  🤖 Python (Feedback IA): ${process.env.PYTHON_API_URL || 'http://localhost:8000/api/v1'}`);
  console.log(`  ☕ Java (Calificaciones): ${process.env.JAVA_API_URL || 'http://localhost:8080/api'}`);
  console.log('✅ Gateway listo para recibir consultas!');
}).catch((error) => {
  console.error('❌ Error al iniciar el gateway:', error);
  process.exit(1);
});
