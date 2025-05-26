package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.service.DetalleCalificacionService;

/**
 * Controlador REST para los detalles de calificación.
 * Permite CRUD de puntajes individuales por criterio en cada grabación.
 */
@RestController
@RequestMapping("/api/detalles")
public class DetalleCalificacionController {
    private final DetalleCalificacionService service;

    /**
     * Constructor con inyección de servicio.
     * @param service Servicio de DetalleCalificacion
     */
    public DetalleCalificacionController(DetalleCalificacionService service) {
        this.service = service;
    }

    /**
     * Lista todos los detalles de calificación.
     * GET /api/detalles
     * @return lista de DetalleCalificacion
     */
    @GetMapping
    public List<DetalleCalificacion> all() {
        return service.findAll();
    }

    /**
     * Busca un detalle por ID.
     * GET /api/detalles/{id}
     * @param id ID del detalle
     * @return DetalleCalificacion o 404
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
     * @param d DetalleCalificacion a crear
     * @return Detalle creado
     */
    @PostMapping
    public DetalleCalificacion create(@RequestBody DetalleCalificacion d) {
        return service.create(d);
    }

    /**
     * Actualiza un detalle existente.
     * PUT /api/detalles/{id}
     * @param id ID del detalle
     * @param d Nuevos datos
     * @return Detalle actualizado o 404
     */
    @PutMapping("/{id}")
    public ResponseEntity<DetalleCalificacion> update(@PathVariable Long id,
                                                      @RequestBody DetalleCalificacion d) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, d)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un detalle por ID.
     * DELETE /api/detalles/{id}
     * @param id ID del detalle a eliminar
     * @return 204 si fue eliminado
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
