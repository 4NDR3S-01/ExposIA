package com.informaticonfing.spring.springboot_modulo.dto;

/**
 * Representa el puntaje otorgado por la IA para un criterio.
 */
public class AiDetalleDTO {
    private Long criterioId;
    private Integer puntaje;
    private String comentario;

    public Long getCriterioId() { return criterioId; }
    public void setCriterioId(Long criterioId) { this.criterioId = criterioId; }

    public Integer getPuntaje() { return puntaje; }
    public void setPuntaje(Integer puntaje) { this.puntaje = puntaje; }

    public String getComentario() { return comentario; }
    public void setComentario(String comentario) { this.comentario = comentario; }

}
