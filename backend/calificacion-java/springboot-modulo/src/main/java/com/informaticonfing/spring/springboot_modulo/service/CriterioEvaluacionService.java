package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.CriterioEvaluacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.repository.CriterioEvaluacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de criterios de evaluación.
 */
@Service
public class CriterioEvaluacionService {
    private final CriterioEvaluacionRepository repository;

    public CriterioEvaluacionService(CriterioEvaluacionRepository repository) {
        this.repository = repository;
    }

    /**
     * Obtiene todos los criterios de evaluación.
     * @return lista de CriterioEvaluacionResponseDTO
     */
    public List<CriterioEvaluacionResponseDTO> findAll() {
        return repository.findAll()
            .stream()
            .map(CriterioEvaluacionMapper::toDTO)
            .collect(Collectors.toList());
    }

    /**
     * Busca un criterio por su ID.
     * @param id identificador del criterio
     * @return CriterioEvaluacionResponseDTO si existe, vacío si no
     */
    public Optional<CriterioEvaluacionResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(CriterioEvaluacionMapper::toDTO);
    }

    /**
     * Crea un nuevo criterio de evaluación.
     * @param dto datos del nuevo criterio
     * @return el criterio creado
     */
    public CriterioEvaluacionResponseDTO create(CriterioEvaluacionRequestDTO dto) {
        CriterioEvaluacion entidad = CriterioEvaluacionMapper.toEntity(dto);
        CriterioEvaluacion saved = repository.save(entidad);
        return CriterioEvaluacionMapper.toDTO(saved);
    }

    /**
     * Actualiza un criterio existente.
     * @param id identificador del criterio a actualizar
     * @param dto nuevos datos del criterio
     * @return el criterio actualizado
     */
    public CriterioEvaluacionResponseDTO update(Long id, CriterioEvaluacionRequestDTO dto) {
        CriterioEvaluacion entidad = CriterioEvaluacionMapper.toEntity(dto);
        entidad.setId(id);
        CriterioEvaluacion saved = repository.save(entidad);
        return CriterioEvaluacionMapper.toDTO(saved);
    }

    /**
     * Elimina un criterio por su ID.
     * @param id identificador del criterio a eliminar
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
