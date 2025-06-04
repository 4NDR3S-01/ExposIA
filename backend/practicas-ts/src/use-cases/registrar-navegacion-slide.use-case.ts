import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { NavegacionSlide } from '../models/navegacion_slide.entity';
import { CreateNavegacionSlideDto } from '../models/navegacion_slide.dto';

@Injectable()
export class RegistrarNavegacionSlideUseCase {
  constructor(
    @InjectRepository(NavegacionSlide)
    private readonly repo: Repository<NavegacionSlide>
  ) {}

  async execute(dto: CreateNavegacionSlideDto) {
    const nueva = this.repo.create(dto);
    return this.repo.save(nueva);
  }
}