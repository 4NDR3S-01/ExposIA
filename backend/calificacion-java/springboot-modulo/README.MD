
# 📚 Módulo de Calificaciones – Spring Boot

## Descripción General

Este módulo, desarrollado en **Java Spring Boot**, forma parte de un sistema backend modular para la gestión y evaluación de presentaciones orales. Permite crear, consultar, actualizar y eliminar calificaciones, criterios de evaluación, detalles de calificación, feedbacks y parámetros ideales. Es compatible con bases de datos PostgreSQL (usando Supabase).

---

## 🚀 ¿Cómo inicializar el proyecto?

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/tu-repo.git
cd springboot-modulo
````

### 2. Instalar dependencias

El proyecto utiliza **Maven** como gestor de dependencias. No necesitas instalar nada extra si usas el wrapper que ya viene en el proyecto.

```bash
./mvnw clean install
```

o si tienes Maven instalado globalmente:

```bash
mvn clean install
```

### 3. Configurar la base de datos

Edita el archivo `application.properties` con tus credenciales de base de datos PostgreSQL (ya viene listo para Supabase, pero revisa que el usuario, password y url sean correctos).

### 4. Levantar el proyecto

```bash
./mvnw spring-boot:run
```

o, si tienes Maven instalado globalmente:

```bash
mvn spring-boot:run
```

El backend estará disponible en [http://localhost:8080](http://localhost:8080).

---

## 📁 Estructura del Módulo

```
/springboot-modulo
│
├── src/
│   ├── controller/       # Controladores REST
│   ├── service/          # Lógica de negocio
│   ├── repository/       # Interfaces JPA para acceso a datos
│   ├── model/            # Entidades JPA
│   ├── dto/              # Objetos de transferencia de datos
│   ├── mapper/           # Conversores entidad-DTO
│   ├── config/           # Configuración (seguridad, etc.)
│
├── screenshots/          # Evidencias de pruebas (Postman)
│   ├── calificacion_delete.png
│   ├── calificacion_get_delete.png
│   ├── calificacion_getbyid.png
│   ├── calificacion_post.png
│   ├── calificacion_put.png
│   ├── calificaciones_get.png
│   ├── post_supabase.png
│   ├── revision_post.png
│
├── README.md
└── application.properties
```

---

## 🌍 Contexto Internacional

Este módulo fue desarrollado para un emprendimiento internacional que automatiza la gestión de calificaciones en presentaciones orales en instituciones educativas fuera de Ecuador. El enfoque es la adaptabilidad y escalabilidad para contextos internacionales.

---

## 🏗️ Entidades Principales

* **Calificacion:** Evaluación global de una grabación de presentación.
* **CriterioEvaluacion:** Criterios para evaluar presentaciones (claridad, estructura, etc.).
* **DetalleCalificacion:** Detalle individual de calificación por criterio.
* **FeedbackCalificacion:** Retroalimentación sobre la calificación.
* **ParametrosIdeales:** Parámetros de referencia para la evaluación (velocidad, pausas, claridad).

---

## 🔒 Seguridad

El módulo está protegido con **Spring Security**.

* Autenticación: Basic Auth
* Usuario para pruebas:

  * **Username:** `admin`
  * **Password:** `admin123`

---

## 🌐 Endpoints REST

| Entidad              | Método | Endpoint                   | Descripción                          |
| -------------------- | ------ | -------------------------- | ------------------------------------ |
| Calificacion         | GET    | `/api/calificaciones`      | Lista todas las calificaciones       |
|                      | GET    | `/api/calificaciones/{id}` | Consulta una calificación por ID     |
|                      | POST   | `/api/calificaciones`      | Crea una nueva calificación          |
|                      | PUT    | `/api/calificaciones/{id}` | Actualiza una calificación existente |
|                      | DELETE | `/api/calificaciones/{id}` | Elimina una calificación             |
| CriterioEvaluacion   | ...    | `/api/criterios`           | CRUD completo de criterios           |
| DetalleCalificacion  | ...    | `/api/detalles`            | CRUD completo de detalles            |
| FeedbackCalificacion | ...    | `/api/feedback`            | CRUD completo de feedbacks           |
| ParametrosIdeales    | ...    | `/api/parametros-ideales`  | CRUD de parámetros ideales           |

> **Nota:** Excepto `/api/parametros-ideales`, todos los endpoints requieren autenticación Basic Auth.


## 🧪 Evidencias de Pruebas (Postman)

A continuación, algunas capturas de las pruebas realizadas sobre los endpoints principales:

### Obtener todas las calificaciones (GET)

![GET Calificaciones](screenshots/calificaciones_get.png)


### Crear nueva calificación (POST)

![POST Calificación](screenshots/calificacion_post.png)

### Obtener calificación por ID (GET)

![GET Calificación por ID](screenshots/calificacion_getbyid.png)


### Editar calificación existente (PUT)

![PUT Calificación](screenshots/calificacion_put.png)

### Eliminar calificación (DELETE)

![DELETE Calificación](screenshots/calificacion_delete.png)

### Verificar calificación eliminada (GET tras DELETE)

![GET tras DELETE](screenshots/calificacion_get_delete.png)

### Otras pruebas de integración Supabase

![POST Supabase](screenshots/post_supabase.png)
![Revisión POST](screenshots/revision_post.png)

---

## ⚙️ Recomendaciones

* Asegúrate de que los registros relacionados existan en la base antes de hacer POST o PUT (usuarios, grabaciones, etc.).
* Las evidencias aquí mostradas son de rutas realmente probadas con Postman.
* Puedes ampliar este módulo agregando más lógica de negocio o integraciones según las necesidades del proyecto.

