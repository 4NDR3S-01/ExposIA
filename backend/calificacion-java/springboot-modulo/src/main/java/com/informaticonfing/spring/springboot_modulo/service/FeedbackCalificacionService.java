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

@Service
public class FeedbackCalificacionService {
    private final FeedbackCalificacionRepository repository;
    private final CalificacionRepository calificacionRepo;

    public FeedbackCalificacionService(FeedbackCalificacionRepository repository, CalificacionRepository calificacionRepo) {
        this.repository = repository;
        this.calificacionRepo = calificacionRepo;
    }

    public List<FeedbackCalificacionResponseDTO> findAll() {
        return repository.findAll().stream().map(FeedbackCalificacionMapper::toDTO).collect(Collectors.toList());
    }

    public Optional<FeedbackCalificacionResponseDTO> findById(Long id) {
        return repository.findById(id).map(FeedbackCalificacionMapper::toDTO);
    }

    public FeedbackCalificacionResponseDTO create(FeedbackCalificacionRequestDTO dto) {
        Calificacion calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        FeedbackCalificacion entidad = FeedbackCalificacionMapper.toEntity(dto, calificacion);
        FeedbackCalificacion saved = repository.save(entidad);
        return FeedbackCalificacionMapper.toDTO(saved);
    }

    public FeedbackCalificacionResponseDTO update(Long id, FeedbackCalificacionRequestDTO dto) {
        Calificacion calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        FeedbackCalificacion entidad = FeedbackCalificacionMapper.toEntity(dto, calificacion);
        entidad.setId(id);
        FeedbackCalificacion saved = repository.save(entidad);
        return FeedbackCalificacionMapper.toDTO(saved);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
