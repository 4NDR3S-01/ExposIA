// src/use-cases/fragmentar-desde-navegacion.usecase.ts

import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { NavegacionSlide } from '../models/navegacion_slide.entity';
import { FragmentoAudio } from '../models/fragmento_audio.entity';
import { Grabacion } from '../models/grabacion.entity';
import { FragmentarAudioUseCase } from './fragmentar-audio.usecase';

@Injectable()
export class FragmentarDesdeNavegacionUseCase {
  constructor(
    @InjectRepository(NavegacionSlide)
    private readonly navegacionRepo: Repository<NavegacionSlide>,

    @InjectRepository(FragmentoAudio)
    private readonly fragmentoRepo: Repository<FragmentoAudio>,

    @InjectRepository(Grabacion)
    private readonly grabacionRepo: Repository<Grabacion>,

    private readonly fragmentarAudioUseCase: FragmentarAudioUseCase
  ) {}

  async ejecutar(grabacionId: number): Promise<FragmentoAudio[]> {
    const navegaciones = await this.navegacionRepo.find({
      where: { grabacion_id: grabacionId },
      order: { timestamp: 'ASC' },
    });

    console.log('🧠 Navegaciones:', navegaciones); 

    if (navegaciones.length < 2) {
      throw new Error('Se necesitan al menos dos eventos de navegación para fragmentar');
    }

    const fragmentosGenerados: FragmentoAudio[] = [];

    for (let i = 0; i < navegaciones.length - 1; i++) {
      const inicio = navegaciones[i];
      const fin = navegaciones[i + 1];

      const fragmento = this.fragmentoRepo.create({
        grabacion_id: grabacionId,
        slide_id: inicio.slide_id,
        inicio_segundo: Math.floor(inicio.timestamp / 1000),
        fin_segundo: Math.floor(fin.timestamp / 1000),
      });

      const guardado = await this.fragmentoRepo.save(fragmento);
      const procesado = await this.fragmentarAudioUseCase.ejecutar(guardado.id);
      fragmentosGenerados.push(procesado);
    }

    return fragmentosGenerados;
  }
}
