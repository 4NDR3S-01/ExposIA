import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Grabacion } from './models/grabacion.entity';
import { GrabacionService } from './services/grabacion.service';
import { GrabacionController } from './controllers/grabacion.controller';
import { GrabacionModule } from './grabacion.module';
import { MulterModule } from '@nestjs/platform-express';
import { CrearGrabacionUseCase } from './use-cases/crear-grabacion.use-case';
import { NavegacionSlide } from './models/navegacion_slide.entity';
import { NavegacionSlideController } from './controllers/navegacion-slide.controller';
import { NavegacionSlideModule } from './navegacion-slide.module';
import { FragmentoAudio } from './models/fragmento_audio.entity';
import { FragmentoAudioModule } from './fragmento-audio.module';
import { DebugModule } from './debug.module';
import { NotaSlideModule } from './nota-slide.module';
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
    TypeOrmModule.forFeature([Grabacion]),
    MulterModule.register({
      dest: './uploads/audio',
    }),
  ],
  controllers: [],
  providers: [CrearGrabacionUseCase],
})
export class AppModule {}