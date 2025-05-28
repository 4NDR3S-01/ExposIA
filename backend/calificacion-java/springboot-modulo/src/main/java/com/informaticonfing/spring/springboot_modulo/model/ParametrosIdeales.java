package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;

/**
 * Entidad para los parámetros ideales usados como referencia en la evaluación.
 */
@Entity
@Table(name = "parametros_ideales")
public class ParametrosIdeales {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Double claridadIdeal;
    private Double velocidadIdeal;
    private Double pausasIdeales;

    @Column(columnDefinition = "TEXT")
    private String otrosParametros; // JSON como texto

    // Constructor vacío
    public ParametrosIdeales() {}

    // Constructor completo
    public ParametrosIdeales(Long id, Double claridadIdeal, Double velocidadIdeal, Double pausasIdeales, String otrosParametros) {
        this.id = id;
        this.claridadIdeal = claridadIdeal;
        this.velocidadIdeal = velocidadIdeal;
        this.pausasIdeales = pausasIdeales;
        this.otrosParametros = otrosParametros;
    }

    // Getters y setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Double getClaridadIdeal() { return claridadIdeal; }
    public void setClaridadIdeal(Double claridadIdeal) { this.claridadIdeal = claridadIdeal; }

    public Double getVelocidadIdeal() { return velocidadIdeal; }
    public void setVelocidadIdeal(Double velocidadIdeal) { this.velocidadIdeal = velocidadIdeal; }

    public Double getPausasIdeales() { return pausasIdeales; }
    public void setPausasIdeales(Double pausasIdeales) { this.pausasIdeales = pausasIdeales; }

    public String getOtrosParametros() { return otrosParametros; }
    public void setOtrosParametros(String otrosParametros) { this.otrosParametros = otrosParametros; }
}
