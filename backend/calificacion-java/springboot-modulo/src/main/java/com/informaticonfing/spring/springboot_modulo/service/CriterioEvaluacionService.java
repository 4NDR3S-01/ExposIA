package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.repository.CriterioEvaluacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * Servicio para la lógica de negocio de CriterioEvaluacion.
 */
@Service
public class CriterioEvaluacionService {
    private final CriterioEvaluacionRepository repository;

    public CriterioEvaluacionService(CriterioEvaluacionRepository repository) {
        this.repository = repository;
    }

    public List<CriterioEvaluacion> findAll() {
        return repository.findAll();
    }

    public Optional<CriterioEvaluacion> findById(Long id) {
        return repository.findById(id);
    }

    public CriterioEvaluacion create(CriterioEvaluacion c) {
        return repository.save(c);
    }

    public CriterioEvaluacion update(Long id, CriterioEvaluacion c) {
        c.setId(id);
        return repository.save(c);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
