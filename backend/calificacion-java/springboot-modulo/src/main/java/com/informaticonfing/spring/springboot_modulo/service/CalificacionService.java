package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;

@Service
@Transactional
public class CalificacionService {
    private final CalificacionRepository repo;

    public CalificacionService(CalificacionRepository repo) {
        this.repo = repo;
    }

    public Calificacion create(Calificacion c) {
        return repo.save(c);
    }

    public List<Calificacion> findAll() {
        return repo.findAll();
    }

    public Optional<Calificacion> findById(Long id) {
        return repo.findById(id);
    }

    public Calificacion update(Long id, Calificacion c) {
        c.setId(id);
        return repo.save(c);
    }

    public void delete(Long id) {
        repo.deleteById(id);
    }
}
