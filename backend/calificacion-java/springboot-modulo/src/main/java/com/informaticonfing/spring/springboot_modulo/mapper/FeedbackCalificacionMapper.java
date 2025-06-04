package com.informaticonfing.spring.springboot_modulo.mapper;

import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.FeedbackCalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.FeedbackCalificacion;

public class FeedbackCalificacionMapper {

    public static FeedbackCalificacion toEntity(FeedbackCalificacionRequestDTO dto, Calificacion calificacion) {
        FeedbackCalificacion f = new FeedbackCalificacion();
        f.setCalificacion(calificacion);
        f.setObservacion(dto.getObservacion());
        f.setFecha(dto.getFecha());
        f.setAutor(dto.getAutor());
        return f;
    }

    public static FeedbackCalificacionResponseDTO toDTO(FeedbackCalificacion f) {
        FeedbackCalificacionResponseDTO dto = new FeedbackCalificacionResponseDTO();
        dto.setId(f.getId());
        if (f.getCalificacion() != null) dto.setCalificacionId(f.getCalificacion().getId());
        dto.setObservacion(f.getObservacion());
        dto.setFecha(f.getFecha());
        dto.setAutor(f.getAutor());
        return dto;
    }
}
