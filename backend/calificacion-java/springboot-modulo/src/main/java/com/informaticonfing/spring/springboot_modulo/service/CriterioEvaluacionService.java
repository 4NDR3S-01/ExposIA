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

@Service
public class CriterioEvaluacionService {
    private final CriterioEvaluacionRepository repository;

    public CriterioEvaluacionService(CriterioEvaluacionRepository repository) {
        this.repository = repository;
    }

    public List<CriterioEvaluacionResponseDTO> findAll() {
        return repository.findAll().stream().map(CriterioEvaluacionMapper::toDTO).collect(Collectors.toList());
    }

    public Optional<CriterioEvaluacionResponseDTO> findById(Long id) {
        return repository.findById(id).map(CriterioEvaluacionMapper::toDTO);
    }

    public CriterioEvaluacionResponseDTO create(CriterioEvaluacionRequestDTO dto) {
        CriterioEvaluacion entidad = CriterioEvaluacionMapper.toEntity(dto);
        CriterioEvaluacion saved = repository.save(entidad);
        return CriterioEvaluacionMapper.toDTO(saved);
    }

    public CriterioEvaluacionResponseDTO update(Long id, CriterioEvaluacionRequestDTO dto) {
        CriterioEvaluacion entidad = CriterioEvaluacionMapper.toEntity(dto);
        entidad.setId(id);
        CriterioEvaluacion saved = repository.save(entidad);
        return CriterioEvaluacionMapper.toDTO(saved);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
