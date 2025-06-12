package com.informaticonfing.spring.springboot_modulo.mapper;

import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.ParametrosIdealesResponseDTO;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;

public class ParametrosIdealesMapper {

    public static ParametrosIdeales toEntity(ParametrosIdealesRequestDTO dto) {
        ParametrosIdeales p = new ParametrosIdeales();
        p.setClaridadIdeal(dto.getClaridadIdeal());
        p.setVelocidadIdeal(dto.getVelocidadIdeal());
        p.setPausasIdeales(dto.getPausasIdeales());
        p.setOtrosParametros(dto.getOtrosParametros());
        return p;
    }

    public static ParametrosIdealesResponseDTO toDTO(ParametrosIdeales p) {
        ParametrosIdealesResponseDTO dto = new ParametrosIdealesResponseDTO();
        dto.setId(p.getId());
        dto.setClaridadIdeal(p.getClaridadIdeal());
        dto.setVelocidadIdeal(p.getVelocidadIdeal());
        dto.setPausasIdeales(p.getPausasIdeales());
        dto.setOtrosParametros(p.getOtrosParametros());
        return dto;
    }
}
