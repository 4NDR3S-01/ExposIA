package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.repository.CriterioEvaluacionRepository;

/**
 * Servicio de lógica para los criterios de evaluación.
 * Permite la gestión CRUD de los criterios usados por la IA.
 */
@Service
@Transactional
public class CriterioEvaluacionService {
    private final CriterioEvaluacionRepository repo;

    /**
     * Constructor para inyectar el repositorio.
     * @param repo Repositorio de CriterioEvaluacion
     */
    public CriterioEvaluacionService(CriterioEvaluacionRepository repo) {
        this.repo = repo;
    }

    /**
     * Crea y persiste un nuevo criterio de evaluación.
     * @param c Objeto CriterioEvaluacion
     * @return Criterio creado
     */
    public CriterioEvaluacion create(CriterioEvaluacion c) {
        return repo.save(c);
    }

    /**
     * Devuelve la lista de todos los criterios registrados.
     * @return lista de CriterioEvaluacion
     */
    public List<CriterioEvaluacion> findAll() {
        return repo.findAll();
    }

    /**
     * Busca un criterio de evaluación por su ID.
     * @param id ID a buscar
     * @return Optional con el criterio si existe, vacío si no
     */
    public Optional<CriterioEvaluacion> findById(Long id) {
        return repo.findById(id);
    }

    /**
     * Actualiza los datos de un criterio existente.
     * @param id ID del criterio
     * @param c Datos nuevos
     * @return Criterio actualizado
     */
    public CriterioEvaluacion update(Long id, CriterioEvaluacion c) {
        c.setId(id);
        return repo.save(c);
    }

    /**
     * Elimina un criterio de evaluación por su ID.
     * @param id ID del criterio a eliminar
     */
    public void delete(Long id) {
        repo.deleteById(id);
    }
}
