package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.FeedbackCalificacion;
import com.informaticonfing.spring.springboot_modulo.service.FeedbackCalificacionService;

/**
 * Controlador REST para la gestión de feedback sobre calificaciones.
 * Permite consultar, crear, actualizar y eliminar comentarios de retroalimentación asociados a calificaciones.
 */
@RestController
@RequestMapping("/api/feedback")
public class FeedbackCalificacionController {
    private final FeedbackCalificacionService service;

    /**
     * Constructor inyectando el servicio correspondiente.
     * @param service Servicio de FeedbackCalificacion
     */
    public FeedbackCalificacionController(FeedbackCalificacionService service) {
        this.service = service;
    }

    /**
     * Obtiene la lista de todos los feedbacks registrados.
     * GET /api/feedback
     * @return lista de FeedbackCalificacion
     */
    @GetMapping
    public List<FeedbackCalificacion> all() {
        return service.findAll();
    }

    /**
     * Busca un feedback por su ID.
     * GET /api/feedback/{id}
     * @param id ID del feedback a buscar
     * @return FeedbackCalificacion si existe o 404 si no se encuentra
     */
    @GetMapping("/{id}")
    public ResponseEntity<FeedbackCalificacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo feedback.
     * POST /api/feedback
     * @param f FeedbackCalificacion a crear (en el body)
     * @return FeedbackCalificacion creado
     */
    @PostMapping
    public FeedbackCalificacion create(@RequestBody FeedbackCalificacion f) {
        return service.create(f);
    }

    /**
     * Actualiza un feedback existente.
     * PUT /api/feedback/{id}
     * @param id ID del feedback a actualizar
     * @param f Objeto FeedbackCalificacion con los datos nuevos
     * @return FeedbackCalificacion actualizado o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<FeedbackCalificacion> update(@PathVariable Long id,
                                                       @RequestBody FeedbackCalificacion f) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, f)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un feedback por ID.
     * DELETE /api/feedback/{id}
     * @param id ID del feedback a eliminar
     * @return 204 No Content si fue borrado
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
