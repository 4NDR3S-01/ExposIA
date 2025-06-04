package com.informaticonfing.spring.springboot_modulo.dto;

import java.time.LocalDateTime;

public class FeedbackCalificacionRequestDTO {
    private Long calificacionId;
    private String observacion;
    private LocalDateTime fecha;
    private String autor;

    public Long getCalificacionId() { return calificacionId; }
    public void setCalificacionId(Long calificacionId) { this.calificacionId = calificacionId; }

    public String getObservacion() { return observacion; }
    public void setObservacion(String observacion) { this.observacion = observacion; }

    public LocalDateTime getFecha() { return fecha; }
    public void setFecha(LocalDateTime fecha) { this.fecha = fecha; }

    public String getAutor() { return autor; }
    public void setAutor(String autor) { this.autor = autor; }
}
