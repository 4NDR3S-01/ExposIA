package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;

public interface CalificacionRepository
        extends JpaRepository<Calificacion, Long> {
    // aquí puedes añadir consultas personalizadas si las necesitas
}
