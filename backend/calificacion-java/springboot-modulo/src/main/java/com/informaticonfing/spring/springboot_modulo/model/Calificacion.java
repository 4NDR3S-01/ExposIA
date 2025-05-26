// src/main/java/com/informaticonfing/spring/springboot_modulo/model/Calificacion.java
package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;
import java.util.List;

/**
 * Entidad que representa una calificación general asignada a una grabación
 * evaluada por la IA, con puntaje, observaciones, y referencia a los detalles
 * por criterio y a los parámetros ideales usados.
 */
@Entity
@Table(name = "calificaciones")
public class Calificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Puntaje global asignado a la grabación */
    private double puntaje;

    /** Observaciones generadas por la IA (puede ser feedback textual) */
    private String observacion;

    /** Relación uno-a-uno con la grabación evaluada */
    @OneToOne
    @JoinColumn(name = "grabacion_id")
    private Grabacion grabacion;

    /** Parámetros ideales que fueron usados para comparar la grabación */
    @ManyToOne
    @JoinColumn(name = "parametros_id")
    private ParametrosIdeales parametrosIdeales;

    /** Detalles de calificación por cada criterio (uno a muchos) */
    @OneToMany(mappedBy = "calificacion", cascade = CascadeType.ALL)
    private List<DetalleCalificacion> detalles;

    public Calificacion() { }

    public Calificacion(double puntaje, String observacion, Grabacion grabacion, ParametrosIdeales parametrosIdeales) {
        this.puntaje = puntaje;
        this.observacion = observacion;
        this.grabacion = grabacion;
        this.parametrosIdeales = parametrosIdeales;
    }

    // --- Getters y Setters ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public double getPuntaje() { return puntaje; }
    public void setPuntaje(double puntaje) { this.puntaje = puntaje; }

    public String getObservacion() { return observacion; }
    public void setObservacion(String observacion) { this.observacion = observacion; }

    public Grabacion getGrabacion() { return grabacion; }
    public void setGrabacion(Grabacion grabacion) { this.grabacion = grabacion; }

    public ParametrosIdeales getParametrosIdeales() { return parametrosIdeales; }
    public void setParametrosIdeales(ParametrosIdeales parametrosIdeales) { this.parametrosIdeales = parametrosIdeales; }

    public List<DetalleCalificacion> getDetalles() { return detalles; }
    public void setDetalles(List<DetalleCalificacion> detalles) { this.detalles = detalles; }
}
