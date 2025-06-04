package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.FeedbackCalificacionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/feedback")
public class FeedbackCalificacionController {

    private final FeedbackCalificacionService service;

    public FeedbackCalificacionController(FeedbackCalificacionService service) {
        this.service = service;
    }

    @GetMapping
    public List<FeedbackCalificacionResponseDTO> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<FeedbackCalificacionResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public FeedbackCalificacionResponseDTO create(@RequestBody FeedbackCalificacionRequestDTO dto) {
        return service.create(dto);
    }

    @PutMapping("/{id}")
    public ResponseEntity<FeedbackCalificacionResponseDTO> update(@PathVariable Long id,
                                                                  @RequestBody FeedbackCalificacionRequestDTO dto) {
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
