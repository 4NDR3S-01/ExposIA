import { Controller, Post, Body, Get, Param, Delete } from '@nestjs/common';
import { GrabacionesService } from './grabaciones.service';
import { CreateGrabacionDto } from './dto/create-grabacion.dto';

@Controller('grabaciones')
export class GrabacionesController {
  constructor(private readonly grabacionesService: GrabacionesService) {}

  @Post()
  create(@Body() dto: CreateGrabacionDto) {
    return this.grabacionesService.create(dto);
  }

  @Get()
  findAll() {
    return this.grabacionesService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.grabacionesService.findOne(+id);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.grabacionesService.remove(+id);
  }
}
