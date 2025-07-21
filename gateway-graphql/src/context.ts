import { DataSources, createDataSources } from './dataSources';
import { NotificationService } from './services/NotificationService';

export interface Context {
  dataSources: DataSources;
  notificationService: NotificationService;
}

export function createContext(): Context {
  return {
    dataSources: createDataSources(),
    notificationService: new NotificationService(),
  };
}