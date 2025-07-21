import { gql } from 'apollo-server-express';

export const typeDefs = gql`
  scalar DateTime

  """
  Usuario del sistema ExposIA
  """
  type Usuario {
    id: ID!
    nombre: String!
    email: String!
    presentaciones: [Presentacion!]!
    calificaciones: [Calificacion!]!
    grabaciones: [Grabacion!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Tema de presentación
  """
  type Tema {
    id: ID!
    nombre: String!
    descripcion: String
    presentaciones: [Presentacion!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Presentación con slides y archivos PDF
  """
  type Presentacion {
    id: ID!
    titulo: String!
    archivoPdf: String
    usuario: Usuario!
    tema: Tema!
    slides: [Slide!]!
    calificaciones: [Calificacion!]!
    grabaciones: [Grabacion!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Slide individual de una presentación
  """
  type Slide {
    id: ID!
    numeroSlide: Int!
    imagenSlide: String
    textoSlide: String
    presentacion: Presentacion!
    navegaciones: [NavegacionSlide!]!
    notas: [NotaSlide!]!
    fragmentosAudio: [FragmentoAudio!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Grabación de audio de una práctica
  """
  type Grabacion {
    id: ID!
    usuarioId: ID!
    presentacionId: ID!
    archivoAudio: String!
    nombreArchivo: String!
    fechaGrabacion: DateTime!
    usuario: Usuario!
    presentacion: Presentacion!
    navegaciones: [NavegacionSlide!]!
    fragmentos: [FragmentoAudio!]!
    notas: [NotaSlide!]!
    historial: HistorialPractica
    feedbacks: [Feedback!]!
    calificaciones: [Calificacion!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Navegación entre slides durante la práctica
  """
  type NavegacionSlide {
    id: ID!
    grabacionId: ID!
    slideId: ID!
    timestamp: Int!
    tipoNavegacion: String
    grabacion: Grabacion!
    slide: Slide!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Fragmento de audio correspondiente a un slide específico
  """
  type FragmentoAudio {
    id: ID!
    grabacionId: ID!
    slideId: ID!
    inicioSegundo: Int!
    finSegundo: Int!
    archivoFragmento: String
    grabacion: Grabacion!
    slide: Slide!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Nota del usuario en un slide específico
  """
  type NotaSlide {
    id: ID!
    grabacionId: ID!
    slideId: ID!
    contenido: String!
    timestamp: Int
    grabacion: Grabacion!
    slide: Slide!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Historial de práctica completa
  """
  type HistorialPractica {
    id: ID!
    grabacionId: ID!
    duracionTotal: Int!
    fechaInicio: DateTime!
    fechaFin: DateTime!
    finalizado: Boolean!
    grabacion: Grabacion!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Feedback de IA sobre parámetros específicos
  """
  type Feedback {
    id: ID!
    grabacionId: ID!
    parametroId: ID!
    valor: Float!
    comentario: String
    esManual: Boolean!
    grabacion: Grabacion!
    parametro: Parametro!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Parámetro de evaluación
  """
  type Parametro {
    id: ID!
    metricaId: ID!
    nombre: String!
    valor: Float!
    unidad: String
    metrica: Metrica!
    feedbacks: [Feedback!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Métrica de evaluación
  """
  type Metrica {
    id: ID!
    nombre: String!
    descripcion: String
    tipoMetricaId: ID!
    tipoMetrica: TipoMetrica!
    parametros: [Parametro!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Tipo de métrica para categorización
  """
  type TipoMetrica {
    id: ID!
    nombre: String!
    descripcion: String
    metricas: [Metrica!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Calificación final de una presentación
  """
  type Calificacion {
    id: ID!
    grabacionId: ID!
    usuarioId: ID!
    puntajeGlobal: Float!
    observacionGlobal: String
    tipoCalificacion: String!
    parametrosIdealesId: ID
    fecha: DateTime
    usuario: Usuario!
    grabacion: Grabacion!
    detalles: [DetalleCalificacion!]!
    feedbacks: [FeedbackCalificacion!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Detalle de calificación por criterio
  """
  type DetalleCalificacion {
    id: ID!
    calificacionId: ID!
    criterioId: ID!
    slideId: ID
    puntaje: Int!
    comentario: String
    fragmentoAudioId: ID
    calificacion: Calificacion!
    criterio: CriterioEvaluacion!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Criterio de evaluación
  """
  type CriterioEvaluacion {
    id: ID!
    nombre: String!
    descripcion: String!
    peso: Float!
    detalles: [DetalleCalificacion!]!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Feedback de calificación
  """
  type FeedbackCalificacion {
    id: ID!
    calificacionId: ID!
    observacion: String!
    fecha: DateTime!
    autor: String!
    calificacion: Calificacion!
    createdAt: DateTime
    updatedAt: DateTime
  }

  """
  Estadísticas generales del sistema
  """
  type EstadisticasGenerales {
    totalUsuarios: Int!
    totalPresentaciones: Int!
    totalGrabaciones: Int!
    totalCalificaciones: Int!
    promedioCalificaciones: Float
    presentacionesPorTema: [EstadisticaTema!]!
    actividadReciente: [ActividadReciente!]!
  }

  """
  Estadística por tema
  """
  type EstadisticaTema {
    tema: Tema!
    cantidad: Int!
    promedioCalificacion: Float
  }

  """
  Actividad reciente del sistema
  """
  type ActividadReciente {
    tipo: String!
    descripcion: String!
    fecha: DateTime!
    usuarioId: ID
    entidadId: ID
  }

  """
  Inputs para mutaciones
  """
  input CrearUsuarioInput {
    nombre: String!
    email: String!
    password: String!
  }

  input CrearTemaInput {
    nombre: String!
    descripcion: String
  }

  input CrearPresentacionInput {
    titulo: String!
    usuarioId: ID!
    temaId: ID!
  }

  input CrearGrabacionInput {
    usuarioId: ID!
    presentacionId: ID!
    nombreArchivo: String!
  }

  input CrearFeedbackInput {
    grabacionId: ID!
    parametroId: ID!
    valor: Float!
    comentario: String
    esManual: Boolean = false
  }

  """
  Consultas principales del sistema
  """
  type Query {
    # Usuarios
    usuarios: [Usuario!]!
    usuario(id: ID!): Usuario
    
    # Temas
    temas: [Tema!]!
    tema(id: ID!): Tema
    
    # Presentaciones
    presentaciones: [Presentacion!]!
    presentacion(id: ID!): Presentacion
    presentacionesPorUsuario(usuarioId: ID!): [Presentacion!]!
    presentacionesPorTema(temaId: ID!): [Presentacion!]!
    
    # Grabaciones y Prácticas
    grabaciones: [Grabacion!]!
    grabacion(id: ID!): Grabacion
    grabacionesPorUsuario(usuarioId: ID!): [Grabacion!]!
    grabacionesPorPresentacion(presentacionId: ID!): [Grabacion!]!
    
    # Slides
    slides: [Slide!]!
    slide(id: ID!): Slide
    slidesPorPresentacion(presentacionId: ID!): [Slide!]!
    
    # Feedback y Métricas
    feedbacks: [Feedback!]!
    feedbacksPorGrabacion(grabacionId: ID!): [Feedback!]!
    tiposMetrica: [TipoMetrica!]!
    metricas: [Metrica!]!
    parametros: [Parametro!]!
    
    # Calificaciones
    calificaciones: [Calificacion!]!
    calificacion(id: ID!): Calificacion
    calificacionesPorUsuario(usuarioId: ID!): [Calificacion!]!
    calificacionesPorGrabacion(grabacionId: ID!): [Calificacion!]!
    
    # Estadísticas
    estadisticasGenerales: EstadisticasGenerales!
    
    # Health check
    ping: String!
  }

  """
  Mutaciones del sistema
  """
  type Mutation {
    # Usuarios
    crearUsuario(input: CrearUsuarioInput!): Usuario!
    
    # Temas
    crearTema(input: CrearTemaInput!): Tema!
    
    # Presentaciones
    crearPresentacion(input: CrearPresentacionInput!): Presentacion!
    
    # Grabaciones
    crearGrabacion(input: CrearGrabacionInput!): Grabacion!
    
    # Feedback
    crearFeedback(input: CrearFeedbackInput!): Feedback!
    
    # Notificaciones de prueba
    enviarNotificacionPrueba(mensaje: String!): Boolean!
  }

  """
  Suscripciones en tiempo real
  """
  type Subscription {
    # Notificaciones generales
    notificacionesGenerales: String!
    
    # Eventos específicos
    presentacionCreada: Presentacion!
    grabacionCreada: Grabacion!
    calificacionCreada: Calificacion!
    feedbackCreado: Feedback!
  }
`;