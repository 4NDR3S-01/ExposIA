package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.service.CriterioEvaluacionService;

/**
 * Controlador REST para la gestión de criterios de evaluación.
 * Permite realizar operaciones CRUD sobre los criterios utilizados para calificar grabaciones.
 */
@RestController
@RequestMapping("/api/criterios")
public class CriterioEvaluacionController {
    private final CriterioEvaluacionService service;

    /**
     * Constructor inyectando el servicio correspondiente.
     * @param service Servicio de CriterioEvaluacion
     */
    public CriterioEvaluacionController(CriterioEvaluacionService service) {
        this.service = service;
    }

    /**
     * Obtiene la lista de todos los criterios de evaluación existentes.
     * GET /api/criterios
     * @return lista de CriterioEvaluacion
     */
    @GetMapping
    public List<CriterioEvaluacion> all() {
        return service.findAll();
    }

    /**
     * Busca un criterio de evaluación por ID.
     * GET /api/criterios/{id}
     * @param id ID del criterio a buscar
     * @return CriterioEvaluacion si existe o 404 si no se encuentra
     */
    @GetMapping("/{id}")
    public ResponseEntity<CriterioEvaluacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo criterio de evaluación.
     * POST /api/criterios
     * @param c Objeto CriterioEvaluacion en el body
     * @return CriterioEvaluacion creado
     */
    @PostMapping
    public CriterioEvaluacion create(@RequestBody CriterioEvaluacion c) {
        return service.create(c);
    }

    /**
     * Actualiza un criterio de evaluación existente.
     * PUT /api/criterios/{id}
     * @param id ID del criterio a actualizar
     * @param c Objeto CriterioEvaluacion con los datos nuevos
     * @return CriterioEvaluacion actualizado o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<CriterioEvaluacion> update(@PathVariable Long id,
                                                     @RequestBody CriterioEvaluacion c) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, c)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un criterio de evaluación por ID.
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
