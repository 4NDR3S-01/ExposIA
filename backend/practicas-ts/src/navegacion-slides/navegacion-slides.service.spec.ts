import { Test, TestingModule } from '@nestjs/testing';
import { NavegacionSlidesService } from './navegacion-slides.service';

describe('NavegacionSlidesService', () => {
  let service: NavegacionSlidesService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [NavegacionSlidesService],
    }).compile();

    service = module.get<NavegacionSlidesService>(NavegacionSlidesService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
