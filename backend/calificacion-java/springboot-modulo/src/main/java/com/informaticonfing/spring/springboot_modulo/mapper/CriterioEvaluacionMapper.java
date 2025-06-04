package com.informaticonfing.spring.springboot_modulo.mapper;

import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CriterioEvaluacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;

public class CriterioEvaluacionMapper {
    public static CriterioEvaluacion toEntity(CriterioEvaluacionRequestDTO dto) {
        return new CriterioEvaluacion(null, dto.getNombre(), dto.getDescripcion(), dto.getPeso());
    }
    public static CriterioEvaluacionResponseDTO toDTO(CriterioEvaluacion c) {
        CriterioEvaluacionResponseDTO dto = new CriterioEvaluacionResponseDTO();
        dto.setId(c.getId());
        dto.setNombre(c.getNombre());
        dto.setDescripcion(c.getDescripcion());
        dto.setPeso(c.getPeso());
        return dto;
    }
}
