// src/main/java/com/informaticonfing/spring/springboot_modulo/service/ParametrosIdealesService.java
package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;

/**
 * Servicio de lógica para los parámetros ideales de evaluación.
 * Permite la gestión CRUD de los parámetros base de comparación.
 */
@Service
@Transactional
public class ParametrosIdealesService {
    private final ParametrosIdealesRepository repo;

    /**
     * Constructor para inyectar el repositorio.
     * @param repo Repositorio de ParametrosIdeales
     */
    public ParametrosIdealesService(ParametrosIdealesRepository repo) {
        this.repo = repo;
    }

    /**
     * Crea un nuevo registro de parámetros ideales.
     * @param p Objeto ParametrosIdeales
     * @return Parámetro creado
     */
    public ParametrosIdeales create(ParametrosIdeales p) {
        return repo.save(p);
    }

    /**
     * Obtiene la lista de todos los parámetros ideales registrados.
     * @return lista de ParametrosIdeales
     */
    public List<ParametrosIdeales> findAll() {
        return repo.findAll();
    }

    /**
     * Busca un parámetro ideal por ID.
     * @param id ID a buscar
     * @return Optional con el parámetro si existe, vacío si no
     */
    public Optional<ParametrosIdeales> findById(Long id) {
        return repo.findById(id);
    }

    /**
     * Actualiza los datos de un parámetro ideal existente.
     * @param id ID del parámetro
     * @param p Datos nuevos
     * @return Parámetro actualizado
     */
    public ParametrosIdeales update(Long id, ParametrosIdeales p) {
        p.setId(id);
        return repo.save(p);
    }

    /**
     * Elimina un parámetro ideal por su ID.
     * @param id ID del parámetro a eliminar
     */
    public void delete(Long id) {
        repo.deleteById(id);
    }
}
