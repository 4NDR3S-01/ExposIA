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

    public List<DetalleCalificacionResponseDTO> findAll() {
        return repository.findAll().stream().map(DetalleCalificacionMapper::toDTO).collect(Collectors.toList());
    }

    public Optional<DetalleCalificacionResponseDTO> findById(Long id) {
        return repository.findById(id).map(DetalleCalificacionMapper::toDTO);
    }

    public DetalleCalificacionResponseDTO create(DetalleCalificacionRequestDTO dto) {
        Calificacion calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        CriterioEvaluacion criterio = criterioRepo.findById(dto.getCriterioId()).orElse(null);
        DetalleCalificacion entidad = DetalleCalificacionMapper.toEntity(dto, calificacion, criterio);
        DetalleCalificacion saved = repository.save(entidad);
        return DetalleCalificacionMapper.toDTO(saved);
    }

    public DetalleCalificacionResponseDTO update(Long id, DetalleCalificacionRequestDTO dto) {
        Calificacion calificacion = calificacionRepo.findById(dto.getCalificacionId()).orElse(null);
        CriterioEvaluacion criterio = criterioRepo.findById(dto.getCriterioId()).orElse(null);
        DetalleCalificacion entidad = DetalleCalificacionMapper.toEntity(dto, calificacion, criterio);
        entidad.setId(id);
        DetalleCalificacion saved = repository.save(entidad);
        return DetalleCalificacionMapper.toDTO(saved);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
