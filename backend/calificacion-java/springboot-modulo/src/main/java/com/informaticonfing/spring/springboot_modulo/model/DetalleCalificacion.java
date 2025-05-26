package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;

/**
 * Entidad que representa el puntaje asignado a una grabación según
 * un criterio de evaluación específico.
 */
@Entity
@Table(name = "detalle_calificacion")
public class DetalleCalificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Puntaje asignado en este detalle */
    private double puntaje;

    /** Calificación global a la que pertenece este detalle */
    @ManyToOne
    @JoinColumn(name = "calificacion_id")
    private Calificacion calificacion;

    /** Criterio de evaluación asociado a este detalle */
    @ManyToOne
    @JoinColumn(name = "criterio_id")
    private CriterioEvaluacion criterioEvaluacion;

    public DetalleCalificacion() { }

    public DetalleCalificacion(double puntaje, Calificacion calificacion, CriterioEvaluacion criterioEvaluacion) {
        this.puntaje = puntaje;
        this.calificacion = calificacion;
        this.criterioEvaluacion = criterioEvaluacion;
    }

    // --- Getters y Setters ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public double getPuntaje() { return puntaje; }
    public void setPuntaje(double puntaje) { this.puntaje = puntaje; }

    public Calificacion getCalificacion() { return calificacion; }
    public void setCalificacion(Calificacion calificacion) { this.calificacion = calificacion; }

    public CriterioEvaluacion getCriterioEvaluacion() { return criterioEvaluacion; }
    public void setCriterioEvaluacion(CriterioEvaluacion criterioEvaluacion) { this.criterioEvaluacion = criterioEvaluacion; }
}
