import axios from 'axios';

export class NotificationService {
  private wsUrl: string;
  private token: string;

  constructor() {
    this.wsUrl = process.env.WS_NOTIFICATION_URL || 'http://localhost:9000';
    this.token = process.env.WS_NOTIFICATION_TOKEN || 'dev';
  }

  async enviarNotificacion(evento: string, payload: any): Promise<void> {
    try {
      await axios.post(`${this.wsUrl}/notify`, {
        event: evento,
        payload: {
          ...payload,
          timestamp: new Date().toISOString(),
          source: 'gateway-graphql'
        }
      }, {
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        },
        timeout: 5000
      });

      console.log(`📡 Notificación enviada: ${evento}`, payload);
    } catch (error) {
      console.error(`❌ Error enviando notificación ${evento}:`, error.message);
      // No lanzamos el error para que no afecte la operación principal
    }
  }

  async enviarNotificacionUsuario(usuarioId: string, evento: string, payload: any): Promise<void> {
    await this.enviarNotificacion(`user.${usuarioId}.${evento}`, payload);
  }

  async enviarNotificacionGlobal(evento: string, payload: any): Promise<void> {
    await this.enviarNotificacion(`global.${evento}`, payload);
  }
}