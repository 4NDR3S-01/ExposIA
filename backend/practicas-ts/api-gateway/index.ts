import { ApolloServer, gql } from "apollo-server";
import axios from "axios";
import fs from "fs";

// Lee el schema desde el archivo
const typeDefs = gql(fs.readFileSync("./schema.graphql", { encoding: "utf-8" }));

// Implementa los resolvers
const resolvers = {
  Query: {
    resumenGrabacion: async (_: any, { id }: { id: number }) => {
      try {
        const response = await axios.get(`http://localhost:3000/debug/resumen/${id}`, {
          headers: {
            'Authorization': 'Bearer mi-token-seguro'
          }
        });
        
        const data = response.data;
        
        // Crear una copia limpia de los datos para evitar referencias circulares
        return {
          grabacion: data.grabacion ? { ...data.grabacion } : null,
          navegaciones: data.navegaciones ? data.navegaciones.map((nav: any) => ({ ...nav })) : [],
          fragmentos: data.fragmentos ? data.fragmentos.map((frag: any) => ({ ...frag })) : [],
          notas: data.notas ? data.notas.map((nota: any) => ({ ...nota })) : [],
          historial: data.historial ? { ...data.historial } : null
        };
      } catch (error) {
        console.error('Error al obtener resumen de grabación:', error);
        throw new Error('Error al obtener resumen de grabación');
      }
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 4000 }).then(({ url }) => {
  console.log(`🚀 API Gateway GraphQL listo en ${url}`);
});