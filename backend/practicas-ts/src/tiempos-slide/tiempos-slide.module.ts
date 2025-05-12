import { Module } from '@nestjs/common';
import { TiemposSlideController } from './tiempos-slide.controller';
import { TiemposSlideService } from './tiempos-slide.service';

@Module({
  controllers: [TiemposSlideController],
  providers: [TiemposSlideService]
})
export class TiemposSlideModule {}
