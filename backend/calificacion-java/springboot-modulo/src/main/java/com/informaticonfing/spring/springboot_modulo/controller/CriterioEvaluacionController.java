package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.CriterioEvaluacionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controlador REST para la gestión de criterios de evaluación.
 */
@RestController
@RequestMapping("/api/criterios")
public class CriterioEvaluacionController {

    private final CriterioEvaluacionService service;

    public CriterioEvaluacionController(CriterioEvaluacionService service) {
        this.service = service;
    }

    /**
     * Obtiene todos los criterios de evaluación.
     * @return lista de CriterioEvaluacionResponseDTO
     */
    @GetMapping
    public List<CriterioEvaluacionResponseDTO> all() {
        return service.findAll();
    }

    /**
     * Busca un criterio de evaluación por su ID.
     * @param id identificador del criterio
     * @return CriterioEvaluacionResponseDTO si existe, 404 si no existe
     */
    @GetMapping("/{id}")
    public ResponseEntity<CriterioEvaluacionResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo criterio de evaluación.
     * @param dto datos del nuevo criterio
     * @return el criterio creado
     */
    @PostMapping
    public CriterioEvaluacionResponseDTO create(@RequestBody CriterioEvaluacionRequestDTO dto) {
        return service.create(dto);
    }

    /**
     * Actualiza un criterio de evaluación por su ID.
     * @param id identificador del criterio
     * @param dto nuevos datos del criterio
     * @return el criterio actualizado, o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<CriterioEvaluacionResponseDTO> update(@PathVariable Long id,
                                                                @RequestBody CriterioEvaluacionRequestDTO dto) {
        return service.findById(id)
                .map(existing -> ResponseEntity.ok(service.update(id, dto)))
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un criterio de evaluación por su ID.
     * @param id identificador del criterio
     * @return respuesta vacía (204 No Content)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
