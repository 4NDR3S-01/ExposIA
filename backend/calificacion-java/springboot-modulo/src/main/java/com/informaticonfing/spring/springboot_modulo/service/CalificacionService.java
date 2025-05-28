package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * Servicio para la lógica de negocio de Calificacion.
 */
@Service
public class CalificacionService {

    private final CalificacionRepository repository;

    public CalificacionService(CalificacionRepository repository) {
        this.repository = repository;
    }

    /**
     * Lista todas las calificaciones.
     */
    public List<Calificacion> findAll() {
        return repository.findAll();
    }

    /**
     * Busca una calificación por ID.
     */
    public Optional<Calificacion> findById(Long id) {
        return repository.findById(id);
    }

    /**
     * Crea una nueva calificación.
     */
    public Calificacion create(Calificacion c) {
        return repository.save(c);
    }

    /**
     * Actualiza una calificación existente.
     */
    public Calificacion update(Long id, Calificacion c) {
        c.setId(id);
        return repository.save(c);
    }

    /**
     * Elimina una calificación por ID.
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
