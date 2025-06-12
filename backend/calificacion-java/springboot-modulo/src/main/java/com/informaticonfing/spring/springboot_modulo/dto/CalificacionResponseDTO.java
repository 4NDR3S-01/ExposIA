package com.informaticonfing.spring.springboot_modulo.dto;

public class CalificacionResponseDTO {
    private Long id;
    private Long grabacionId;
    private Long usuarioId;
    private Double puntajeGlobal;
    private String observacionGlobal;
    private String tipoCalificacion;
    private Long parametrosIdealesId;
    private java.util.List<DetalleCalificacionResponseDTO> detalles;

    // Getters y Setters
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

    public Long getParametrosIdealesId() { return parametrosIdealesId; }
    public void setParametrosIdealesId(Long parametrosIdealesId) { this.parametrosIdealesId = parametrosIdealesId; }

    public java.util.List<DetalleCalificacionResponseDTO> getDetalles() { return detalles; }
    public void setDetalles(java.util.List<DetalleCalificacionResponseDTO> detalles) { this.detalles = detalles; }
}
