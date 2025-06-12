package com.informaticonfing.spring.springboot_modulo.dto;

import java.util.List;

import com.informaticonfing.spring.springboot_modulo.dto.AiFeedbackDTO;


/**
 * Estructura recibida desde la IA con la evaluación completa.
 */
public class AiCalificacionDTO {
    private Long calificacionId;
    private Double puntajeGlobalAi;
    private String observacionGlobalAi;
    private List<AiDetalleDTO> detalles;
    private List<AiFeedbackDTO> feedbacks;

    public Long getCalificacionId() { return calificacionId; }
    public void setCalificacionId(Long calificacionId) { this.calificacionId = calificacionId; }

    public Double getPuntajeGlobalAi() { return puntajeGlobalAi; }
    public void setPuntajeGlobalAi(Double puntajeGlobalAi) { this.puntajeGlobalAi = puntajeGlobalAi; }

    public String getObservacionGlobalAi() { return observacionGlobalAi; }
    public void setObservacionGlobalAi(String observacionGlobalAi) { this.observacionGlobalAi = observacionGlobalAi; }

    public List<AiDetalleDTO> getDetalles() { return detalles; }
    public void setDetalles(List<AiDetalleDTO> detalles) { this.detalles = detalles; }

    public List<AiFeedbackDTO> getFeedbacks() { return feedbacks; }
    public void setFeedbacks(List<AiFeedbackDTO> feedbacks) { this.feedbacks = feedbacks; }
}
