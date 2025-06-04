package com.informaticonfing.spring.springboot_modulo.dto;

public class ParametrosIdealesResponseDTO {
    private Long id;
    private Double claridadIdeal;
    private Double velocidadIdeal;
    private Double pausasIdeales;
    private String otrosParametros;

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
