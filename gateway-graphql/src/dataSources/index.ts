import { PresentacionesAPI } from './PresentacionesAPI';
import { PracticasAPI } from './PracticasAPI';
import { FeedbackAPI } from './FeedbackAPI';
import { CalificacionAPI } from './CalificacionAPI';

export interface DataSources {
  presentacionesAPI: PresentacionesAPI;
  practicasAPI: PracticasAPI;
  feedbackAPI: FeedbackAPI;
  calificacionAPI: CalificacionAPI;
}

export function createDataSources(): DataSources {
  return {
    presentacionesAPI: new PresentacionesAPI(),
    practicasAPI: new PracticasAPI(),
    feedbackAPI: new FeedbackAPI(),
    calificacionAPI: new CalificacionAPI(),
  };
}

export * from './PresentacionesAPI';
export * from './PracticasAPI';
export * from './FeedbackAPI';
export * from './CalificacionAPI';