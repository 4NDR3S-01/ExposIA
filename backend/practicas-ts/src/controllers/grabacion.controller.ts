import { Controller, Post, Body, UseInterceptors, UploadedFile } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { GrabacionService } from '../services/grabacion.service';
import { CreateGrabacionDto } from '../models/grabacion.dto';
import { diskStorage } from 'multer';
import { extname } from 'path';

@Controller('grabacion')
export class GrabacionController {
  constructor(private readonly grabacionService: GrabacionService) {}

@Post('subir')
@UseInterceptors(FileInterceptor('archivo_audio', {
  storage: diskStorage({
    destination: './uploads/audio',
    filename: (req, file, cb) => {
      const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
      const ext = extname(file.originalname);
      cb(null, `${file.fieldname}-${uniqueSuffix}${ext}`);
    },
  }),
}))
async subirAudio(
  @UploadedFile() archivo_audio: Express.Multer.File,
  @Body() body: any // <- cambia esto
) {
  const { usuario_id, presentacion_id } = body;

  return this.grabacionService.crearGrabacion({
    usuario_id: parseInt(usuario_id),
    presentacion_id: parseInt(presentacion_id),
  }, archivo_audio.filename);
}

}   