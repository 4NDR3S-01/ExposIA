// src/main/java/com/informaticonfing/spring/springboot_modulo/model/ParametrosIdeales.java
package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;
import java.util.List;

/**
 * Entidad que representa los parámetros ideales contra los cuales se compara
 * la grabación (puede ser claridad, velocidad, pausas ideales, etc.).
 */
@Entity
@Table(name = "parametros_ideales")
public class ParametrosIdeales {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Claridad ideal esperada */
    private double claridadIdeal;

    /** Velocidad ideal esperada */
    private double velocidadIdeal;

    /** Número ideal de pausas */
    private int pausasIdeales;

    /** Lista de calificaciones que usaron estos parámetros */
    @OneToMany(mappedBy = "parametrosIdeales")
    private List<Calificacion> calificaciones;

    public ParametrosIdeales() { }

    public ParametrosIdeales(double claridadIdeal, double velocidadIdeal, int pausasIdeales) {
        this.claridadIdeal = claridadIdeal;
        this.velocidadIdeal = velocidadIdeal;
        this.pausasIdeales = pausasIdeales;
    }

    // --- Getters y Setters ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public double getClaridadIdeal() { return claridadIdeal; }
    public void setClaridadIdeal(double claridadIdeal) { this.claridadIdeal = claridadIdeal; }

    public double getVelocidadIdeal() { return velocidadIdeal; }
    public void setVelocidadIdeal(double velocidadIdeal) { this.velocidadIdeal = velocidadIdeal; }

    public int getPausasIdeales() { return pausasIdeales; }
    public void setPausasIdeales(int pausasIdeales) { this.pausasIdeales = pausasIdeales; }

    public List<Calificacion> getCalificaciones() { return calificaciones; }
    public void setCalificaciones(List<Calificacion> calificaciones) { this.calificaciones = calificaciones; }
}
