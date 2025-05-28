package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.service.CalificacionService;

/**
 * Controlador REST para la gestión de calificaciones.
 * Permite consultar, crear, actualizar y eliminar las evaluaciones de las grabaciones.
 */
@RestController
@RequestMapping("/api/calificaciones")
public class CalificacionController {

    private final CalificacionService service;

    /**
     * Constructor inyectando el servicio correspondiente.
     * @param service Servicio de Calificacion
     */
    public CalificacionController(CalificacionService service) {
        this.service = service;
    }

    /**
     * Obtiene la lista de todas las calificaciones registradas.
     * GET /api/calificaciones
     * @return lista de Calificacion
     */
    @GetMapping
    public List<Calificacion> all() {
        return service.findAll();
    }

    /**
     * Busca una calificación por su ID.
     * GET /api/calificaciones/{id}
     * @param id ID de la calificación a buscar
     * @return Calificacion si existe o 404 si no se encuentra
     */
    @GetMapping("/{id}")
    public ResponseEntity<Calificacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea una nueva calificación.
     * POST /api/calificaciones
     * @param c Calificacion a crear (en el body)
     * @return Calificacion creada
     */
    @PostMapping
    public Calificacion create(@RequestBody Calificacion c) {
        return service.create(c);
    }

    /**
     * Actualiza una calificación existente.
     * PUT /api/calificaciones/{id}
     * @param id ID de la calificación a actualizar
     * @param c Objeto Calificacion con los datos nuevos
     * @return Calificacion actualizada o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<Calificacion> update(@PathVariable Long id,
                                               @RequestBody Calificacion c) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, c)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina una calificación por ID.
     * DELETE /api/calificaciones/{id}
     * @param id ID de la calificación a eliminar
     * @return 204 No Content si fue borrada
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
