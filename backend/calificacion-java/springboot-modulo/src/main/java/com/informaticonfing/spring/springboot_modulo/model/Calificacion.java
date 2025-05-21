// src/main/java/com/informaticonfing/spring/springboot_modulo/model/Calificacion.java
package com.informaticonfing.spring.springboot_modulo.model;
import org.springframework.data.jpa.repository.JpaRepository;

import jakarta.persistence.*;

@Entity
@Table(name = "calificaciones")
public class Calificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private double puntaje;
    private String observacion;
    private String vinculoGrabacion;

    @ManyToOne
    @JoinColumn(name = "parametros_id")
    private ParametrosIdeales parametrosIdeales;

    public Calificacion() { }

    public Calificacion(double puntaje,
                        String observacion,
                        String vinculoGrabacion,
                        ParametrosIdeales parametrosIdeales) {
        this.puntaje = puntaje;
        this.observacion = observacion;
        this.vinculoGrabacion = vinculoGrabacion;
        this.parametrosIdeales = parametrosIdeales;
    }

    public Long getId() {
        return id;
    }
    // <-- Y también aquí:
    public void setId(Long id) {
        this.id = id;
    }

    // … resto de getters y setters …
}
