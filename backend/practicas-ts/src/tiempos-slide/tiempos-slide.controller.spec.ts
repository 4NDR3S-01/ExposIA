import { Test, TestingModule } from '@nestjs/testing';
import { TiemposSlideController } from './tiempos-slide.controller';

describe('TiemposSlideController', () => {
  let controller: TiemposSlideController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [TiemposSlideController],
    }).compile();

    controller = module.get<TiemposSlideController>(TiemposSlideController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
