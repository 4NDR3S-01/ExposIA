package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.model.FeedbackCalificacion;
import com.informaticonfing.spring.springboot_modulo.repository.FeedbackCalificacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * Servicio para la lógica de negocio de FeedbackCalificacion.
 */
@Service
public class FeedbackCalificacionService {
    private final FeedbackCalificacionRepository repository;

    public FeedbackCalificacionService(FeedbackCalificacionRepository repository) {
        this.repository = repository;
    }

    public List<FeedbackCalificacion> findAll() {
        return repository.findAll();
    }

    public Optional<FeedbackCalificacion> findById(Long id) {
        return repository.findById(id);
    }

    public FeedbackCalificacion create(FeedbackCalificacion f) {
        return repository.save(f);
    }

    public FeedbackCalificacion update(Long id, FeedbackCalificacion f) {
        f.setId(id);
        return repository.save(f);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
