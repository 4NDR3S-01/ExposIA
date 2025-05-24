import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Grabacion } from './entities/grabacion.entity';
import { CreateGrabacionDto } from './dto/create-grabacion.dto';
import { Usuario } from '../usuarios/entities/usuario.entity';
import { Presentacion } from '../presentaciones/entities/presentacion.entity';

@Injectable()
export class GrabacionesService {
  constructor(
    @InjectRepository(Grabacion)
    private grabacionRepo: Repository<Grabacion>,
    @InjectRepository(Usuario)
    private usuarioRepo: Repository<Usuario>,
    @InjectRepository(Presentacion)
    private presentacionRepo: Repository<Presentacion>,
  ) {}

  async create(dto: CreateGrabacionDto) {
    const usuario = await this.usuarioRepo.findOneBy({ id_usuario: dto.id_usuario });
    const presentacion = await this.presentacionRepo.findOneBy({ id_presentacion: dto.id_presentacion });

    if (!usuario || !presentacion) throw new Error('Usuario o Presentación no encontrados');

    const grabacion = this.grabacionRepo.create({
      usuario,
      presentacion,
      archivo_audio: dto.archivo_audio,
    });

    return this.grabacionRepo.save(grabacion);
  }

  async findAll() {
    return this.grabacionRepo.find();
  }

  async findOne(id: number) {
    return this.grabacionRepo.findOneBy({ id_grabacion: id });
  }

  async remove(id: number) {
    return this.grabacionRepo.delete(id);
  }
}
