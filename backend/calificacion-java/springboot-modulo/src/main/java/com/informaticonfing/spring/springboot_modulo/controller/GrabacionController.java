package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.Grabacion;
import com.informaticonfing.spring.springboot_modulo.service.GrabacionService;

/**
 * Controlador REST para la gestión de grabaciones.
 * Permite consultar, crear, actualizar y eliminar grabaciones de evidencia.
 */
@RestController
@RequestMapping("/api/grabaciones")
public class GrabacionController {
    private final GrabacionService service;

    /**
     * Constructor con inyección de dependencias.
     * @param service Servicio de Grabacion
     */
    public GrabacionController(GrabacionService service) {
        this.service = service;
    }

    /**
     * Devuelve todas las grabaciones.
     * GET /api/grabaciones
     * @return lista de Grabacion
     */
    @GetMapping
    public List<Grabacion> all() {
        return service.findAll();
    }

    /**
     * Busca una grabación por su ID.
     * GET /api/grabaciones/{id}
     * @param id ID de la grabación
     * @return Grabacion encontrada o 404
     */
    @GetMapping("/{id}")
    public ResponseEntity<Grabacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea una nueva grabación.
     * POST /api/grabaciones
     * @param g Grabacion a crear
     * @return Grabacion creada
     */
    @PostMapping
    public Grabacion create(@RequestBody Grabacion g) {
        return service.create(g);
    }

    /**
     * Actualiza una grabación existente.
     * PUT /api/grabaciones/{id}
     * @param id ID de la grabación
     * @param g Datos nuevos
     * @return Grabacion actualizada o 404
     */
    @PutMapping("/{id}")
    public ResponseEntity<Grabacion> update(@PathVariable Long id,
                                            @RequestBody Grabacion g) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, g)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina una grabación por ID.
     * DELETE /api/grabaciones/{id}
     * @param id ID de la grabación a eliminar
     * @return 204 si fue eliminada
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
