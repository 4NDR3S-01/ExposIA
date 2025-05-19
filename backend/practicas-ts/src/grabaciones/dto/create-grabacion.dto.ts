import { IsNotEmpty, IsNumber, IsString } from 'class-validator';

export class CreateGrabacionDto {
  @IsNumber()
  id_usuario: number;

  @IsNumber()
  id_presentacion: number;

  @IsString()
  @IsNotEmpty()
  archivo_audio: string;
}
