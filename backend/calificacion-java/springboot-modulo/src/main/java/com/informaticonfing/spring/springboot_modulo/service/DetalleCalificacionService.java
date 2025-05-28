package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.repository.DetalleCalificacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * Servicio para la lógica de negocio de DetalleCalificacion.
 */
@Service
public class DetalleCalificacionService {
    private final DetalleCalificacionRepository repository;

    public DetalleCalificacionService(DetalleCalificacionRepository repository) {
        this.repository = repository;
    }

    public List<DetalleCalificacion> findAll() {
        return repository.findAll();
    }

    public Optional<DetalleCalificacion> findById(Long id) {
        return repository.findById(id);
    }

    public DetalleCalificacion create(DetalleCalificacion d) {
        return repository.save(d);
    }

    public DetalleCalificacion update(Long id, DetalleCalificacion d) {
        d.setId(id);
        return repository.save(d);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
