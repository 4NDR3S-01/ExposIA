package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;

/**
 * Repositorio JPA para Calificacion.
 */
public interface CalificacionRepository extends JpaRepository<Calificacion, Long> {
}
// Aquí puedes agregar métodos personalizados si algún día los necesitas.