import { Context } from '../context';

export const feedbackResolvers = {
  Query: {
    feedbacks: async (_, __, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getFeedbacks();
    },
    
    feedbacksPorGrabacion: async (_, { grabacionId }, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getFeedbacksPorGrabacion(grabacionId);
    },
    
    tiposMetrica: async (_, __, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getTiposMetrica();
    },
    
    metricas: async (_, __, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getMetricas();
    },
    
    parametros: async (_, __, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getParametros();
    },
  },

  Mutation: {
    crearFeedback: async (_, { input }, { dataSources, notificationService }: Context) => {
      const feedback = await dataSources.feedbackAPI.crearFeedback(input);
      
      await notificationService.enviarNotificacion('feedback.creado', {
        id: feedback.id,
        grabacionId: feedback.grabacionId,
        parametroId: feedback.parametroId,
        valor: feedback.valor,
        esManual: feedback.esManual
      });
      
      return feedback;
    },
  },

  Feedback: {
    grabacion: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacion(parent.grabacion_id || parent.grabacionId);
    },
    
    parametro: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getParametro(parent.parametro_id || parent.parametroId);
    },
  },

  Parametro: {
    metrica: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getMetrica(parent.metrica_id || parent.metricaId);
    },
    
    feedbacks: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getFeedbacksPorParametro(parent.id);
    },
  },

  Metrica: {
    tipoMetrica: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getTipoMetrica(parent.tipo_metrica_id || parent.tipoMetricaId);
    },
    
    parametros: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getParametrosPorMetrica(parent.id);
    },
  },

  TipoMetrica: {
    metricas: async (parent, _, { dataSources }: Context) => {
      return await dataSources.feedbackAPI.getMetricasPorTipo(parent.id);
    },
  },
};