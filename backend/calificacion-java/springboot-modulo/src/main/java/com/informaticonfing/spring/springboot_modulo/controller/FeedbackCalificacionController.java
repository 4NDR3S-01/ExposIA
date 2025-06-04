package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.FeedbackCalificacionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controlador REST para la gestión de feedback de calificación.
 */
@RestController
@RequestMapping("/api/feedback")
public class FeedbackCalificacionController {

    private final FeedbackCalificacionService service;

    public FeedbackCalificacionController(FeedbackCalificacionService service) {
        this.service = service;
    }

    /**
     * Obtiene todos los feedbacks.
     * @return lista de FeedbackCalificacionResponseDTO
     */
    @GetMapping
    public List<FeedbackCalificacionResponseDTO> all() {
        return service.findAll();
    }

    /**
     * Busca un feedback por su ID.
     * @param id identificador del feedback
     * @return FeedbackCalificacionResponseDTO si existe, 404 si no existe
     */
    @GetMapping("/{id}")
    public ResponseEntity<FeedbackCalificacionResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo feedback de calificación.
     * @param dto datos del nuevo feedback
     * @return el feedback creado
     */
    @PostMapping
    public FeedbackCalificacionResponseDTO create(@RequestBody FeedbackCalificacionRequestDTO dto) {
        return service.create(dto);
    }

    /**
     * Actualiza un feedback por su ID.
     * @param id identificador del feedback
     * @param dto nuevos datos del feedback
     * @return el feedback actualizado, o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<FeedbackCalificacionResponseDTO> update(@PathVariable Long id,
                                                                  @RequestBody FeedbackCalificacionRequestDTO dto) {
        return service.findById(id)
                .map(existing -> ResponseEntity.ok(service.update(id, dto)))
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un feedback por su ID.
     * @param id identificador del feedback
     * @return respuesta vacía (204 No Content)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
