package com.informaticonfing.spring.springboot_modulo.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.service.ParametrosIdealesService;

@RestController
@RequestMapping("/api/parametros")
public class ParametrosIdealesController {
    private final ParametrosIdealesService service;

    public ParametrosIdealesController(ParametrosIdealesService service) {
        this.service = service;
    }

    @GetMapping
    public List<ParametrosIdeales> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<ParametrosIdeales> byId(@PathVariable Long id) {
        return service.findById(id)
                      .map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ParametrosIdeales create(@RequestBody ParametrosIdeales p) {
        return service.create(p);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ParametrosIdeales> update(@PathVariable Long id,
                                                    @RequestBody ParametrosIdeales p) {
        return service.findById(id)
                      .map(existing -> ResponseEntity.ok(service.update(id, p)))
                      .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
