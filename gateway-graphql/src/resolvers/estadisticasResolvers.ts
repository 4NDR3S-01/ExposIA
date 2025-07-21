import { Context } from '../context';

export const estadisticasResolvers = {
  Query: {
    estadisticasGenerales: async (_, __, { dataSources }: Context) => {
      try {
        // Obtener datos de todos los servicios
        const [usuarios, presentaciones, grabaciones, calificaciones] = await Promise.all([
          dataSources.presentacionesAPI.getUsuarios(),
          dataSources.presentacionesAPI.getPresentaciones(),
          dataSources.practicasAPI.getGrabaciones(),
          dataSources.calificacionAPI.getCalificaciones(),
        ]);

        // Calcular promedio de calificaciones
        const promedioCalificaciones = calificaciones.length > 0
          ? calificaciones.reduce((sum, cal) => sum + (cal.puntaje_global || cal.puntajeGlobal || 0), 0) / calificaciones.length
          : 0;

        // Agrupar presentaciones por tema
        const temas = await dataSources.presentacionesAPI.getTemas();
        const presentacionesPorTema = temas.map(tema => {
          const presentacionesDelTema = presentaciones.filter(p => 
            (p.id_tema || p.temaId) === tema.id
          );
          
          // Calcular promedio de calificaciones para este tema
          const calificacionesDelTema = calificaciones.filter(cal => {
            const grabacionesDelTema = grabaciones.filter(grab => 
              presentacionesDelTema.some(pres => pres.id === (grab.presentacion_id || grab.presentacionId))
            );
            return grabacionesDelTema.some(grab => grab.id === (cal.grabacion_id || cal.grabacionId));
          });
          
          const promedioTema = calificacionesDelTema.length > 0
            ? calificacionesDelTema.reduce((sum, cal) => sum + (cal.puntaje_global || cal.puntajeGlobal || 0), 0) / calificacionesDelTema.length
            : 0;

          return {
            tema,
            cantidad: presentacionesDelTema.length,
            promedioCalificacion: promedioTema
          };
        });

        // Actividad reciente (últimas 10 actividades)
        const actividadReciente = [
          ...presentaciones.slice(-5).map(p => ({
            tipo: 'PRESENTACION_CREADA',
            descripcion: `Nueva presentación: ${p.titulo}`,
            fecha: p.created_at || p.createdAt || new Date(),
            usuarioId: p.id_usuario || p.usuarioId,
            entidadId: p.id
          })),
          ...grabaciones.slice(-5).map(g => ({
            tipo: 'GRABACION_CREADA',
            descripcion: `Nueva grabación: ${g.nombre_archivo || g.nombreArchivo}`,
            fecha: g.created_at || g.createdAt || new Date(),
            usuarioId: g.usuario_id || g.usuarioId,
            entidadId: g.id
          }))
        ].sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime()).slice(0, 10);

        return {
          totalUsuarios: usuarios.length,
          totalPresentaciones: presentaciones.length,
          totalGrabaciones: grabaciones.length,
          totalCalificaciones: calificaciones.length,
          promedioCalificaciones,
          presentacionesPorTema,
          actividadReciente
        };
      } catch (error) {
        console.error('Error obteniendo estadísticas:', error);
        return {
          totalUsuarios: 0,
          totalPresentaciones: 0,
          totalGrabaciones: 0,
          totalCalificaciones: 0,
          promedioCalificaciones: 0,
          presentacionesPorTema: [],
          actividadReciente: []
        };
      }
    },
  },
};