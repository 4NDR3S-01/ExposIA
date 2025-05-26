package com.informaticonfing.spring.springboot_modulo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.informaticonfing.spring.springboot_modulo.model.Grabacion;

/**
 * Repositorio para la entidad Grabacion.
 * Permite operaciones CRUD sobre las grabaciones almacenadas.
 */
@Repository
public interface GrabacionRepository extends JpaRepository<Grabacion, Long> {
    // Puedes agregar métodos personalizados, por ejemplo:
    // Optional<Grabacion> findByNombreArchivo(String nombreArchivo);
}
