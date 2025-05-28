package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * Servicio para la lógica de negocio de ParametrosIdeales.
 */
@Service
public class ParametrosIdealesService {
    private final ParametrosIdealesRepository repository;

    public ParametrosIdealesService(ParametrosIdealesRepository repository) {
        this.repository = repository;
    }

    /**
     * Lista todos los parámetros ideales.
     */
    public List<ParametrosIdeales> findAll() {
        return repository.findAll();
    }

    /**
     * Busca un parámetro ideal por ID.
     */
    public Optional<ParametrosIdeales> findById(Long id) {
        return repository.findById(id);
    }

    /**
     * Crea un nuevo parámetro ideal.
     */
    public ParametrosIdeales create(ParametrosIdeales p) {
        return repository.save(p);
    }

    /**
     * Actualiza un parámetro ideal existente.
     */
    public ParametrosIdeales update(Long id, ParametrosIdeales p) {
        p.setId(id);
        return repository.save(p);
    }

    /**
     * Elimina un parámetro ideal por ID.
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
