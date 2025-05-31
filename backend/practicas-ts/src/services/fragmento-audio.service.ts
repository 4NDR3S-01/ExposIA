import { Injectable } from '@nestjs/common';
import { CrearFragmentoAudioUseCase } from '../use-cases/crear-fragmento-audio.use-case';
import { CreateFragmentoAudioDto } from '../models/fragmento_audio.dto';

@Injectable()
export class FragmentoAudioService {
  constructor(
    private readonly crearUseCase: CrearFragmentoAudioUseCase
  ) {}

  crear(dto: CreateFragmentoAudioDto) {
    return this.crearUseCase.ejecutar(dto);
  }
}
