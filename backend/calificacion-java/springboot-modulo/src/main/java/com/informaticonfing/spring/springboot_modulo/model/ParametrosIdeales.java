// src/main/java/com/informaticonfing/spring/springboot_modulo/model/ParametrosIdeales.java
package com.informaticonfing.spring.springboot_modulo.model;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import org.springframework.data.jpa.repository.JpaRepository;

import jakarta.persistence.*;

@Entity
@Table(name = "parametros_ideales")
public class ParametrosIdeales {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private double claridadIdeal;
    private double velocidadIdeal;
    private int pausasIdeales;

    public ParametrosIdeales() { }

    public ParametrosIdeales(double claridadIdeal, double velocidadIdeal, int pausasIdeales) {
        this.claridadIdeal = claridadIdeal;
        this.velocidadIdeal = velocidadIdeal;
        this.pausasIdeales = pausasIdeales;
    }

    public Long getId() {
        return id;
    }
    // <-- Agregamos este setter
    public void setId(Long id) {
        this.id = id;
    }

    // … resto de getters y setters …
}
