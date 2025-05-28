package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;

/**
 * Repositorio JPA para DetalleCalificacion.
 */
public interface DetalleCalificacionRepository extends JpaRepository<DetalleCalificacion, Long> {
}
// Aquí puedes agregar métodos personalizados si algún día los necesitas.