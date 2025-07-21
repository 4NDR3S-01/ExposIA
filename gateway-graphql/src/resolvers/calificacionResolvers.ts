import { Context } from '../context';

export const calificacionResolvers = {
  Query: {
    calificaciones: async (_, __, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificaciones();
    },
    
    calificacion: async (_, { id }, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacion(id);
    },
    
    calificacionesPorUsuario: async (_, { usuarioId }, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacionesPorUsuario(usuarioId);
    },
    
    calificacionesPorGrabacion: async (_, { grabacionId }, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacionesPorGrabacion(grabacionId);
    },
  },

  Mutation: {
    // Las calificaciones se crean desde el módulo Java, aquí solo consultamos
  },

  Calificacion: {
    usuario: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getUsuario(parent.usuario_id || parent.usuarioId);
    },
    
    grabacion: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacion(parent.grabacion_id || parent.grabacionId);
    },
    
    detalles: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getDetallesPorCalificacion(parent.id);
    },
    
    feedbacks: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getFeedbacksPorCalificacion(parent.id);
    },
  },

  DetalleCalificacion: {
    calificacion: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacion(parent.calificacion_id || parent.calificacionId);
    },
    
    criterio: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCriterio(parent.criterio_id || parent.criterioId);
    },
  },

  CriterioEvaluacion: {
    detalles: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getDetallesPorCriterio(parent.id);
    },
  },

  FeedbackCalificacion: {
    calificacion: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacion(parent.calificacion_id || parent.calificacionId);
    },
  },
};