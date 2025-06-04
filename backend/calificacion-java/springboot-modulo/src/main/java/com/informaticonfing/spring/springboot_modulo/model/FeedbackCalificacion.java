package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "feedback_calificacion")
public class FeedbackCalificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "calificacion_id")
    private Calificacion calificacion;

    private String observacion;
    private LocalDateTime fecha;
    private String autor;

    public FeedbackCalificacion() {}

    public FeedbackCalificacion(Long id, Calificacion calificacion, String observacion, LocalDateTime fecha, String autor) {
        this.id = id;
        this.calificacion = calificacion;
        this.observacion = observacion;
        this.fecha = fecha;
        this.autor = autor;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Calificacion getCalificacion() { return calificacion; }
    public void setCalificacion(Calificacion calificacion) { this.calificacion = calificacion; }

    public String getObservacion() { return observacion; }
    public void setObservacion(String observacion) { this.observacion = observacion; }

    public LocalDateTime getFecha() { return fecha; }
    public void setFecha(LocalDateTime fecha) { this.fecha = fecha; }

    public String getAutor() { return autor; }
    public void setAutor(String autor) { this.autor = autor; }
}
