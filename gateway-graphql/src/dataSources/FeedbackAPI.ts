import axios, { AxiosInstance } from 'axios';

export class FeedbackAPI {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.FEEDBACK_API_URL || 'http://localhost:8000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.FEEDBACK_API_KEY || 'test-api-key-12345'}`
      }
    });

    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Error en FeedbackAPI:', error.response?.data || error.message);
        throw error;
      }
    );
  }

  // Feedbacks
  async getFeedbacks() {
    try {
      const response = await this.api.get('/feedbacks');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo feedbacks:', error);
      return [];
    }
  }

  async getFeedbacksPorGrabacion(grabacionId: string) {
    try {
      const response = await this.api.get(`/feedbacks/grabacion/${grabacionId}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo feedbacks de la grabación ${grabacionId}:`, error);
      return [];
    }
  }

  async getFeedbacksPorParametro(parametroId: string) {
    try {
      const response = await this.api.get(`/feedbacks/parametro/${parametroId}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo feedbacks del parámetro ${parametroId}:`, error);
      return [];
    }
  }

  async crearFeedback(input: any) {
    try {
      const response = await this.api.post('/feedbacks', {
        grabacion_id: input.grabacionId,
        parametro_id: input.parametroId,
        valor: input.valor,
        comentario: input.comentario,
        es_manual: input.esManual
      });
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error creando feedback:', error);
      throw error;
    }
  }

  // Tipos de métrica
  async getTiposMetrica() {
    try {
      const response = await this.api.get('/tipos-metrica');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo tipos de métrica:', error);
      return [];
    }
  }

  async getTipoMetrica(id: string) {
    try {
      const response = await this.api.get(`/tipos-metrica/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo tipo de métrica ${id}:`, error);
      return null;
    }
  }

  // Métricas
  async getMetricas() {
    try {
      const response = await this.api.get('/metricas');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo métricas:', error);
      return [];
    }
  }

  async getMetrica(id: string) {
    try {
      const response = await this.api.get(`/metricas/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo métrica ${id}:`, error);
      return null;
    }
  }

  async getMetricasPorTipo(tipoId: string) {
    try {
      const response = await this.api.get(`/metricas/tipo/${tipoId}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo métricas del tipo ${tipoId}:`, error);
      return [];
    }
  }

  // Parámetros
  async getParametros() {
    try {
      const response = await this.api.get('/parametros');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo parámetros:', error);
      return [];
    }
  }

  async getParametro(id: string) {
    try {
      const response = await this.api.get(`/parametros/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo parámetro ${id}:`, error);
      return null;
    }
  }

  async getParametrosPorMetrica(metricaId: string) {
    try {
      const response = await this.api.get(`/parametros/metrica/${metricaId}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo parámetros de la métrica ${metricaId}:`, error);
      return [];
    }
  }
}