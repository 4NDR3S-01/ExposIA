import { Context } from '../context';

export const presentacionResolvers = {
  Query: {
    presentaciones: async (_, __, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentaciones();
    },
    
    presentacion: async (_, { id }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacion(id);
    },
    
    presentacionesPorUsuario: async (_, { usuarioId }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacionesPorUsuario(usuarioId);
    },
    
    presentacionesPorTema: async (_, { temaId }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacionesPorTema(temaId);
    },
    
    temas: async (_, __, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getTemas();
    },
    
    tema: async (_, { id }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getTema(id);
    },
    
    slides: async (_, __, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getSlides();
    },
    
    slide: async (_, { id }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getSlide(id);
    },
    
    slidesPorPresentacion: async (_, { presentacionId }, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getSlidesPorPresentacion(presentacionId);
    },
  },

  Mutation: {
    crearTema: async (_, { input }, { dataSources, notificationService }: Context) => {
      const tema = await dataSources.presentacionesAPI.crearTema(input);
      
      await notificationService.enviarNotificacion('tema.creado', {
        id: tema.id,
        nombre: tema.nombre
      });
      
      return tema;
    },
    
    crearPresentacion: async (_, { input }, { dataSources, notificationService }: Context) => {
      const presentacion = await dataSources.presentacionesAPI.crearPresentacion(input);
      
      await notificationService.enviarNotificacion('presentacion.creada', {
        id: presentacion.id,
        titulo: presentacion.titulo,
        usuarioId: presentacion.usuarioId,
        temaId: presentacion.temaId
      });
      
      return presentacion;
    },
  },

  Presentacion: {
    usuario: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getUsuario(parent.id_usuario || parent.usuarioId);
    },
    
    tema: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getTema(parent.id_tema || parent.temaId);
    },
    
    slides: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getSlidesPorPresentacion(parent.id);
    },
    
    calificaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.calificacionAPI.getCalificacionesPorPresentacion(parent.id);
    },
    
    grabaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getGrabacionesPorPresentacion(parent.id);
    },
  },

  Tema: {
    presentaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacionesPorTema(parent.id);
    },
  },

  Slide: {
    presentacion: async (parent, _, { dataSources }: Context) => {
      return await dataSources.presentacionesAPI.getPresentacion(parent.id_presentacion || parent.presentacionId);
    },
    
    navegaciones: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getNavegacionesPorSlide(parent.id);
    },
    
    notas: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getNotasPorSlide(parent.id);
    },
    
    fragmentosAudio: async (parent, _, { dataSources }: Context) => {
      return await dataSources.practicasAPI.getFragmentosPorSlide(parent.id);
    },
  },
};