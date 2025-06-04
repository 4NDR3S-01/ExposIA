package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.DetalleCalificacionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/detalles")
public class DetalleCalificacionController {

    private final DetalleCalificacionService service;

    public DetalleCalificacionController(DetalleCalificacionService service) {
        this.service = service;
    }

    @GetMapping
    public List<DetalleCalificacionResponseDTO> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<DetalleCalificacionResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public DetalleCalificacionResponseDTO create(@RequestBody DetalleCalificacionRequestDTO dto) {
        return service.create(dto);
    }

    @PutMapping("/{id}")
    public ResponseEntity<DetalleCalificacionResponseDTO> update(@PathVariable Long id,
                                                                 @RequestBody DetalleCalificacionRequestDTO dto) {
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
