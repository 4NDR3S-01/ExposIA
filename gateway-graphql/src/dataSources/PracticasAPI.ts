import axios, { AxiosInstance } from 'axios';

export class PracticasAPI {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.PRACTICAS_API_URL || 'http://localhost:3000',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.PRACTICAS_API_KEY || 'mi-token-seguro'}`
      }
    });

    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Error en PracticasAPI:', error.response?.data || error.message);
        throw error;
      }
    );
  }

  // Grabaciones
  async getGrabaciones() {
    try {
      const response = await this.api.get('/debug/resumen/all');
      return response.data.grabaciones || [];
    } catch (error) {
      console.error('Error obteniendo grabaciones:', error);
      return [];
    }
  }

  async getGrabacion(id: string) {
    try {
      const response = await this.api.get(`/debug/resumen/${id}`);
      return response.data.grabacion;
    } catch (error) {
      console.error(`Error obteniendo grabación ${id}:`, error);
      return null;
    }
  }

  async getGrabacionesPorUsuario(usuarioId: string) {
    try {
      const grabaciones = await this.getGrabaciones();
      return grabaciones.filter((g: any) => 
        (g.usuario_id || g.usuarioId) === parseInt(usuarioId)
      );
    } catch (error) {
      console.error(`Error obteniendo grabaciones del usuario ${usuarioId}:`, error);
      return [];
    }
  }

  async getGrabacionesPorPresentacion(presentacionId: string) {
    try {
      const grabaciones = await this.getGrabaciones();
      return grabaciones.filter((g: any) => 
        (g.presentacion_id || g.presentacionId) === parseInt(presentacionId)
      );
    } catch (error) {
      console.error(`Error obteniendo grabaciones de la presentación ${presentacionId}:`, error);
      return [];
    }
  }

  async crearGrabacion(input: any) {
    try {
      // Simular creación de grabación (en realidad se hace por upload)
      const formData = new FormData();
      formData.append('usuario_id', input.usuarioId);
      formData.append('presentacion_id', input.presentacionId);
      formData.append('nombreArchivo', input.nombreArchivo);
      
      // Nota: En un caso real, aquí se subiría el archivo de audio
      const response = await this.api.post('/grabacion/subir', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error creando grabación:', error);
      throw error;
    }
  }

  // Navegaciones
  async getNavegacionesPorGrabacion(grabacionId: string) {
    try {
      const response = await this.api.get(`/debug/resumen/${grabacionId}`);
      return response.data.navegaciones || [];
    } catch (error) {
      console.error(`Error obteniendo navegaciones de la grabación ${grabacionId}:`, error);
      return [];
    }
  }

  async getNavegacionesPorSlide(slideId: string) {
    try {
      const grabaciones = await this.getGrabaciones();
      const navegaciones = [];
      
      for (const grabacion of grabaciones) {
        const navGrabacion = await this.getNavegacionesPorGrabacion(grabacion.id);
        navegaciones.push(...navGrabacion.filter((nav: any) => 
          (nav.slide_id || nav.slideId) === parseInt(slideId)
        ));
      }
      
      return navegaciones;
    } catch (error) {
      console.error(`Error obteniendo navegaciones del slide ${slideId}:`, error);
      return [];
    }
  }

  // Fragmentos de audio
  async getFragmentosPorGrabacion(grabacionId: string) {
    try {
      const response = await this.api.get(`/debug/resumen/${grabacionId}`);
      return response.data.fragmentos || [];
    } catch (error) {
      console.error(`Error obteniendo fragmentos de la grabación ${grabacionId}:`, error);
      return [];
    }
  }

  async getFragmentosPorSlide(slideId: string) {
    try {
      const grabaciones = await this.getGrabaciones();
      const fragmentos = [];
      
      for (const grabacion of grabaciones) {
        const fragGrabacion = await this.getFragmentosPorGrabacion(grabacion.id);
        fragmentos.push(...fragGrabacion.filter((frag: any) => 
          (frag.slide_id || frag.slideId) === parseInt(slideId)
        ));
      }
      
      return fragmentos;
    } catch (error) {
      console.error(`Error obteniendo fragmentos del slide ${slideId}:`, error);
      return [];
    }
  }

  // Notas
  async getNotasPorGrabacion(grabacionId: string) {
    try {
      const response = await this.api.get(`/debug/resumen/${grabacionId}`);
      return response.data.notas || [];
    } catch (error) {
      console.error(`Error obteniendo notas de la grabación ${grabacionId}:`, error);
      return [];
    }
  }

  async getNotasPorSlide(slideId: string) {
    try {
      const grabaciones = await this.getGrabaciones();
      const notas = [];
      
      for (const grabacion of grabaciones) {
        const notasGrabacion = await this.getNotasPorGrabacion(grabacion.id);
        notas.push(...notasGrabacion.filter((nota: any) => 
          (nota.slide_id || nota.slideId) === parseInt(slideId)
        ));
      }
      
      return notas;
    } catch (error) {
      console.error(`Error obteniendo notas del slide ${slideId}:`, error);
      return [];
    }
  }

  // Historial
  async getHistorialPorGrabacion(grabacionId: string) {
    try {
      const response = await this.api.get(`/debug/resumen/${grabacionId}`);
      return response.data.historial;
    } catch (error) {
      console.error(`Error obteniendo historial de la grabación ${grabacionId}:`, error);
      return null;
    }
  }
}