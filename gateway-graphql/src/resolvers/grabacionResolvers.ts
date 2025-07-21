import { Context } from '../context';

export const grabacionResolvers = {
  Query: {
    grabaciones: async (_, __, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabaciones();
    },
    
    grabacion: async (_, { id }, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacion(id);
    },
    
    grabacionesPorUsuario: async (_, { usuarioId }, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacionesPorUsuario(usuarioId);
    },
    
    grabacionesPorPresentacion: async (_, { presentacionId }, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacionesPorPresentacion(presentacionId);
    },
  },

  Mutation: {
    crearGrabacion: async (_, { input }, { dataSources, notificationService }: Context) => {
      const grabacion = await dataSources.practicasAPI.crearGrabacion(input);
      
      await notificationService.enviarNotificacion('grabacion.creada', {
        id: grabacion.id,
        usuarioId: grabacion.usuarioId,
        presentacionId: grabacion.presentacionId,
        nombreArchivo: grabacion.nombreArchivo
      });
      
      return grabacion;
    },
  },

  Grabacion: {
    usuario: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getUsuario(parent.usuario_id || parent.usuarioId);
    },
    
    presentacion: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacion(parent.presentacion_id || parent.presentacionId);
    },
    
    navegaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getNavegacionesPorGrabacion(parent.id);
    },
    
    fragmentos: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getFragmentosPorGrabacion(parent.id);
    },
    
    notas: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getNotasPorGrabacion(parent.id);
    },
    
    historial: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getHistorialPorGrabacion(parent.id);
    },
    
    feedbacks: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getFeedbacksPorGrabacion(parent.id);
    },
    
    calificaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacionesPorGrabacion(parent.id);
    },
  },
};