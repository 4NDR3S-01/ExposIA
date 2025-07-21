import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Grabacion } from '../models/grabacion.entity';
import { CreateGrabacionDto } from '../models/grabacion.dto';
import axios from 'axios';

@Injectable()
export class CrearGrabacionUseCase {
  constructor(
    @InjectRepository(Grabacion)
    private readonly grabacionRepo: Repository<Grabacion>,
  ) {}

  async execute(dto: CreateGrabacionDto, nombreArchivo: string) {
    const nueva = this.grabacionRepo.create({
      ...dto,
      archivo_audio: `/uploads/audio/${nombreArchivo}`,
      nombreArchivo,
    });
    
    const grabacionGuardada = await this.grabacionRepo.save(nueva);
    
    // Enviar notificación al servicio WebSocket
    await this.enviarNotificacion('grabacion.creada', {
      id: grabacionGuardada.id,
      usuarioId: grabacionGuardada.usuario_id,
      presentacionId: grabacionGuardada.presentacion_id,
      nombreArchivo: grabacionGuardada.nombreArchivo,
    });
    
    return grabacionGuardada;
  }

  private async enviarNotificacion(evento: string, payload: any): Promise<void> {
    try {
      const wsUrl = process.env.WS_NOTIFICATION_URL || 'http://localhost:9000';
      const token = process.env.WS_NOTIFICATION_TOKEN || 'dev';

      await axios.post(`${wsUrl}/notify`, {
        event: evento,
        payload: {
          ...payload,
          timestamp: new Date().toISOString(),
          source: 'practicas-ts'
        }
      }, {
        params: { token },
        timeout: 5000
      });

      console.log(`📡 Notificación enviada: ${evento}`, payload);
    } catch (error) {
      console.error(`❌ Error enviando notificación ${evento}:`, error.message);
      // No lanzamos el error para que no afecte la operación principal
    }
  }
}
