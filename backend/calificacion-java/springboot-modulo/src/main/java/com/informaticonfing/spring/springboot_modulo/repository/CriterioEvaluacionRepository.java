package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;

/**
 * Repositorio para la entidad CriterioEvaluacion.
 * Acceso a datos de los criterios que usa la IA para calificar.
 */
@Repository
public interface CriterioEvaluacionRepository extends JpaRepository<CriterioEvaluacion, Long> {
    // Por ejemplo:
    // Optional<CriterioEvaluacion> findByNombre(String nombre);
}
