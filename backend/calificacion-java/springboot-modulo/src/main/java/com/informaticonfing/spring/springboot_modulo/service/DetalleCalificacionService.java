package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.repository.DetalleCalificacionRepository;

/**
 * Servicio de lógica para los detalles de calificación (puntajes individuales).
 * Permite crear, buscar, actualizar y borrar detalles de cada evaluación por criterio.
 */
@Service
@Transactional
public class DetalleCalificacionService {
    private final DetalleCalificacionRepository repo;

    /**
     * Constructor para inyectar el repositorio.
     * @param repo Repositorio de DetalleCalificacion
     */
    public DetalleCalificacionService(DetalleCalificacionRepository repo) {
        this.repo = repo;
    }

    /**
     * Crea un nuevo detalle de calificación.
     * @param d DetalleCalificacion a guardar
     * @return Detalle creado
     */
    public DetalleCalificacion create(DetalleCalificacion d) {
        return repo.save(d);
    }

    /**
     * Lista todos los detalles de calificación existentes.
     * @return lista de DetalleCalificacion
     */
    public List<DetalleCalificacion> findAll() {
        return repo.findAll();
    }

    /**
     * Busca un detalle por su ID.
     * @param id ID del detalle
     * @return Optional con el detalle si existe, vacío si no
     */
    public Optional<DetalleCalificacion> findById(Long id) {
        return repo.findById(id);
    }

    /**
     * Actualiza un detalle de calificación existente.
     * @param id ID del detalle
     * @param d Datos nuevos
     * @return Detalle actualizado
     */
    public DetalleCalificacion update(Long id, DetalleCalificacion d) {
        d.setId(id);
        return repo.save(d);
    }

    /**
     * Elimina un detalle de calificación por su ID.
     * @param id ID del detalle a eliminar
     */
    public void delete(Long id) {
        repo.deleteById(id);
    }
}
