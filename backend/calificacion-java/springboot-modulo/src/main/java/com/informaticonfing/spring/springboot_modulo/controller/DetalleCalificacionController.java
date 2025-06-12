package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.DetalleCalificacionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controlador REST para la gestión de detalles de calificación.
 */
@RestController
@RequestMapping("/api/detalles")
public class DetalleCalificacionController {

    private final DetalleCalificacionService service;

    public DetalleCalificacionController(DetalleCalificacionService service) {
        this.service = service;
    }

    /**
     * Obtiene todos los detalles de calificación.
     * @return lista de DetalleCalificacionResponseDTO
     */
    @GetMapping
    public List<DetalleCalificacionResponseDTO> all() {
        return service.findAll();
    }

    /**
     * Busca un detalle de calificación por su ID.
     * @param id identificador del detalle
     * @return DetalleCalificacionResponseDTO si existe, 404 si no existe
     */
    @GetMapping("/{id}")
    public ResponseEntity<DetalleCalificacionResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo detalle de calificación.
     * @param dto datos del nuevo detalle
     * @return el detalle creado
     */
    @PostMapping
    public DetalleCalificacionResponseDTO create(@RequestBody DetalleCalificacionRequestDTO dto) {
        return service.create(dto);
    }

    /**
     * Actualiza un detalle de calificación por su ID.
     * @param id identificador del detalle
     * @param dto nuevos datos del detalle
     * @return el detalle actualizado, o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<DetalleCalificacionResponseDTO> update(@PathVariable Long id,
                                                                 @RequestBody DetalleCalificacionRequestDTO dto) {
        return service.findById(id)
                .map(existing -> ResponseEntity.ok(service.update(id, dto)))
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un detalle de calificación por su ID.
     * @param id identificador del detalle
     * @return respuesta vacía (204 No Content)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
