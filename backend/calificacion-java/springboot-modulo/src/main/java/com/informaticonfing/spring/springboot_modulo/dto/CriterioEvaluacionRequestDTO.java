package com.informaticonfing.spring.springboot_modulo.dto;

public class CriterioEvaluacionRequestDTO {
    private String nombre;
    private String descripcion;
    private Double peso;

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }

    public Double getPeso() { return peso; }
    public void setPeso(Double peso) { this.peso = peso; }
}
