package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.CriterioEvaluacionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/criterios")
public class CriterioEvaluacionController {

    private final CriterioEvaluacionService service;

    public CriterioEvaluacionController(CriterioEvaluacionService service) {
        this.service = service;
    }

    @GetMapping
    public List<CriterioEvaluacionResponseDTO> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<CriterioEvaluacionResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public CriterioEvaluacionResponseDTO create(@RequestBody CriterioEvaluacionRequestDTO dto) {
        return service.create(dto);
    }

    @PutMapping("/{id}")
    public ResponseEntity<CriterioEvaluacionResponseDTO> update(@PathVariable Long id,
                                                          @RequestBody CriterioEvaluacionRequestDTO dto) {
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
