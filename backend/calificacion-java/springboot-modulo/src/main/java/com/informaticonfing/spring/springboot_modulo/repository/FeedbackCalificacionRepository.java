package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.FeedbackCalificacion;

/**
 * Repositorio JPA para FeedbackCalificacion.
 */
public interface FeedbackCalificacionRepository extends JpaRepository<FeedbackCalificacion, Long> {
}
