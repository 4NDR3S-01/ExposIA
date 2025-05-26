package com.informaticonfing.spring.springboot_modulo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;

/**
 * Servicio de lógica de negocio para la entidad Calificacion.
 * Administra el ciclo de vida de las calificaciones evaluadas por la IA.
 * 
 * Las anotaciones @Service y @Transactional permiten que Spring gestione
 * automáticamente las transacciones y la inyección de dependencias.
 */
@Service
@Transactional
public class CalificacionService {
    private final CalificacionRepository repo;

    /**
     * Constructor para inyectar el repositorio.
     * @param repo Repositorio de Calificacion (inyectado por Spring)
     */
    public CalificacionService(CalificacionRepository repo) {
        this.repo = repo;
    }

    /**
     * Crea y persiste una nueva calificación en la base de datos.
     * @param c Objeto Calificacion a guardar
     * @return Calificacion creada (con ID autogenerado)
     */
    public Calificacion create(Calificacion c) {
        return repo.save(c);
    }

    /**
     * Devuelve la lista de todas las calificaciones registradas.
     * @return lista de Calificacion
     */
    public List<Calificacion> findAll() {
        return repo.findAll();
    }

    /**
     * Busca una calificación por su ID.
     * @param id ID de la calificación
     * @return Optional con la calificación si existe, vacío si no
     */
    public Optional<Calificacion> findById(Long id) {
        return repo.findById(id);
    }

    /**
     * Actualiza una calificación existente (por ID).
     * @param id ID de la calificación a actualizar
     * @param c Objeto Calificacion con los nuevos datos
     * @return Calificacion actualizada
     */
    public Calificacion update(Long id, Calificacion c) {
        c.setId(id); // Asegura que se actualice la calificación correcta
        return repo.save(c);
    }

    /**
     * Elimina una calificación por su ID.
     * @param id ID de la calificación a eliminar
     */
    public void delete(Long id) {
        repo.deleteById(id);
    }
}
