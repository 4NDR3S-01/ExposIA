import { Test, TestingModule } from '@nestjs/testing';
import { NavegacionSlidesController } from './navegacion-slides.controller';

describe('NavegacionSlidesController', () => {
  let controller: NavegacionSlidesController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [NavegacionSlidesController],
    }).compile();

    controller = module.get<NavegacionSlidesController>(NavegacionSlidesController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
