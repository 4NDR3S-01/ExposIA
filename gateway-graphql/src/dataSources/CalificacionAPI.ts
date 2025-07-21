import axios, { AxiosInstance } from 'axios';

export class CalificacionAPI {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.CALIFICACION_API_URL || 'http://localhost:8080/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
      auth: {
        username: process.env.CALIFICACION_API_USER || 'admin',
        password: process.env.CALIFICACION_API_PASS || 'admin123'
      }
    });

    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Error en CalificacionAPI:', error.response?.data || error.message);
        throw error;
      }
    );
  }

  // Calificaciones
  async getCalificaciones() {
    try {
      const response = await this.api.get('/calificaciones');
      return response.data;
    } catch (error) {
      console.error('Error obteniendo calificaciones:', error);
      return [];
    }
  }

  async getCalificacion(id: string) {
    try {
      const response = await this.api.get(`/calificaciones/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error obteniendo calificación ${id}:`, error);
      return null;
    }
  }

  async getCalificacionesPorUsuario(usuarioId: string) {
    try {
      const calificaciones = await this.getCalificaciones();
      return calificaciones.filter((cal: any) => 
        (cal.usuario_id || cal.usuarioId) === parseInt(usuarioId)
      );
    } catch (error) {
      console.error(`Error obteniendo calificaciones del usuario ${usuarioId}:`, error);
      return [];
    }
  }

  async getCalificacionesPorGrabacion(grabacionId: string) {
    try {
      const calificaciones = await this.getCalificaciones();
      return calificaciones.filter((cal: any) => 
        (cal.grabacion_id || cal.grabacionId) === parseInt(grabacionId)
      );
    } catch (error) {
      console.error(`Error obteniendo calificaciones de la grabación ${grabacionId}:`, error);
      return [];
    }
  }

  async getCalificacionesPorPresentacion(presentacionId: string) {
    try {
      // Necesitamos obtener las grabaciones de esta presentación primero
      // y luego filtrar las calificaciones por esas grabaciones
      const calificaciones = await this.getCalificaciones();
      // Esto requeriría una consulta más compleja en un caso real
      return calificaciones;
    } catch (error) {
      console.error(`Error obteniendo calificaciones de la presentación ${presentacionId}:`, error);
      return [];
    }
  }

  // Detalles de calificación
  async getDetallesPorCalificacion(calificacionId: string) {
    try {
      const response = await this.api.get('/detalles');
      const detalles = response.data;
      return detalles.filter((det: any) => 
        (det.calificacion_id || det.calificacionId) === parseInt(calificacionId)
      );
    } catch (error) {
      console.error(`Error obteniendo detalles de la calificación ${calificacionId}:`, error);
      return [];
    }
  }

  async getDetallesPorCriterio(criterioId: string) {
    try {
      const response = await this.api.get('/detalles');
      const detalles = response.data;
      return detalles.filter((det: any) => 
        (det.criterio_id || det.criterioId) === parseInt(criterioId)
      );
    } catch (error) {
      console.error(`Error obteniendo detalles del criterio ${criterioId}:`, error);
      return [];
    }
  }

  // Criterios de evaluación
  async getCriterios() {
    try {
      const response = await this.api.get('/criterios');
      return response.data;
    } catch (error) {
      console.error('Error obteniendo criterios:', error);
      return [];
    }
  }

  async getCriterio(id: string) {
    try {
      const criterios = await this.getCriterios();
      return criterios.find((crit: any) => crit.id === parseInt(id));
    } catch (error) {
      console.error(`Error obteniendo criterio ${id}:`, error);
      return null;
    }
  }

  // Feedback de calificación
  async getFeedbacksPorCalificacion(calificacionId: string) {
    try {
      const response = await this.api.get('/feedback');
      const feedbacks = response.data;
      return feedbacks.filter((fb: any) => 
        (fb.calificacion_id || fb.calificacionId) === parseInt(calificacionId)
      );
    } catch (error) {
      console.error(`Error obteniendo feedbacks de la calificación ${calificacionId}:`, error);
      return [];
    }
  }
}