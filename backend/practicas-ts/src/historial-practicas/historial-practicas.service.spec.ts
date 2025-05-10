import { Test, TestingModule } from '@nestjs/testing';
import { HistorialPracticasService } from './historial-practicas.service';

describe('HistorialPracticasService', () => {
  let service: HistorialPracticasService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [HistorialPracticasService],
    }).compile();

    service = module.get<HistorialPracticasService>(HistorialPracticasService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
