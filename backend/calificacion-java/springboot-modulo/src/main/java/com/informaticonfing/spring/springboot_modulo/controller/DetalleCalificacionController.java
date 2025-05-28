package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.service.DetalleCalificacionService;

/**
 * Controlador REST para la gestión de detalles de calificación.
 * Permite consultar, crear, actualizar y eliminar los detalles asociados a cada calificación.
 */
@RestController
@RequestMapping("/api/detalles")
public class DetalleCalificacionController {
    private final DetalleCalificacionService service;

    /**
     * Constructor inyectando el servicio correspondiente.
     * @param service Servicio de DetalleCalificacion
     */
    public DetalleCalificacionController(DetalleCalificacionService service) {
        this.service = service;
    }

    /**
     * Obtiene la lista de todos los detalles de calificación registrados.
     * GET /api/detalles
     * @return lista de DetalleCalificacion
     */
    @GetMapping
    public List<DetalleCalificacion> all() {
        return service.findAll();
    }

    /**
     * Busca un detalle de calificación por su ID.
     * GET /api/detalles/{id}
     * @param id ID del detalle a buscar
     * @return DetalleCalificacion si existe o 404 si no se encuentra
     */
    @GetMapping("/{id}")
    public ResponseEntity<DetalleCalificacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo detalle de calificación.
     * POST /api/detalles
     * @param d DetalleCalificacion a crear (en el body)
     * @return DetalleCalificacion creado
     */
    @PostMapping
    public DetalleCalificacion create(@RequestBody DetalleCalificacion d) {
        return service.create(d);
    }

    /**
     * Actualiza un detalle de calificación existente.
     * PUT /api/detalles/{id}
     * @param id ID del detalle a actualizar
     * @param d Objeto DetalleCalificacion con los datos nuevos
     * @return DetalleCalificacion actualizado o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<DetalleCalificacion> update(@PathVariable Long id,
                                                     @RequestBody DetalleCalificacion d) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, d)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un detalle de calificación por ID.
     * DELETE /api/detalles/{id}
     * @param id ID del detalle a eliminar
     * @return 204 No Content si fue borrado
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
