import { Test, TestingModule } from '@nestjs/testing';
import { TiemposSlideService } from './tiempos-slide.service';

describe('TiemposSlideService', () => {
  let service: TiemposSlideService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TiemposSlideService],
    }).compile();

    service = module.get<TiemposSlideService>(TiemposSlideService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
