import { Module } from '@nestjs/common';
import { HistorialPracticasController } from './historial-practicas.controller';
import { HistorialPracticasService } from './historial-practicas.service';

@Module({
  controllers: [HistorialPracticasController],
  providers: [HistorialPracticasService]
})
export class HistorialPracticasModule {}
