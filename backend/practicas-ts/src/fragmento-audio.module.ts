import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { FragmentoAudio } from './models/fragmento_audio.entity';
import { CrearFragmentoAudioUseCase } from './use-cases/crear-fragmento-audio.use-case';
import { FragmentoAudioService } from './services/fragmento-audio.service';
import { FragmentoAudioController } from './controllers/fragmento-audio.controller';

@Module({
  imports: [TypeOrmModule.forFeature([FragmentoAudio])],
  controllers: [FragmentoAudioController],
  providers: [
    CrearFragmentoAudioUseCase,
    FragmentoAudioService
  ],
})
export class FragmentoAudioModule {}
