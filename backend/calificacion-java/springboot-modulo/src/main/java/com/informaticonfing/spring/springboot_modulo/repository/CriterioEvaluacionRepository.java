package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;

/**
 * Repositorio JPA para CriterioEvaluacion.
 */
public interface CriterioEvaluacionRepository extends JpaRepository<CriterioEvaluacion, Long> {
}
// Aquí puedes agregar métodos personalizados si algún día los necesitas.