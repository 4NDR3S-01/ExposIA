package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.informaticonfing.spring.springboot_modulo.model.Calificacion;

/**
 * Repositorio para la entidad Calificacion.
 * Hereda de JpaRepository para proveer operaciones CRUD y consultas JPA estándar.
 * 
 * Puedes agregar métodos personalizados aquí si necesitas búsquedas avanzadas.
 */
@Repository
public interface CalificacionRepository extends JpaRepository<Calificacion, Long> {
    // Ejemplo de método personalizado:
    // List<Calificacion> findByPuntajeGreaterThan(double minPuntaje);
}
