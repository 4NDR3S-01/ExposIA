// src/use-cases/fragmentos/fragmentar-audio.usecase.ts

import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { FragmentoAudio } from '../models/fragmento_audio.entity';
import { Grabacion } from '../models/grabacion.entity';
import * as ffmpeg from 'fluent-ffmpeg';
import * as ffmpegInstaller from '@ffmpeg-installer/ffmpeg';
import { join } from 'path';

ffmpeg.setFfmpegPath(ffmpegInstaller.path);

@Injectable()
export class FragmentarAudioUseCase {
  constructor(
    @InjectRepository(FragmentoAudio)
    private readonly fragmentoRepo: Repository<FragmentoAudio>,

    @InjectRepository(Grabacion)
    private readonly grabacionRepo: Repository<Grabacion>,
  ) {}

  async ejecutar(fragmentoId: number): Promise<FragmentoAudio> {
    const fragmento = await this.fragmentoRepo.findOne({ where: { id: fragmentoId } });
    if (!fragmento) throw new Error('Fragmento no encontrado');

    const grabacion = await this.grabacionRepo.findOne({ where: { id: fragmento.grabacion_id } });
    if (!grabacion) throw new Error('Grabación no encontrada');

    const duracion = fragmento.fin_segundo - fragmento.inicio_segundo;
    const nombreArchivo = `fragmento-${fragmento.id}-${Date.now()}.mp3`;
    const rutaSalida = join(__dirname, '..', '..', '..', 'uploads', 'fragmentos', nombreArchivo);
    const rutaEntrada = join(__dirname, '..', '..', '..', grabacion.archivo_audio);

    await new Promise<void>((resolve, reject) => {
      ffmpeg(rutaEntrada)
        .setStartTime(fragmento.inicio_segundo)
        .setDuration(duracion)
        .output(rutaSalida)
        .on('end', () => resolve())
        .on('error', err => reject(err))
        .run();
    });

    fragmento.archivo_fragmento = `/uploads/fragmentos/${nombreArchivo}`;
    return await this.fragmentoRepo.save(fragmento);
  }
}
