package com.informaticonfing.spring.springboot_modulo.mapper;

import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.DetalleCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;

public class DetalleCalificacionMapper {

    public static DetalleCalificacion toEntity(DetalleCalificacionRequestDTO dto, Calificacion calificacion, CriterioEvaluacion criterio) {
        DetalleCalificacion d = new DetalleCalificacion();
        d.setCalificacion(calificacion);
        d.setCriterioEvaluacion(criterio);
        d.setSlideId(dto.getSlideId());
        d.setPuntaje(dto.getPuntaje());
        d.setComentario(dto.getComentario());
        d.setFragmentoAudioId(dto.getFragmentoAudioId());
        return d;
    }

    public static DetalleCalificacionResponseDTO toDTO(DetalleCalificacion d) {
        DetalleCalificacionResponseDTO dto = new DetalleCalificacionResponseDTO();
        dto.setId(d.getId());
        if (d.getCalificacion() != null) dto.setCalificacionId(d.getCalificacion().getId());
        if (d.getCriterioEvaluacion() != null) dto.setCriterioId(d.getCriterioEvaluacion().getId());
        dto.setSlideId(d.getSlideId());
        dto.setPuntaje(d.getPuntaje());
        dto.setComentario(d.getComentario());
        dto.setFragmentoAudioId(d.getFragmentoAudioId());
        return dto;
    }
}
