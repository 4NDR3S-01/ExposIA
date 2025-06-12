package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.ParametrosIdealesMapper;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de parámetros ideales.
 */
@Service
public class ParametrosIdealesService {
    private final ParametrosIdealesRepository repository;

    public ParametrosIdealesService(ParametrosIdealesRepository repository) {
        this.repository = repository;
    }

    /**
     * Obtiene todos los parámetros ideales.
     * @return lista de ParametrosIdealesResponseDTO
     */
    public List<ParametrosIdealesResponseDTO> findAll() {
        return repository.findAll()
            .stream()
            .map(ParametrosIdealesMapper::toDTO)
            .collect(Collectors.toList());
    }

    /**
     * Busca parámetros ideales por su ID.
     * @param id identificador de los parámetros ideales
     * @return ParametrosIdealesResponseDTO si existe, vacío si no
     */
    public Optional<ParametrosIdealesResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(ParametrosIdealesMapper::toDTO);
    }

    /**
     * Crea nuevos parámetros ideales.
     * @param dto datos de los nuevos parámetros ideales
     * @return los parámetros ideales creados
     */
    public ParametrosIdealesResponseDTO create(ParametrosIdealesRequestDTO dto) {
        ParametrosIdeales entidad = ParametrosIdealesMapper.toEntity(dto);
        ParametrosIdeales saved = repository.save(entidad);
        return ParametrosIdealesMapper.toDTO(saved);
    }

    /**
     * Actualiza parámetros ideales existentes.
     * @param id identificador de los parámetros ideales a actualizar
     * @param dto nuevos datos
     * @return los parámetros ideales actualizados
     */
    public ParametrosIdealesResponseDTO update(Long id, ParametrosIdealesRequestDTO dto) {
        ParametrosIdeales entidad = ParametrosIdealesMapper.toEntity(dto);
        entidad.setId(id);
        ParametrosIdeales saved = repository.save(entidad);
        return ParametrosIdealesMapper.toDTO(saved);
    }

    /**
     * Elimina parámetros ideales por su ID.
     * @param id identificador de los parámetros ideales a eliminar
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
