import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GrabacionesModule } from './grabaciones/grabaciones.module';
import { NavegacionSlidesModule } from './navegacion-slides/navegacion-slides.module';
import { CalificacionesModule } from './calificaciones/calificaciones.module';
import { HistorialPracticasModule } from './historial-practicas/historial-practicas.module';
import { TiemposSlideModule } from './tiempos-slide/tiempos-slide.module';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [GrabacionesModule, NavegacionSlidesModule, CalificacionesModule, HistorialPracticasModule, TiemposSlideModule, TypeOrmModule.forRoot({
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'postgres',
  password: 'postgres',
  database: 'exposia',
  autoLoadEntities: true,
  synchronize: true,
}),],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
