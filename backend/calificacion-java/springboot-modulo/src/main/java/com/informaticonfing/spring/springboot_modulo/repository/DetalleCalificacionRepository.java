package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;

/**
 * Repositorio para la entidad DetalleCalificacion.
 * Permite acceder y gestionar los detalles de cada calificación por criterio.
 */
@Repository
public interface DetalleCalificacionRepository extends JpaRepository<DetalleCalificacion, Long> {
    // Ejemplo de método personalizado:
    // List<DetalleCalificacion> findByCalificacionId(Long calificacionId);
}
