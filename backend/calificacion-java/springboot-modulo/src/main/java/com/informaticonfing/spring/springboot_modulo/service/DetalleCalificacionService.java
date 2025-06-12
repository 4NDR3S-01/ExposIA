package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.DetalleCalificacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.CriterioEvaluacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.DetalleCalificacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de detalles de calificación.
 */
@Service
public class DetalleCalificacionService {
    private final DetalleCalificacionRepository repository;
    private final CalificacionRepository calificacionRepo;
    private final CriterioEvaluacionRepository criterioRepo;

    public DetalleCalificacionService(
            DetalleCalificacionRepository repository,
            CalificacionRepository calificacionRepo,
            CriterioEvaluacionRepository criterioRepo
    ) {
        this.repository = repository;
        this.calificacionRepo = calificacionRepo;
        this.criterioRepo = criterioRepo;
    }

    /**
     * Obtiene todos los detalles de calificación.
     * @return lista de DetalleCalificacionResponseDTO
     */
    public List<DetalleCalificacionResponseDTO> findAll() {
        return repository.findAll()
            .stream()
            .map(DetalleCalificacionMapper::toDTO)
            .collect(Collectors.toList());
    }

    /**
     * Busca un detalle por su ID.
     * @param id identificador del detalle
     * @return DetalleCalificacionResponseDTO si existe, vacío si no
     */
    public Optional<DetalleCalificacionResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(DetalleCalificacionMapper::toDTO);
    }

    /**
     * Crea un nuevo detalle de calificación.
     * @param dto datos del nuevo detalle
     * @return el detalle creado
     */
    public DetalleCalificacionResponseDTO create(DetalleCalificacionRequestDTO dto) {
        Calificacion calificacion = null;
        if (dto.getCalificacionId() != null) {
            calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        }
        CriterioEvaluacion criterio = null;
        if (dto.getCriterioId() != null) {
            criterio = criterioRepo.findById(dto.getCriterioId()).orElse(null);
        }
        DetalleCalificacion entidad = DetalleCalificacionMapper.toEntity(dto, calificacion, criterio);
        DetalleCalificacion saved = repository.save(entidad);
        return DetalleCalificacionMapper.toDTO(saved);
    }

    /**
     * Actualiza un detalle existente.
     * @param id identificador del detalle a actualizar
     * @param dto nuevos datos del detalle
     * @return el detalle actualizado
     */
    public DetalleCalificacionResponseDTO update(Long id, DetalleCalificacionRequestDTO dto) {
        Calificacion calificacion = null;
        if (dto.getCalificacionId() != null) {
            calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        }
        CriterioEvaluacion criterio = null;
        if (dto.getCriterioId() != null) {
            criterio = criterioRepo.findById(dto.getCriterioId()).orElse(null);
        }
        DetalleCalificacion entidad = DetalleCalificacionMapper.toEntity(dto, calificacion, criterio);
        entidad.setId(id);
        DetalleCalificacion saved = repository.save(entidad);
        return DetalleCalificacionMapper.toDTO(saved);
    }

    /**
     * Elimina un detalle por su ID.
     * @param id identificador del detalle a eliminar
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
