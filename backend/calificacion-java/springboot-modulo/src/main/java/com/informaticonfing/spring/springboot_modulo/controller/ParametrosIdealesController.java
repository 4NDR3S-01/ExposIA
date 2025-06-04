package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.ParametrosIdealesService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/parametros-ideales")
public class ParametrosIdealesController {

    private final ParametrosIdealesService service;

    public ParametrosIdealesController(ParametrosIdealesService service) {
        this.service = service;
    }

    @GetMapping
    public List<ParametrosIdealesResponseDTO> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<ParametrosIdealesResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ParametrosIdealesResponseDTO create(@RequestBody ParametrosIdealesRequestDTO dto) {
        return service.create(dto);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ParametrosIdealesResponseDTO> update(@PathVariable Long id,
                                                               @RequestBody ParametrosIdealesRequestDTO dto) {
        if (service.findById(id).isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(service.update(id, dto));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
