// controllers/debug.controller.ts
import { Controller, Get, Param } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { NavegacionSlide } from '../models/navegacion_slide.entity';

@Controller('debug')
export class DebugController {
  constructor(
    @InjectRepository(NavegacionSlide)
    private readonly repo: Repository<NavegacionSlide>,
  ) {}

  @Get('navegacion/:grabacionId')
  async ver(@Param('grabacionId') id: number) {
    return await this.repo.find({
      where: { grabacion_id: id },
      order: { timestamp: 'ASC' }
    });
  }
}
