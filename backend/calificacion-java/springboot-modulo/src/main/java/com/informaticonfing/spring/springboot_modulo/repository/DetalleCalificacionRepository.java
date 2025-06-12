package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import java.util.List;

/**
 * Repositorio JPA para DetalleCalificacion.
 */
public interface DetalleCalificacionRepository extends JpaRepository<DetalleCalificacion, Long> {
    // Obtiene todos los detalles asociados a una calificación
    List<DetalleCalificacion> findByCalificacionId(Long calificacionId);
}
