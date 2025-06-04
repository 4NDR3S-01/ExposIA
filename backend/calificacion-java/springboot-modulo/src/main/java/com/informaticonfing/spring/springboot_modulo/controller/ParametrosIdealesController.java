package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.service.ParametrosIdealesService;
import com.informaticonfing.spring.springboot_modulo.util.ParametrosIdealesConstantes;

/**
 * Controlador REST para los parámetros ideales de evaluación.
 * Permite consultar, modificar y exponer el estándar global de parámetros ideales.
 */
@RestController
@RequestMapping("/api/parametros")
public class ParametrosIdealesController {
    private final ParametrosIdealesService service;

    /**
     * Constructor inyectando el servicio correspondiente.
     * @param service Servicio de ParametrosIdeales
     */
    public ParametrosIdealesController(ParametrosIdealesService service) {
        this.service = service;
    }

    /**
     * Obtiene la lista de todos los parámetros ideales existentes.
     * GET /api/parametros
     * @return lista de ParametrosIdeales
     */
    @GetMapping
    public List<ParametrosIdeales> all() {
        return service.findAll();
    }

    /**
     * Busca un parámetro ideal por ID.
     * GET /api/parametros/{id}
     * @param id ID del parámetro ideal
     * @return ParametrosIdeales si existe o 404
     */
    @GetMapping("/{id}")
    public ResponseEntity<ParametrosIdeales> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo parámetro ideal.
     * POST /api/parametros
     * @param p Objeto ParametrosIdeales en el body
     * @return Parámetro creado
     */
    @PostMapping
    public ParametrosIdeales create(@RequestBody ParametrosIdeales p) {
        return service.create(p);
    }

    /**
     * Actualiza un parámetro ideal existente.
     * PUT /api/parametros/{id}
     * @param id ID del parámetro a actualizar
     * @param p Parámetros nuevos en el body
     * @return Parámetro actualizado o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<ParametrosIdeales> update(@PathVariable Long id,
                                                    @RequestBody ParametrosIdeales p) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, p)))
                      .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un parámetro ideal por ID.
     * DELETE /api/parametros/{id}
     * @param id ID del parámetro a eliminar
     * @return 204 si se borró correctamente
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }

    /**
     * Devuelve los parámetros ideales estándar definidos en código.
     * GET /api/parametros/estandar
     * @return ParametrosIdeales con valores globales (solo lectura)
     */
    @GetMapping("/estandar")
    public ParametrosIdeales getParametrosEstandar() {
        ParametrosIdeales p = new ParametrosIdeales();
        p.setClaridadIdeal(ParametrosIdealesConstantes.CLARIDAD_IDEAL);
        p.setVelocidadIdeal(ParametrosIdealesConstantes.VELOCIDAD_IDEAL);
        p.setPausasIdeales(ParametrosIdealesConstantes.PAUSAS_IDEALES);
        p.setOtrosParametros(null);
        return p;
    }
}
