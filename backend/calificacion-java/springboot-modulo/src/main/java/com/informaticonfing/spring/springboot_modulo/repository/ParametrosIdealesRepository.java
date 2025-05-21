package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;

public interface ParametrosIdealesRepository
        extends JpaRepository<ParametrosIdeales, Long> {
    // consultas adicionales van aquí
}
