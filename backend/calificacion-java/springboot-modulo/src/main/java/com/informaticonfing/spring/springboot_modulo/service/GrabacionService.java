package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.Grabacion;
import com.informaticonfing.spring.springboot_modulo.repository.GrabacionRepository;

/**
 * Servicio de lógica para la gestión de grabaciones de evidencia.
 * Permite CRUD sobre las grabaciones almacenadas en el sistema.
 */
@Service
@Transactional
public class GrabacionService {
    private final GrabacionRepository repo;

    /**
     * Constructor para inyectar el repositorio.
     * @param repo Repositorio de Grabacion
     */
    public GrabacionService(GrabacionRepository repo) {
        this.repo = repo;
    }

    /**
     * Crea una nueva grabación.
     * @param g Objeto Grabacion
     * @return Grabacion creada
     */
    public Grabacion create(Grabacion g) {
        return repo.save(g);
    }

    /**
     * Lista todas las grabaciones existentes.
     * @return lista de Grabacion
     */
    public List<Grabacion> findAll() {
        return repo.findAll();
    }

    /**
     * Busca una grabación por su ID.
     * @param id ID de la grabación
     * @return Optional con la grabación si existe, vacío si no
     */
    public Optional<Grabacion> findById(Long id) {
        return repo.findById(id);
    }

    /**
     * Actualiza los datos de una grabación existente.
     * @param id ID de la grabación
     * @param g Datos nuevos
     * @return Grabacion actualizada
     */
    public Grabacion update(Long id, Grabacion g) {
        g.setId(id);
        return repo.save(g);
    }

    /**
     * Elimina una grabación por su ID.
     * @param id ID de la grabación a eliminar
     */
    public void delete(Long id) {
        repo.deleteById(id);
    }
}
