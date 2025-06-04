package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;

/**
 * Entidad para los detalles individuales de la calificación.
 */
@Entity
@Table(name = "detalle_calificacion")
public class DetalleCalificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Pertenece a una calificación
    @ManyToOne
    @JoinColumn(name = "calificacion_id")
    private Calificacion calificacion;

    // Relación con criterio de evaluación
    @ManyToOne
    @JoinColumn(name = "criterio_id")
    private CriterioEvaluacion criterio;

    // Slide relacionado
    @Column(name = "slide_ide")
    private Long slideId;

    private Integer puntaje;

    private String comentario;

    // Puede ser null
    @Column(name = "fragmento_audio_id")
    private Long fragmentoAudioId;

    public DetalleCalificacion() {}

    public DetalleCalificacion(Long id, Calificacion calificacion, CriterioEvaluacion criterio,
                               Long slideId, Integer puntaje, String comentario, Long fragmentoAudioId) {
        this.id = id;
        this.calificacion = calificacion;
        this.criterio = criterio;
        this.slideId = slideId;
        this.puntaje = puntaje;
        this.comentario = comentario;
        this.fragmentoAudioId = fragmentoAudioId;
    }

    // Getters y setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Calificacion getCalificacion() { return calificacion; }
    public void setCalificacion(Calificacion calificacion) { this.calificacion = calificacion; }

    public CriterioEvaluacion getCriterio() { return criterio; }
    public void setCriterio(CriterioEvaluacion criterio) { this.criterio = criterio; }

    public Long getSlideId() { return slideId; }
    public void setSlideId(Long slideId) { this.slideId = slideId; }

    public Integer getPuntaje() { return puntaje; }
    public void setPuntaje(Integer puntaje) { this.puntaje = puntaje; }

    public String getComentario() { return comentario; }
    public void setComentario(String comentario) { this.comentario = comentario; }

    public Long getFragmentoAudioId() { return fragmentoAudioId; }
    public void setFragmentoAudioId(Long fragmentoAudioId) { this.fragmentoAudioId = fragmentoAudioId; }
}
