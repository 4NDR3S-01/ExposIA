package com.informaticonfing.spring.springboot_modulo.controller;

import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesResponseDTO;
import com.informaticonfing.spring.springboot_modulo.service.ParametrosIdealesService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controlador REST para la gestión de parámetros ideales.
 */
@RestController
@RequestMapping("/api/parametros-ideales")
public class ParametrosIdealesController {

    private final ParametrosIdealesService service;

    public ParametrosIdealesController(ParametrosIdealesService service) {
        this.service = service;
    }

    /**
     * Obtiene todos los parámetros ideales.
     * @return lista de ParametrosIdealesResponseDTO
     */
    @GetMapping
    public List<ParametrosIdealesResponseDTO> all() {
        return service.findAll();
    }

    /**
     * Busca un parámetro ideal por su ID.
     * @param id identificador del parámetro ideal
     * @return ParametrosIdealesResponseDTO si existe, 404 si no existe
     */
    @GetMapping("/{id}")
    public ResponseEntity<ParametrosIdealesResponseDTO> byId(@PathVariable Long id) {
        return service.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo parámetro ideal.
     * @param dto datos del nuevo parámetro ideal
     * @return el parámetro ideal creado
     */
    @PostMapping
    public ParametrosIdealesResponseDTO create(@RequestBody ParametrosIdealesRequestDTO dto) {
        return service.create(dto);
    }

    /**
     * Actualiza un parámetro ideal por su ID.
     * @param id identificador del parámetro ideal
     * @param dto nuevos datos del parámetro ideal
     * @return el parámetro ideal actualizado, o 404 si no existe
     */
    @PutMapping("/{id}")
    public ResponseEntity<ParametrosIdealesResponseDTO> update(@PathVariable Long id,
                                                               @RequestBody ParametrosIdealesRequestDTO dto) {
        return service.findById(id)
                .map(existing -> ResponseEntity.ok(service.update(id, dto)))
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * Elimina un parámetro ideal por su ID.
     * @param id identificador del parámetro ideal
     * @return respuesta vacía (204 No Content)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
