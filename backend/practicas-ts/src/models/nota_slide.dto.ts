import { IsInt, IsString, IsOptional } from 'class-validator';

export class CreateNotaSlideDto {
    @IsInt()
    grabacion_id: number; // ID de la grabación asociada a la nota

    @IsInt()
    slide_id: number; // ID del slide al que pertenece la nota

    @IsString()
    contenido: string; // Contenido de la nota

    @IsOptional()
    @IsString()
    timestamp?: number; 
}
