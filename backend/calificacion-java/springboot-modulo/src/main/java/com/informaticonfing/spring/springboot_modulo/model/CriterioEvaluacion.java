package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;
import java.util.List;

/**
 * Entidad que define un criterio específico para evaluar una grabación
 * (por ejemplo: "Claridad", "Entonación", etc.).
 */
@Entity
@Table(name = "criterios_evaluacion")
public class CriterioEvaluacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Nombre corto del criterio (ej: "Claridad") */
    private String nombre;

    /** Descripción del criterio */
    private String descripcion;

    /** Detalles de calificación asociados a este criterio */
    @OneToMany(mappedBy = "criterioEvaluacion")
    private List<DetalleCalificacion> detalles;

    public CriterioEvaluacion() { }

    public CriterioEvaluacion(String nombre, String descripcion) {
        this.nombre = nombre;
        this.descripcion = descripcion;
    }

    // --- Getters y Setters ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }

    public List<DetalleCalificacion> getDetalles() { return detalles; }
    public void setDetalles(List<DetalleCalificacion> detalles) { this.detalles = detalles; }
}
