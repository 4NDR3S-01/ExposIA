# Ejemplos de Consultas GraphQL para ExposIA Gateway

## 1. QUERIES BÁSICAS

### Obtener todos los usuarios
```graphql
query ObtenerUsuarios {
  usuarios {
    id
    nombre
    email
    created_at
  }
}
```

### Obtener usuario específico con sus presentaciones
```graphql
query UsuarioConPresentaciones {
  usuario(id: "1") {
    id
    nombre
    email
    presentaciones {
      id
      titulo
      archivo_pdf
      created_at
    }
  }
}
```

### Obtener presentaciones con datos completos
```graphql
query PresentacionesCompletas {
  presentaciones {
    id
    titulo
    archivo_pdf
    practicas {
      id
      grabacion {
        archivo_audio
        duracion
      }
    }
    feedback {
      id
      puntuacion_general
      feedback_texto
    }
    calificacionFinal {
      id
      puntaje_total
      comentario_general
    }
  }
}
```

## 2. CONSULTAS POR MÓDULO

### Módulo TypeScript - Prácticas detalladas
```graphql
query PracticasDetalladas {
  practicas(id_usuario: "1") {
    id
    grabacion {
      id
      archivo_audio
      duracion
      created_at
    }
    navegaciones {
      numero_slide
      tiempo_inicio
      tiempo_fin
    }
    fragmentos {
      numero_slide
      archivo_fragmento
      tiempo_inicio
      tiempo_fin
    }
    notas {
      numero_slide
      nota
    }
    historial {
      total_slides
      tiempo_total
      promedio_por_slide
    }
  }
}
```

### Módulo Python - Feedback con métricas
```graphql
query FeedbackConMetricas {
  feedbacks(id_usuario: "1") {
    id
    feedback_texto
    puntuacion_general
    metricas {
      id
      valor
      descripcion
      tipo {
        nombre
        descripcion
        peso
      }
      parametros {
        nombre
        valor
      }
    }
    created_at
  }
}
```

### Módulo Java - Calificaciones completas
```graphql
query CalificacionesCompletas {
  calificaciones(id_usuario: "1") {
    id
    puntaje_total
    comentario_general
    detalles {
      criterio
      puntaje
      peso
      comentario
    }
    feedback_calificacion {
      aspecto
      comentario
      sugerencia
    }
    created_at
  }
}
```

## 3. CONSULTA COMPLETA DEL FLUJO

### Flujo completo de una presentación
```graphql
query FlujoCompletoDetallado {
  flujoCompleto(id_presentacion: "1", id_usuario: "1") {
    usuario {
      id
      nombre
      email
    }
    presentacion {
      id
      titulo
      archivo_pdf
      created_at
    }
    practica {
      id
      grabacion {
        id
        archivo_audio
        duracion
      }
      navegaciones {
        numero_slide
        tiempo_inicio
        tiempo_fin
      }
      fragmentos {
        numero_slide
        archivo_fragmento
      }
      notas {
        numero_slide
        nota
      }
      historial {
        total_slides
        tiempo_total
        promedio_por_slide
      }
    }
    feedback {
      id
      feedback_texto
      puntuacion_general
      metricas {
        valor
        descripcion
        tipo {
          nombre
          peso
        }
      }
    }
    calificacion {
      id
      puntaje_total
      comentario_general
      detalles {
        criterio
        puntaje
        comentario
      }
    }
    estado
    timestamp
  }
}
```

## 4. MUTATIONS

### Ejecutar flujo completo del sistema
```graphql
mutation EjecutarFlujoCompleto {
  ejecutarFlujoCompleto(
    id_usuario: "1"
    id_presentacion: "1"
    archivo_audio: "presentacion_usuario1_20250124.mp3"
    navegaciones: [
      {
        numero_slide: 1
        tiempo_inicio: 0.0
        tiempo_fin: 45.5
      }
      {
        numero_slide: 2
        tiempo_inicio: 45.5
        tiempo_fin: 92.3
      }
      {
        numero_slide: 3
        tiempo_inicio: 92.3
        tiempo_fin: 150.0
      }
    ]
    notas: [
      {
        numero_slide: 1
        nota: "Buena introducción, pero muy rápida"
      }
      {
        numero_slide: 2
        nota: "Contenido técnico bien explicado"
      }
      {
        numero_slide: 3
        nota: "Conclusión clara y convincente"
      }
    ]
    usar_ia_calificacion: true
  ) {
    usuario {
      nombre
      email
    }
    presentacion {
      titulo
    }
    practica {
      grabacion {
        duracion
        archivo_audio
      }
      historial {
        total_slides
        tiempo_total
        promedio_por_slide
      }
    }
    feedback {
      puntuacion_general
      feedback_texto
      metricas {
        valor
        descripcion
      }
    }
    calificacion {
      puntaje_total
      comentario_general
      detalles {
        criterio
        puntaje
      }
    }
    estado
    timestamp
  }
}
```

