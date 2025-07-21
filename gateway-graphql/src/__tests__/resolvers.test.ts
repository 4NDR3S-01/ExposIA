import { resolvers } from '../resolvers';
import { createContext } from '../context';

// Mock de los data sources
const mockDataSources = {
  presentacionesAPI: {
    getUsuarios: jest.fn().mockResolvedValue([
      { id: 1, nombre: 'Test User', email: 'test@test.com' }
    ]),
    getPresentaciones: jest.fn().mockResolvedValue([
      { id: 1, titulo: 'Test Presentation', id_usuario: 1, id_tema: 1 }
    ]),
    getTemas: jest.fn().mockResolvedValue([
      { id: 1, nombre: 'Test Theme', descripcion: 'Test Description' }
    ]),
  },
  practicasAPI: {
    getGrabaciones: jest.fn().mockResolvedValue([
      { id: 1, usuario_id: 1, presentacion_id: 1, nombre_archivo: 'test.mp3' }
    ]),
  },
  feedbackAPI: {
    getFeedbacks: jest.fn().mockResolvedValue([
      { id: 1, grabacion_id: 1, parametro_id: 1, valor: 85.5 }
    ]),
  },
  calificacionAPI: {
    getCalificaciones: jest.fn().mockResolvedValue([
      { id: 1, grabacion_id: 1, usuario_id: 1, puntaje_global: 8.5 }
    ]),
  },
};

const mockNotificationService = {
  enviarNotificacion: jest.fn().mockResolvedValue(undefined),
};

const mockContext = {
  dataSources: mockDataSources,
  notificationService: mockNotificationService,
};

describe('GraphQL Resolvers', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Query resolvers', () => {
    test('ping should return pong message', async () => {
      const result = await resolvers.Query.ping();
      expect(result).toBe('pong - ExposIA Gateway funcionando!');
    });

    test('usuarios should return list of users', async () => {
      const result = await resolvers.Query.usuarios(null, {}, mockContext);
      expect(result).toHaveLength(1);
      expect(result[0]).toHaveProperty('nombre', 'Test User');
      expect(mockDataSources.presentacionesAPI.getUsuarios).toHaveBeenCalled();
    });

    test('presentaciones should return list of presentations', async () => {
      const result = await resolvers.Query.presentaciones(null, {}, mockContext);
      expect(result).toHaveLength(1);
      expect(result[0]).toHaveProperty('titulo', 'Test Presentation');
      expect(mockDataSources.presentacionesAPI.getPresentaciones).toHaveBeenCalled();
    });

    test('grabaciones should return list of recordings', async () => {
      const result = await resolvers.Query.grabaciones(null, {}, mockContext);
      expect(result).toHaveLength(1);
      expect(result[0]).toHaveProperty('nombre_archivo', 'test.mp3');
      expect(mockDataSources.practicasAPI.getGrabaciones).toHaveBeenCalled();
    });

    test('estadisticasGenerales should return system statistics', async () => {
      const result = await resolvers.Query.estadisticasGenerales(null, {}, mockContext);
      
      expect(result).toHaveProperty('totalUsuarios', 1);
      expect(result).toHaveProperty('totalPresentaciones', 1);
      expect(result).toHaveProperty('totalGrabaciones', 1);
      expect(result).toHaveProperty('totalCalificaciones', 1);
      expect(result).toHaveProperty('presentacionesPorTema');
      expect(result).toHaveProperty('actividadReciente');
    });
  });

  describe('Mutation resolvers', () => {
    test('crearUsuario should create user and send notification', async () => {
      const input = {
        nombre: 'New User',
        email: 'new@test.com',
        password: 'password123'
      };

      mockDataSources.presentacionesAPI.crearUsuario = jest.fn().mockResolvedValue({
        id: 2,
        ...input
      });

      const result = await resolvers.Mutation.crearUsuario(null, { input }, mockContext);
      
      expect(result).toHaveProperty('nombre', 'New User');
      expect(mockDataSources.presentacionesAPI.crearUsuario).toHaveBeenCalledWith(input);
      expect(mockNotificationService.enviarNotificacion).toHaveBeenCalledWith(
        'usuario.creado',
        expect.objectContaining({
          id: 2,
          nombre: 'New User',
          email: 'new@test.com'
        })
      );
    });

    test('enviarNotificacionPrueba should send test notification', async () => {
      const mensaje = 'Test notification message';
      
      const result = await resolvers.Mutation.enviarNotificacionPrueba(
        null, 
        { mensaje }, 
        mockContext
      );
      
      expect(result).toBe(true);
      expect(mockNotificationService.enviarNotificacion).toHaveBeenCalledWith(
        'test',
        { mensaje }
      );
    });
  });

  describe('Type resolvers', () => {
    test('Usuario.presentaciones should resolve user presentations', async () => {
      const parent = { id: 1 };
      mockDataSources.presentacionesAPI.getPresentacionesPorUsuario = jest.fn()
        .mockResolvedValue([{ id: 1, titulo: 'User Presentation' }]);

      const result = await resolvers.Usuario.presentaciones(parent, {}, mockContext);
      
      expect(result).toHaveLength(1);
      expect(mockDataSources.presentacionesAPI.getPresentacionesPorUsuario)
        .toHaveBeenCalledWith(1);
    });

    test('Presentacion.usuario should resolve presentation owner', async () => {
      const parent = { id: 1, id_usuario: 1 };
      mockDataSources.presentacionesAPI.getUsuario = jest.fn()
        .mockResolvedValue({ id: 1, nombre: 'Owner User' });

      const result = await resolvers.Presentacion.usuario(parent, {}, mockContext);
      
      expect(result).toHaveProperty('nombre', 'Owner User');
      expect(mockDataSources.presentacionesAPI.getUsuario).toHaveBeenCalledWith(1);
    });
  });
});