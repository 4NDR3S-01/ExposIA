import { Module } from '@nestjs/common';
import { NavegacionSlidesController } from './navegacion-slides.controller';
import { NavegacionSlidesService } from './navegacion-slides.service';

@Module({
  controllers: [NavegacionSlidesController],
  providers: [NavegacionSlidesService]
})
export class NavegacionSlidesModule {}
