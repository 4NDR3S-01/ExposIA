package com.informaticonfing.spring.springboot_modulo.model;

import jakarta.persistence.*;
import java.util.List;

/**
 * Entidad que representa la evidencia (archivo o recurso multimedia)
 * evaluada por la IA.
 */
@Entity
@Table(name = "grabaciones")
public class Grabacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** URL o path donde se encuentra almacenada la grabación */
    private String url;

    /** Nombre del archivo original */
    private String nombreArchivo;

    /** Relación uno-a-uno con la calificación principal asociada */
    @OneToOne(mappedBy = "grabacion", cascade = CascadeType.ALL)
    private Calificacion calificacion;

    public Grabacion() { }

    public Grabacion(String url, String nombreArchivo) {
        this.url = url;
        this.nombreArchivo = nombreArchivo;
    }

    // --- Getters y Setters ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }

    public String getNombreArchivo() { return nombreArchivo; }
    public void setNombreArchivo(String nombreArchivo) { this.nombreArchivo = nombreArchivo; }

    public Calificacion getCalificacion() { return calificacion; }
    public void setCalificacion(Calificacion calificacion) { this.calificacion = calificacion; }
}
