package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Entidad principal para la evaluación/calificación.
 */
@Entity
@Table(name = "calificaciones")
public class Calificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Relación con grabaciones (solo almacena el ID por eficiencia)
    @Column(name = "grabacion_id")
    private Long grabacionId;

    // Relación con usuarios (puede ser null si es IA)
    @Column(name = "usuario_id")
    private Long usuarioId;

    @Column(name = "puntaje_global")
    private Double puntajeGlobal;

    @Column(name = "observacion_global")
    private String observacionGlobal;

    @Column(name = "tipo_calificacion")
    private String tipoCalificacion; // ej: "ia", "manual", "final"

    @Column(name = "fecha")
    private LocalDateTime fecha;

    // Relación con parámetros ideales
    @ManyToOne
    @JoinColumn(name = "parametros_id")
    private ParametrosIdeales parametrosIdeales;

    public Calificacion() {}

    public Calificacion(Long id, Long grabacionId, Long usuarioId, Double puntajeGlobal, String observacionGlobal,
                        String tipoCalificacion, LocalDateTime fecha, ParametrosIdeales parametrosIdeales) {
        this.id = id;
        this.grabacionId = grabacionId;
        this.usuarioId = usuarioId;
        this.puntajeGlobal = puntajeGlobal;
        this.observacionGlobal = observacionGlobal;
        this.tipoCalificacion = tipoCalificacion;
        this.fecha = fecha;
        this.parametrosIdeales = parametrosIdeales;
    }

    // Getters y setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getGrabacionId() { return grabacionId; }
    public void setGrabacionId(Long grabacionId) { this.grabacionId = grabacionId; }

    public Long getUsuarioId() { return usuarioId; }
    public void setUsuarioId(Long usuarioId) { this.usuarioId = usuarioId; }

    public Double getPuntajeGlobal() { return puntajeGlobal; }
    public void setPuntajeGlobal(Double puntajeGlobal) { this.puntajeGlobal = puntajeGlobal; }

    public String getObservacionGlobal() { return observacionGlobal; }
    public void setObservacionGlobal(String observacionGlobal) { this.observacionGlobal = observacionGlobal; }

    public String getTipoCalificacion() { return tipoCalificacion; }
    public void setTipoCalificacion(String tipoCalificacion) { this.tipoCalificacion = tipoCalificacion; }

    public LocalDateTime getFecha() { return fecha; }
    public void setFecha(LocalDateTime fecha) { this.fecha = fecha; }

    public ParametrosIdeales getParametrosIdeales() { return parametrosIdeales; }
    public void setParametrosIdeales(ParametrosIdeales parametrosIdeales) { this.parametrosIdeales = parametrosIdeales; }
}
