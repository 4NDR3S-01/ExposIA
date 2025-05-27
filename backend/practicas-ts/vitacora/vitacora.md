# Bitácora del Módulo "Prácticas" – Proyecto ExposIA

**Responsable:** Dwesk  
**Lenguaje y Framework:** TypeScript + NestJS  
**Objetivo del módulo:** Permitir al usuario practicar su exposición navegando entre slides y grabando su voz. El sistema registra la navegación, guarda el audio, divide el contenido en fragmentos, y permite dejar notas por slide. Todo esto se prepara para ser analizado por IA en otro módulo.

---

## Estructura de datos (entidades propias)

1. **grabacion**  
   Registra el audio y vínculo con el usuario/presentación.

2. **navegacion_slide**  
   Guarda los cambios de slide durante la práctica, con timestamp relativo a la grabación.

3. **fragmento_audio**  
   Se genera automáticamente según los tiempos entre cada navegación; sirve para análisis detallado por slide.

4. **historial_practica**  
   Guarda la duración, inicio, fin y si fue terminada.

5. **nota_slide**  
   Permite que el usuario escriba notas por slide durante su práctica.

---

## Lógica de fragmentación

- Al comenzar la grabación, se crea el primer `fragmento_audio`.
- Cada vez que el usuario cambia de slide, se cierra el fragmento actual y se abre uno nuevo.
- Al finalizar la práctica, se cierra el último fragmento con la duración total del audio.

---

## Estado actual (última actualización)

✅ Definición final de entidades  
✅ Relación entre navegación y fragmentos corregida  
⏳ Falta generar `.entity.ts` y DTOs por carpeta  
⏳ Conexión de servicios y controladores pendiente  
❗ Base de datos PostgreSQL común a todos los módulos (por definir esquema final)

---

## Estructura del modulo
src/
├── controllers/               # Controladores por entidad
├── database/                  # Configuración de TypeORM o conexión PostgreSQL
├── models/                    # Entidades y DTOs
│   ├── *.entity.ts
│   ├── *.dto.ts
├── routes/                    # (Pendiente o para modularización futura)
├── services/                  # Lógica de negocio por entidad
├── app.ts                     # Configuración central de la app
├── server.ts                  # Punto de arranque personalizado
├── main.ts                    # (Evaluando eliminar si server.ts lo reemplaza)