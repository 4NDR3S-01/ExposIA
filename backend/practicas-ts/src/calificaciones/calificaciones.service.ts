import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Calificacion } from './entities/calificacion.entity';

@Injectable()
export class CalificacionesService {
  constructor(
    @InjectRepository(Calificacion)
    private calificacionRepo: Repository<Calificacion>,
  ) {}

  create(data: Partial<Calificacion>) {
    const calificacion = this.calificacionRepo.create(data);
    return this.calificacionRepo.save(calificacion);
  }

  findAll() {
    return this.calificacionRepo.find({ relations: ['feedback', 'usuario'] });
  }
}