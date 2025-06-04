import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MulterModule } from '@nestjs/platform-express';

import { Grabacion } from './models/grabacion.entity';
import { NavegacionSlide } from './models/navegacion_slide.entity';
import { FragmentoAudio } from './models/fragmento_audio.entity';

import { GrabacionModule } from './grabacion.module';
import { NavegacionSlideModule } from './navegacion-slide.module';
import { FragmentoAudioModule } from './fragmento-audio.module';
import { DebugModule } from './debug.module';
import { NotaSlideModule } from './nota-slide.module';
import { HistorialPracticaModule } from './historial-practica.module';

import { CrearGrabacionUseCase } from './use-cases/crear-grabacion.use-case';
import { AuthMiddleware } from './common/middleware/api-key.middleware';
import * as dotenv from 'dotenv';
dotenv.config();

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'exposia',
      password: 'exposia123',
      database: 'exposia_db',
      entities: [Grabacion, NavegacionSlide, FragmentoAudio],
      autoLoadEntities: true,
      synchronize: true,
    }),
    GrabacionModule,
    NavegacionSlideModule,
    FragmentoAudioModule,
    DebugModule,
    NotaSlideModule,
    HistorialPracticaModule,
    TypeOrmModule.forFeature([Grabacion]),
    MulterModule.register({
      dest: './uploads/audio',
    }),
  ],
  controllers: [],
  providers: [CrearGrabacionUseCase],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(AuthMiddleware)
      .forRoutes('*'); // o una ruta específica como '/api/*'
  }
}
