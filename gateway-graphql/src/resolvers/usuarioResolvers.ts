import { Context } from '../context';

export const usuarioResolvers = {
  Query: {
    usuarios: async (_, __, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getUsuarios();
    },
    
    usuario: async (_, { id }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getUsuario(id);
    },
  },

  Mutation: {
    crearUsuario: async (_, { input }, { dataSources, notificationService }: Context) => {
      const usuario = await dataSources.presentacionesAPI.crearUsuario(input);
      
      // Enviar notificación
      await notificationService.enviarNotificacion('usuario.creado', {
        id: usuario.id,
        nombre: usuario.nombre,
        email: usuario.email
      });
      
      return usuario;
    },
  },

  Usuario: {
    presentaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacionesPorUsuario(parent.id);
    },
    
    calificaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacionesPorUsuario(parent.id);
    },
    
    grabaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacionesPorUsuario(parent.id);
    },
  },
};