package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.service.CalificacionService;

@RestController
@RequestMapping("/api/calificaciones")
public class CalificacionController {
    private final CalificacionService service;

    public CalificacionController(CalificacionService service) {
        this.service = service;
    }

    @GetMapping
    public List<Calificacion> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Calificacion> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Calificacion create(@RequestBody Calificacion c) {
        return service.create(c);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Calificacion> update(@PathVariable Long id,
                                               @RequestBody Calificacion c) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, c)))
                      .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
