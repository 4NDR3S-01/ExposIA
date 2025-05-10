import { Module } from '@nestjs/common';
import { GrabacionesController } from './grabaciones.controller';
import { GrabacionesService } from './grabaciones.service';

@Module({
  controllers: [GrabacionesController],
  providers: [GrabacionesService]
})
export class GrabacionesModule {}
