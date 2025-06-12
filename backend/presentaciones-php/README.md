# 🟣 API REST - Módulo Presentaciones PHP

## 📋 Información Básica
- **Framework**: Laravel 10
- **Base de Datos**: Postgresql
- **Puerto**: 8000
- **Autenticación**: JWT

---

## 🔐 Autenticación

**Headers requeridos en todas las rutas:**
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Test de conexión:**
```http
GET /api/test-auth
```

---

## 🎯 Endpoints Principales

### **1. Usuarios**

#### Listar usuarios
```http
GET /api/usuarios
```

#### Crear usuario
```http
POST /api/usuarios
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "password": "123456"
}
```

#### Ver usuario
```http
GET /api/usuarios/{id}
```

#### Actualizar usuario
```http
PUT /api/usuarios/{id}
{
  "nombre": "Juan Actualizado"
}
```

#### Eliminar usuario
```http
DELETE /api/usuarios/{id}
```

---

### **2. Temas**

#### Listar temas
```http
GET /api/temas
```

#### Crear tema
```http
POST /api/temas
{
  "nombre": "Marketing Digital",
  "descripcion": "Estrategias de marketing online"
}
```

#### Ver tema con presentaciones
```http
GET /api/temas/{id}
```

---

### **3. Presentaciones**

#### Listar presentaciones
```http
GET /api/presentaciones
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "titulo": "Estrategia Q1 2024",
    "archivo_pdf": "uploads/pdfs/estrategia.pdf",
    "usuario": {
      "id": 1,
      "nombre": "Juan Pérez"
    },
    "tema": {
      "id": 2,
      "nombre": "Estrategia"
    },
    "slides": [...]
  }
]
```

#### Crear presentación
```http
POST /api/presentaciones
Content-Type: multipart/form-data

{
  "titulo": "Mi Presentación",
  "id_usuario": 1,
  "id_tema": 2,
  "archivo_pdf": [archivo.pdf]
}
```

#### Ver presentación
```http
GET /api/presentaciones/{id}
```

#### Actualizar presentación
```http
PUT /api/presentaciones/{id}
{
  "titulo": "Título actualizado"
}
```

#### Eliminar presentación
```http
DELETE /api/presentaciones/{id}
```

---

### **4. Slides**

#### Listar slides
```http
GET /api/slides
```

#### Crear slide
```http
POST /api/slides
{
  "numero_slide": 1,
  "texto_slide": "Contenido del slide",
  "imagen_slide": "url_imagen.jpg",
  "id_presentacion": 1
}
```

#### Ver slide
```http
GET /api/slides/{id}
```

#### Actualizar slide
```http
PUT /api/slides/{id}
{
  "texto_slide": "Nuevo contenido"
}
```

---

### **5. Calificaciones**

#### Listar calificaciones
```http
GET /api/calificaciones
```

#### Crear calificación
```http
POST /api/calificaciones
{
  "puntaje": 8,
  "comentario": "Excelente presentación",
  "id_usuario": 1,
  "id_presentacion": 1
}
```

---

## 📊 Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| `200` | ✅ Éxito |
| `201` | ✅ Creado |
| `400` | ❌ Error en datos |
| `401` | ❌ No autorizado |
| `404` | ❌ No encontrado |
| `500` | ❌ Error servidor |

---

## 🔧 Configuración

### Iniciar servidor
```bash
# Instalar dependencias
composer install

# Configurar BD
php artisan migrate

# Ejecutar
php artisan serve --port=8000
```

### Variables de entorno
```env
DB_CONNECTION=pgsql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=exposia_db
JWT_SECRET=tu_secreto_jwt
```

---

## 🧪 Pruebas con cURL

### Crear presentación
```bash
curl -X POST http://localhost:8000/api/presentaciones \
  -H "Authorization: Bearer tu_token" \
  -F "titulo=Test Presentación" \
  -F "id_usuario=1" \
  -F "id_tema=1" \
  -F "archivo_pdf=@archivo.pdf"
```

### Obtener presentaciones
```bash
curl -X GET http://localhost:8000/api/presentaciones \
  -H "Authorization: Bearer tu_token"
```

---

## 📁 Estructura de Archivos

```
presentaciones-php/
├── app/
│   ├── Http/Controllers/
│   │   ├── PresentacionController.php
│   │   ├── TemaController.php
│   │   ├── SlideController.php
│   │   └── CalificacionController.php
│   └── Models/
│       ├── Presentacion.php
│       ├── Tema.php
│       └── Slide.php
├── routes/
│   └── api.php
└── public/uploads/pdfs/

