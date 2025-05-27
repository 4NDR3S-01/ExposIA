import { IsInt, IsString } from 'class-validator';

export class CreateGrabacionDto {
  @IsInt()
  usuario_id: number;

  @IsInt()
  presentacion_id: number;

  @IsString()
  archivo_audio: string;
}
