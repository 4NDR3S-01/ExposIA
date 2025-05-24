import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Calificacion } from './entities/calificacion.entity';
import { CalificacionesService } from './calificaciones.service';
import { CalificacionesController } from './calificaciones.controller';

@Module({
  imports: [TypeOrmModule.forFeature([Calificacion])],
  providers: [CalificacionesService],
  controllers: [CalificacionesController],
})
export class CalificacionesModule {}