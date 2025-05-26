package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;

/**
 * Repositorio para la entidad ParametrosIdeales.
 * Permite operaciones CRUD sobre los parámetros ideales.
 */
@Repository
public interface ParametrosIdealesRepository extends JpaRepository<ParametrosIdeales, Long> {
    // Aquí puedes agregar métodos personalizados, por ejemplo:
    // List<ParametrosIdeales> findByClaridadIdealBetween(double min, double max);
}
