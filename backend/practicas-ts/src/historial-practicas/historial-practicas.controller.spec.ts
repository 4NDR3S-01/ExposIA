import { Test, TestingModule } from '@nestjs/testing';
import { HistorialPracticasController } from './historial-practicas.controller';

describe('HistorialPracticasController', () => {
  let controller: HistorialPracticasController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [HistorialPracticasController],
    }).compile();

    controller = module.get<HistorialPracticasController>(HistorialPracticasController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
