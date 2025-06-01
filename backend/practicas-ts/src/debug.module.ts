import { Module } from '@nestjs/common';
import { DebugController } from './controllers/debug.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { NavegacionSlide } from './models/navegacion_slide.entity';

@Module({
  imports: [TypeOrmModule.forFeature([NavegacionSlide])],
  controllers: [DebugController],
})
export class DebugModule {}
