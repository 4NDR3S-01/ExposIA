package com.informaticonfing.spring.springboot_modulo.dto;

public class DetalleCalificacionRequestDTO {
    private Long calificacionId;
    private Long criterioId;
    private Long slideId;
    private Integer puntaje;
    private String comentario;
    private Long fragmentoAudioId;

    public Long getCalificacionId() { return calificacionId; }
    public void setCalificacionId(Long calificacionId) { this.calificacionId = calificacionId; }

    public Long getCriterioId() { return criterioId; }
    public void setCriterioId(Long criterioId) { this.criterioId = criterioId; }

    public Long getSlideId() { return slideId; }
    public void setSlideId(Long slideId) { this.slideId = slideId; }

    public Integer getPuntaje() { return puntaje; }
    public void setPuntaje(Integer puntaje) { this.puntaje = puntaje; }

    public String getComentario() { return comentario; }
    public void setComentario(String comentario) { this.comentario = comentario; }

    public Long getFragmentoAudioId() { return fragmentoAudioId; }
    public void setFragmentoAudioId(Long fragmentoAudioId) { this.fragmentoAudioId = fragmentoAudioId; }
}
