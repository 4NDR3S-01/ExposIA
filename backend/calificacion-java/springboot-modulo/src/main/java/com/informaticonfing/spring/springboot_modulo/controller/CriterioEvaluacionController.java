package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.service.CriterioEvaluacionService;

/**
 * Controlador REST para la gestión de criterios de evaluación.
 * Cada criterio define un aspecto bajo el cual se evalúa una grabación.
 */
@RestController
@RequestMapping("/api/criterios")
public class CriterioEvaluacionController {
    private final CriterioEvaluacionService service;

    /**
     * Constructor con inyección del servicio.
     * @param service Servicio de CriterioEvaluacion
     */
    public CriterioEvaluacionController(CriterioEvaluacionService service) {
        this.service = service;
    }

    /**
     * Lista todos los criterios de evaluación.
     * GET /api/criterios
     * @return lista de CriterioEvaluacion
     */
    @GetMapping
    public List<CriterioEvaluacion> all() {
        return service.findAll();
    }

    /**
     * Devuelve un criterio por su ID.
     * GET /api/criterios/{id}
     * @param id ID del criterio
     * @return CriterioEvaluacion o 404 si no existe
     */
    @GetMapping("/{id}")
    public ResponseEntity<CriterioEvaluacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo criterio.
     * POST /api/criterios
     * @param c CriterioEvaluacion a crear
     * @return Criterio creado
     */
    @PostMapping
    public CriterioEvaluacion create(@RequestBody CriterioEvaluacion c) {
        return service.create(c);
    }

    /**
     * Actualiza un criterio existente.
     * PUT /api/criterios/{id}
     * @param id ID del criterio a actualizar
     * @param c Criterio con nuevos datos
     * @return Criterio actualizado o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<CriterioEvaluacion> update(@PathVariable Long id,
                                                     @RequestBody CriterioEvaluacion c) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, c)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un criterio por ID.
     * DELETE /api/criterios/{id}
     * @param id ID del criterio a eliminar
     * @return 204 si se borró correctamente
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
