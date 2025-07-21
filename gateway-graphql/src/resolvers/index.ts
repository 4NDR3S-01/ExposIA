import { usuarioResolvers } from './usuarioResolvers';
import { presentacionResolvers } from './presentacionResolvers';
import { grabacionResolvers } from './grabacionResolvers';
import { feedbackResolvers } from './feedbackResolvers';
import { calificacionResolvers } from './calificacionResolvers';
import { estadisticasResolvers } from './estadisticasResolvers';
import { DateTime } from 'graphql-scalars';

export const resolvers = {
  DateTime,
  
  Query: {
    // Health check
    ping: () => 'pong - ExposIA Gateway funcionando!',
    
    // Usuarios
    ...usuarioResolvers.Query,
    
    // Presentaciones
    ...presentacionResolvers.Query,
    
    // Grabaciones
    ...grabacionResolvers.Query,
    
    // Feedback
    ...feedbackResolvers.Query,
    
    // Calificaciones
    ...calificacionResolvers.Query,
    
    // Estadísticas
    ...estadisticasResolvers.Query,
  },

  Mutation: {
    // Usuarios
    ...usuarioResolvers.Mutation,
    
    // Presentaciones
    ...presentacionResolvers.Mutation,
    
    // Grabaciones
    ...grabacionResolvers.Mutation,
    
    // Feedback
    ...feedbackResolvers.Mutation,
    
    // Calificaciones
    ...calificacionResolvers.Mutation,
    
    // Notificaciones de prueba
    enviarNotificacionPrueba: async (_, { mensaje }, { notificationService }) => {
      try {
        await notificationService.enviarNotificacion('test', { mensaje });
        return true;
      } catch (error) {
        console.error('Error enviando notificación:', error);
        return false;
      }
    },
  },

  // Resolvers de tipos
  Usuario: usuarioResolvers.Usuario,
  Presentacion: presentacionResolvers.Presentacion,
  Grabacion: grabacionResolvers.Grabacion,
  Feedback: feedbackResolvers.Feedback,
  Calificacion: calificacionResolvers.Calificacion,
};