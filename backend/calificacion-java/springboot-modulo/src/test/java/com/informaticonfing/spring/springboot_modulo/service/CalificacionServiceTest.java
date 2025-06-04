package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.CalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.CalificacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentMatchers;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class CalificacionServiceTest {

    private CalificacionRepository repository;
    private ParametrosIdealesRepository parametrosRepo;
    private CalificacionService service;

    @BeforeEach
    void setUp() {
        repository = mock(CalificacionRepository.class);
        parametrosRepo = mock(ParametrosIdealesRepository.class);
        service = new CalificacionService(repository, parametrosRepo);
    }

    @Test
    void testFindAll() {
        Calificacion calif1 = new Calificacion();
        calif1.setId(1L);
        Calificacion calif2 = new Calificacion();
        calif2.setId(2L);

        when(repository.findAll()).thenReturn(Arrays.asList(calif1, calif2));

        List<CalificacionResponseDTO> result = service.findAll();
        assertEquals(2, result.size());
        assertEquals(1L, result.get(0).getId());
        assertEquals(2L, result.get(1).getId());
    }

    @Test
    void testFindById() {
        Calificacion calif = new Calificacion();
        calif.setId(10L);
        when(repository.findById(10L)).thenReturn(Optional.of(calif));

        Optional<CalificacionResponseDTO> result = service.findById(10L);
        assertTrue(result.isPresent());
        assertEquals(10L, result.get().getId());
    }

    @Test
    void testCreate() {
        CalificacionRequestDTO dto = new CalificacionRequestDTO();
        dto.setParametrosIdealesId(100L);

        ParametrosIdeales parametros = new ParametrosIdeales();
        parametros.setId(100L);

        Calificacion entity = CalificacionMapper.toEntity(dto, parametros);
        entity.setId(55L);

        when(parametrosRepo.findById(100L)).thenReturn(Optional.of(parametros));
        when(repository.save(ArgumentMatchers.any(Calificacion.class))).thenReturn(entity);

        CalificacionResponseDTO result = service.create(dto);

        assertNotNull(result);
        assertEquals(55L, result.getId());
    }

    @Test
    void testUpdate() {
        CalificacionRequestDTO dto = new CalificacionRequestDTO();
        dto.setParametrosIdealesId(200L);

        ParametrosIdeales parametros = new ParametrosIdeales();
        parametros.setId(200L);

        Calificacion entity = CalificacionMapper.toEntity(dto, parametros);
        entity.setId(88L);

        when(parametrosRepo.findById(200L)).thenReturn(Optional.of(parametros));
        when(repository.save(ArgumentMatchers.any(Calificacion.class))).thenReturn(entity);

        CalificacionResponseDTO result = service.update(88L, dto);

        assertNotNull(result);
        assertEquals(88L, result.getId());
    }

    @Test
    void testDelete() {
        doNothing().when(repository).deleteById(33L);
        service.delete(33L);
        verify(repository, times(1)).deleteById(33L);
    }
}
