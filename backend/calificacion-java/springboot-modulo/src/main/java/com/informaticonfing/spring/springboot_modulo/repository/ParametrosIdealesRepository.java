package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;

/**
 * Repositorio JPA para ParametrosIdeales.
 */
public interface ParametrosIdealesRepository extends JpaRepository<ParametrosIdeales, Long> {
    // Aquí puedes agregar métodos personalizados si algún día los necesitas.
}
