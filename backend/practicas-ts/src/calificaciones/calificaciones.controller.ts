import { Controller, Get, Post, Body } from '@nestjs/common';
import { CalificacionesService } from './calificaciones.service';
import { Calificacion } from './entities/calificacion.entity';

@Controller('calificaciones')
export class CalificacionesController {
  constructor(private readonly service: CalificacionesService) {}

  @Post()
  create(@Body() data: Partial<Calificacion>) {
    return this.service.create(data);
  }

  @Get()
  findAll() {
    return this.service.findAll();
  }
}