### Mutations individuales

#### Iniciar una práctica
```graphql
mutation IniciarPractica {
  iniciarPractica(input: {
    id_usuario: "1"
    id_presentacion: "1"
    archivo_audio: "audio_practica.mp3"
  }) {
    id
    archivo_audio
    duracion
    created_at
  }
}
```

#### Guardar navegación
```graphql
mutation GuardarNavegacion {
  guardarNavegacion(input: {
    grabacion_id: "1"
    numero_slide: 1
    tiempo_inicio: 0.0
    tiempo_fin: 30.5
  }) {
    id
    numero_slide
    tiempo_inicio
    tiempo_fin
  }
}
```

#### Generar feedback con IA
```graphql
mutation GenerarFeedback {
  generarFeedback(input: {
    id_usuario: "1"
    id_presentacion: "1"
    grabacion_id: "1"
  }) {
    id
    feedback_texto
    puntuacion_general
    metricas {
      valor
      descripcion
    }
  }
}
```

#### Calificar presentación
```graphql
mutation CalificarPresentacion {
  calificarPresentacion(input: {
    id_usuario: "1"
    id_presentacion: "1"
    usar_ia: true
    comentario_adicional: "Presentación muy bien estructurada"
  }) {
    id
    puntaje_total
    comentario_general
    detalles {
      criterio
      puntaje
      comentario
    }
  }
}
```

## 5. CONSULTAS ÚTILES PARA DESARROLLO

### Verificar estado de servicios
```graphql
query VerificarServicios {
  usuarios {
    id
  }
  presentaciones {
    id
  }
  tiposMetrica {
    id
  }
  criteriosEvaluacion {
    id
  }
}
```

### Obtener datos para dashboard
```graphql
query Dashboard {
  usuarios {
    id
    nombre
    presentaciones {
      id
      titulo
      calificacionFinal {
        puntaje_total
      }
    }
  }
}
```

### Consulta de rendimiento de usuario
```graphql
query RendimientoUsuario($userId: ID!) {
  usuario(id: $userId) {
    nombre
    presentaciones {
      titulo
      practicas {
        historial {
          tiempo_total
          promedio_por_slide
        }
      }
      feedback {
        puntuacion_general
      }
      calificacionFinal {
        puntaje_total
      }
    }
  }
}
```

## 6. VARIABLES DE CONSULTA

### Usando variables para consultas dinámicas
```graphql
# Query
query ObtenerDatosUsuario($userId: ID!, $presentacionId: ID!) {
  usuario(id: $userId) {
    nombre
    email
  }
  presentacion(id: $presentacionId) {
    titulo
    practicas {
      grabacion {
        duracion
      }
    }
  }
}

# Variables
{
  "userId": "1",
  "presentacionId": "1"
}
```

## 7. CONSULTAS DE PRUEBA

### Test simple de conectividad
```graphql
query TestConectividad {
  usuarios {
    id
  }
}
```

### Test completo de servicios
```graphql
query TestCompleto {
  usuarios {
    id
    nombre
  }
  presentaciones {
    id
    titulo
  }
  tiposMetrica {
    id
    nombre
  }
  criteriosEvaluacion {
    id
    nombre
  }
}
```

---

**Nota:** Asegúrate de que todos los microservicios estén ejecutándose antes de realizar estas consultas. El gateway intentará conectarse a:
- PHP: http://localhost:8001
- TypeScript: http://localhost:3000  
- Python: http://localhost:8000
- Java: http://localhost:8080
