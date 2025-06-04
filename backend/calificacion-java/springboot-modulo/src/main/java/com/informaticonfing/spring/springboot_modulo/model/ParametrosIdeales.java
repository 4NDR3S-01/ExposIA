package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "parametros_ideales")
public class ParametrosIdeales {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "claridad_ideal")
    private Double claridadIdeal;

    @Column(name = "velocidad_ideal")
    private Double velocidadIdeal;

    @Column(name = "pausas_ideales")
    private Double pausasIdeales;

    @Column(name = "otros_parametros", columnDefinition = "TEXT")
    private String otrosParametros;

    public ParametrosIdeales() {}

    public ParametrosIdeales(Long id, Double claridadIdeal, Double velocidadIdeal, Double pausasIdeales, String otrosParametros) {
        this.id = id;
        this.claridadIdeal = claridadIdeal;
        this.velocidadIdeal = velocidadIdeal;
        this.pausasIdeales = pausasIdeales;
        this.otrosParametros = otrosParametros;
    }

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
