import { Controller, Post, Body, UseInterceptors, UploadedFile } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { CreateGrabacionDto } from '../models/grabacion.dto';
import { diskStorage } from 'multer';
import { extname } from 'path';
import { CrearGrabacionUseCase } from '../use-cases/crear-grabacion.use-case';

@Controller('grabacion')
export class GrabacionController {
  constructor(private readonly crearGrabacionUC: CrearGrabacionUseCase) {}

  @Post('subir')
  @UseInterceptors(
    FileInterceptor('archivo_audio', {
      storage: diskStorage({
        destination: './uploads/audio',
        filename: (req, file, cb) => {
          const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
          const ext = extname(file.originalname);
          cb(null, `${file.fieldname}-${uniqueSuffix}${ext}`);
        },
      }),
    }),
  )
  async subirAudio(
    @UploadedFile() archivo_audio: Express.Multer.File,
    @Body() body: CreateGrabacionDto,
  ) {
    const dto = {
      ...body,
      nombreArchivo: archivo_audio.filename,
    };

    return this.crearGrabacionUC.execute(dto, archivo_audio.filename);
  }
}
