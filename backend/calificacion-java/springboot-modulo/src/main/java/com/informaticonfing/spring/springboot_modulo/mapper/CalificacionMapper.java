package com.informaticonfing.spring.springboot_modulo.mapper;

import com.informaticonfing.spring.springboot_modulo.dto.*;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;

public class CalificacionMapper {

    public static Calificacion toEntity(CalificacionRequestDTO dto, ParametrosIdeales parametrosIdeales) {
        Calificacion c = new Calificacion();
        c.setGrabacionId(dto.getGrabacionId());
        c.setUsuarioId(dto.getUsuarioId());
        c.setPuntajeGlobal(dto.getPuntajeGlobal());
        c.setObservacionGlobal(dto.getObservacionGlobal());
        c.setTipoCalificacion(dto.getTipoCalificacion());
        c.setParametrosIdeales(parametrosIdeales);
        return c;
    }

    public static CalificacionResponseDTO toDTO(Calificacion c) {
        CalificacionResponseDTO dto = new CalificacionResponseDTO();
        dto.setId(c.getId());
        dto.setGrabacionId(c.getGrabacionId());
        dto.setUsuarioId(c.getUsuarioId());
        dto.setPuntajeGlobal(c.getPuntajeGlobal());
        dto.setObservacionGlobal(c.getObservacionGlobal());
        dto.setTipoCalificacion(c.getTipoCalificacion());
        if (c.getParametrosIdeales() != null) {
            dto.setParametrosIdealesId(c.getParametrosIdeales().getId());
        }
        return dto;
    }
}
