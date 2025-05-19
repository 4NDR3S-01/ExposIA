// src/main/java/com/informaticonfing/spring/springboot_modulo/service/ParametrosIdealesService.java
package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;

@Service
@Transactional
public class ParametrosIdealesService {
    private final ParametrosIdealesRepository repo;

    public ParametrosIdealesService(ParametrosIdealesRepository repo) {
        this.repo = repo;
    }

    public ParametrosIdeales create(ParametrosIdeales p) {
        return repo.save(p);
    }

    public List<ParametrosIdeales> findAll() {
        return repo.findAll();
    }

    public Optional<ParametrosIdeales> findById(Long id) {
        return repo.findById(id);
    }

    public ParametrosIdeales update(Long id, ParametrosIdeales p) {
        p.setId(id);         // ahora existe
        return repo.save(p); // y save() es visible
    }

    public void delete(Long id) {
        repo.deleteById(id);
    }
}
