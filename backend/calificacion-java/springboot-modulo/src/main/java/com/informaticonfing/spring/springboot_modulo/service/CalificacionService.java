package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.CalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.CalificacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de calificaciones.
 */
@Service
public class CalificacionService {
    private final CalificacionRepository repository;
    private final ParametrosIdealesRepository parametrosRepo;

    public CalificacionService(CalificacionRepository repository, ParametrosIdealesRepository parametrosRepo) {
        this.repository = repository;
        this.parametrosRepo = parametrosRepo;
    }

    /**
     * Obtiene todas las calificaciones.
     * @return lista de CalificacionResponseDTO
     */
    public List<CalificacionResponseDTO> findAll() {
        return repository.findAll()
            .stream()
            .map(CalificacionMapper::toDTO)
            .collect(Collectors.toList());
    }

    /**
     * Busca una calificación por su ID.
     * @param id identificador de la calificación
     * @return CalificacionResponseDTO si existe, vacío si no
     */
    public Optional<CalificacionResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(CalificacionMapper::toDTO);
    }

    /**
     * Crea una nueva calificación.
     * @param dto datos de la nueva calificación
     * @return la calificación creada
     */
    public CalificacionResponseDTO create(CalificacionRequestDTO dto) {
        ParametrosIdeales parametros = null;
        if (dto.getParametrosIdealesId() != null) {
            parametros = parametrosRepo.findById(dto.getParametrosIdealesId()).orElse(null);
        }
        Calificacion entidad = CalificacionMapper.toEntity(dto, parametros);
        Calificacion saved = repository.save(entidad);
        return CalificacionMapper.toDTO(saved);
    }

    /**
     * Actualiza una calificación existente.
     * @param id identificador de la calificación a actualizar
     * @param dto nuevos datos de la calificación
     * @return la calificación actualizada
     */
    public CalificacionResponseDTO update(Long id, CalificacionRequestDTO dto) {
        ParametrosIdeales parametros = null;
        if (dto.getParametrosIdealesId() != null) {
            parametros = parametrosRepo.findById(dto.getParametrosIdealesId()).orElse(null);
        }
        Calificacion entidad = CalificacionMapper.toEntity(dto, parametros);
        entidad.setId(id);
        Calificacion saved = repository.save(entidad);
        return CalificacionMapper.toDTO(saved);
    }

    /**
     * Elimina una calificación por su ID.
     * @param id identificador de la calificación a eliminar
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
