import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Grabacion } from './entities/grabacion.entity';
import { Usuario } from '../usuarios/entities/usuario.entity';
import { Presentacion } from '../presentaciones/entities/presentacion.entity';
import { GrabacionesService } from './grabaciones.service';
import { GrabacionesController } from './grabaciones.controller';

@Module({
  imports: [TypeOrmModule.forFeature([Grabacion, Usuario, Presentacion])],
  controllers: [GrabacionesController],
  providers: [GrabacionesService],
})
export class GrabacionesModule {}
