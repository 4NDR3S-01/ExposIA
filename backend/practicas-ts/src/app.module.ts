import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config'; // <-- importante
import { TypeOrmModule } from '@nestjs/typeorm';

import { AppController } from './app.controller';
import { AppService } from './app.service';

import { GrabacionesModule } from './grabaciones/grabaciones.module';
import { NavegacionSlidesModule } from './navegacion-slides/navegacion-slides.module';
import { CalificacionesModule } from './calificaciones/calificaciones.module';
import { HistorialPracticasModule } from './historial-practicas/historial-practicas.module';
import { TiemposSlideModule } from './tiempos-slide/tiempos-slide.module';

@Module({
  imports: [
    // 🟢 Cargar variables de entorno
    ConfigModule.forRoot({
      isGlobal: true,
    }),

    // 🟢 Conexión a PostgreSQL usando TypeORM
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      username: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres',
      database: process.env.DB_NAME || 'exposia',
      autoLoadEntities: true,
      synchronize: true, // Solo para desarrollo, no usar en producción
    }),

    // Módulos del sistema
    GrabacionesModule,
    NavegacionSlidesModule,
    CalificacionesModule,
    HistorialPracticasModule,
    TiemposSlideModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
