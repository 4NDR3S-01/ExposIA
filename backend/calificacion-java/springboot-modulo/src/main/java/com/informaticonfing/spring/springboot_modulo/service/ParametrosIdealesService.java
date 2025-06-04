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

@Service
public class ParametrosIdealesService {
    private final ParametrosIdealesRepository repository;

    public ParametrosIdealesService(ParametrosIdealesRepository repository) {
        this.repository = repository;
    }

    public List<ParametrosIdealesResponseDTO> findAll() {
        return repository.findAll().stream().map(ParametrosIdealesMapper::toDTO).collect(Collectors.toList());
    }

    public Optional<ParametrosIdealesResponseDTO> findById(Long id) {
        return repository.findById(id).map(ParametrosIdealesMapper::toDTO);
    }

    public ParametrosIdealesResponseDTO create(ParametrosIdealesRequestDTO dto) {
        ParametrosIdeales entidad = ParametrosIdealesMapper.toEntity(dto);
        ParametrosIdeales saved = repository.save(entidad);
        return ParametrosIdealesMapper.toDTO(saved);
    }

    public ParametrosIdealesResponseDTO update(Long id, ParametrosIdealesRequestDTO dto) {
        ParametrosIdeales entidad = ParametrosIdealesMapper.toEntity(dto);
        entidad.setId(id);
        ParametrosIdeales saved = repository.save(entidad);
        return ParametrosIdealesMapper.toDTO(saved);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
