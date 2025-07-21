import axios, { AxiosInstance } from 'axios';

export class PresentacionesAPI {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.PRESENTACIONES_API_URL || 'http://localhost:8001/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    });

    // Interceptor para agregar token JWT si está disponible
    this.api.interceptors.request.use((config) => {
      const token = process.env.PRESENTACIONES_JWT_TOKEN;
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Interceptor para manejar errores
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Error en PresentacionesAPI:', error.response?.data || error.message);
        throw error;
      }
    );
  }

  // Usuarios
  async getUsuarios() {
    try {
      const response = await this.api.get('/usuarios');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo usuarios:', error);
      return [];
    }
  }

  async getUsuario(id: string) {
    try {
      const response = await this.api.get(`/usuarios/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo usuario ${id}:`, error);
      return null;
    }
  }

  async crearUsuario(input: any) {
    try {
      const response = await this.api.post('/usuarios', input);
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error creando usuario:', error);
      throw error;
    }
  }

  // Temas
  async getTemas() {
    try {
      const response = await this.api.get('/temas');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo temas:', error);
      return [];
    }
  }

  async getTema(id: string) {
    try {
      const response = await this.api.get(`/temas/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo tema ${id}:`, error);
      return null;
    }
  }

  async crearTema(input: any) {
    try {
      const response = await this.api.post('/temas', input);
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error creando tema:', error);
      throw error;
    }
  }

  // Presentaciones
  async getPresentaciones() {
    try {
      const response = await this.api.get('/presentaciones');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo presentaciones:', error);
      return [];
    }
  }

  async getPresentacion(id: string) {
    try {
      const response = await this.api.get(`/presentaciones/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo presentación ${id}:`, error);
      return null;
    }
  }

  async getPresentacionesPorUsuario(usuarioId: string) {
    try {
      const presentaciones = await this.getPresentaciones();
      return presentaciones.filter((p: any) => 
        (p.id_usuario || p.usuarioId) === parseInt(usuarioId)
      );
    } catch (error) {
      console.error(`Error obteniendo presentaciones del usuario ${usuarioId}:`, error);
      return [];
    }
  }

  async getPresentacionesPorTema(temaId: string) {
    try {
      const presentaciones = await this.getPresentaciones();
      return presentaciones.filter((p: any) => 
        (p.id_tema || p.temaId) === parseInt(temaId)
      );
    } catch (error) {
      console.error(`Error obteniendo presentaciones del tema ${temaId}:`, error);
      return [];
    }
  }

  async crearPresentacion(input: any) {
    try {
      const response = await this.api.post('/presentaciones', {
        titulo: input.titulo,
        id_usuario: input.usuarioId,
        id_tema: input.temaId,
      });
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error creando presentación:', error);
      throw error;
    }
  }

  // Slides
  async getSlides() {
    try {
      const response = await this.api.get('/slides');
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error obteniendo slides:', error);
      return [];
    }
  }

  async getSlide(id: string) {
    try {
      const response = await this.api.get(`/slides/${id}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error(`Error obteniendo slide ${id}:`, error);
      return null;
    }
  }

  async getSlidesPorPresentacion(presentacionId: string) {
    try {
      const slides = await this.getSlides();
      return slides.filter((s: any) => 
        (s.id_presentacion || s.presentacionId) === parseInt(presentacionId)
      );
    } catch (error) {
      console.error(`Error obteniendo slides de la presentación ${presentacionId}:`, error);
      return [];
    }
  }
}