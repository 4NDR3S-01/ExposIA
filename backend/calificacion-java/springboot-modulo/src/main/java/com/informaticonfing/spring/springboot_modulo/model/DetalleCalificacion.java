package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "detalle_calificacion")
public class DetalleCalificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "calificacion_id")
    private Calificacion calificacion;

    @ManyToOne
    @JoinColumn(name = "criterio_id")
    private CriterioEvaluacion criterioEvaluacion;

    @Column(name = "slide_id")
    private Long slideId;

    private Integer puntaje;

    private String comentario;

    @Column(name = "fragmento_audio_id")
    private Long fragmentoAudioId;

    public DetalleCalificacion() {}

    public DetalleCalificacion(Long id, Calificacion calificacion, CriterioEvaluacion criterioEvaluacion,
                               Long slideId, Integer puntaje, String comentario, Long fragmentoAudioId) {
        this.id = id;
        this.calificacion = calificacion;
        this.criterioEvaluacion = criterioEvaluacion;
        this.slideId = slideId;
        this.puntaje = puntaje;
        this.comentario = comentario;
        this.fragmentoAudioId = fragmentoAudioId;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Calificacion getCalificacion() { return calificacion; }
    public void setCalificacion(Calificacion calificacion) { this.calificacion = calificacion; }

    public CriterioEvaluacion getCriterioEvaluacion() { return criterioEvaluacion; }
    public void setCriterioEvaluacion(CriterioEvaluacion criterioEvaluacion) { this.criterioEvaluacion = criterioEvaluacion; }

    public Long getSlideId() { return slideId; }
    public void setSlideId(Long slideId) { this.slideId = slideId; }

    public Integer getPuntaje() { return puntaje; }
    public void setPuntaje(Integer puntaje) { this.puntaje = puntaje; }

    public String getComentario() { return comentario; }
    public void setComentario(String comentario) { this.comentario = comentario; }

    public Long getFragmentoAudioId() { return fragmentoAudioId; }
    public void setFragmentoAudioId(Long fragmentoAudioId) { this.fragmentoAudioId = fragmentoAudioId; }
}
