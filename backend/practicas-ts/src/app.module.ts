import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Grabacion } from './models/grabacion.entity';
import { GrabacionService } from './services/grabacion.service';
import { GrabacionController } from './controllers/grabacion.controller';
import { GrabacionModule } from './grabacion.module';
import { MulterModule } from '@nestjs/platform-express';
@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'exposia',
      password: 'exposia123',
      database: 'exposia_db',
      entities: [__dirname + '/models/*.entity.ts'],
      autoLoadEntities: true, 
      synchronize: true,
    }),
    GrabacionModule,
    TypeOrmModule.forFeature([Grabacion]),
    MulterModule.register({
      dest: './uploads/audio',
    }),
  ],
  controllers: [GrabacionController],
  providers: [GrabacionService],
})
export class AppModule {}