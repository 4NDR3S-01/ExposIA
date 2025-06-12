package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.FeedbackCalificacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.FeedbackCalificacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.FeedbackCalificacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de feedback de calificación.
 */
@Service
public class FeedbackCalificacionService {
    private final FeedbackCalificacionRepository repository;
    private final CalificacionRepository calificacionRepo;

    public FeedbackCalificacionService(FeedbackCalificacionRepository repository, CalificacionRepository calificacionRepo) {
        this.repository = repository;
        this.calificacionRepo = calificacionRepo;
    }

    /**
     * Obtiene todos los feedbacks.
     * @return lista de FeedbackCalificacionResponseDTO
     */
    public List<FeedbackCalificacionResponseDTO> findAll() {
        return repository.findAll()
            .stream()
            .map(FeedbackCalificacionMapper::toDTO)
            .collect(Collectors.toList());
    }

    /**
     * Busca un feedback por su ID.
     * @param id identificador del feedback
     * @return FeedbackCalificacionResponseDTO si existe, vacío si no
     */
    public Optional<FeedbackCalificacionResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(FeedbackCalificacionMapper::toDTO);
    }

    /**
     * Crea un nuevo feedback de calificación.
     * @param dto datos del nuevo feedback
     * @return el feedback creado
     */
    public FeedbackCalificacionResponseDTO create(FeedbackCalificacionRequestDTO dto) {
        Calificacion calificacion = null;
        if (dto.getCalificacionId() != null) {
            calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        }
        FeedbackCalificacion entidad = FeedbackCalificacionMapper.toEntity(dto, calificacion);
        FeedbackCalificacion saved = repository.save(entidad);
        return FeedbackCalificacionMapper.toDTO(saved);
    }

    /**
     * Actualiza un feedback existente.
     * @param id identificador del feedback a actualizar
     * @param dto nuevos datos del feedback
     * @return el feedback actualizado
     */
    public FeedbackCalificacionResponseDTO update(Long id, FeedbackCalificacionRequestDTO dto) {
        Calificacion calificacion = null;
        if (dto.getCalificacionId() != null) {
            calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        }
        FeedbackCalificacion entidad = FeedbackCalificacionMapper.toEntity(dto, calificacion);
        entidad.setId(id);
        FeedbackCalificacion saved = repository.save(entidad);
        return FeedbackCalificacionMapper.toDTO(saved);
    }

    /**
     * Elimina un feedback por su ID.
     * @param id identificador del feedback a eliminar
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
