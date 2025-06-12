package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.CalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.mapper.CalificacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.model.CriterioEvaluacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;
import com.informaticonfing.spring.springboot_modulo.repository.DetalleCalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.FeedbackCalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.dto.AiCalificacionDTO;
import com.informaticonfing.spring.springboot_modulo.dto.AiDetalleDTO;
import com.informaticonfing.spring.springboot_modulo.dto.AiFeedbackDTO;
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
    private DetalleCalificacionRepository detalleRepo;
    private FeedbackCalificacionRepository feedbackRepo;
    private CalificacionService service;

    @BeforeEach
    void setUp() {
        repository = mock(CalificacionRepository.class);
        parametrosRepo = mock(ParametrosIdealesRepository.class);
        detalleRepo = mock(DetalleCalificacionRepository.class);
        feedbackRepo = mock(FeedbackCalificacionRepository.class);
        service = new CalificacionService(repository, parametrosRepo, detalleRepo, feedbackRepo);
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

    @Test
    void testAplicarCalificacionAI() {
        // Calificación manual existente
        Calificacion calificacion = new Calificacion();
        calificacion.setId(1L);
        calificacion.setPuntajeGlobal(8.0);

        DetalleCalificacion detalle = new DetalleCalificacion();
        detalle.setPuntaje(8);
        CriterioEvaluacion criterio = new CriterioEvaluacion();
        criterio.setId(5L);
        detalle.setCriterioEvaluacion(criterio);

        when(repository.findById(1L)).thenReturn(Optional.of(calificacion));
        when(detalleRepo.findByCalificacionId(1L)).thenReturn(List.of(detalle));
        when(detalleRepo.save(any(DetalleCalificacion.class))).thenReturn(detalle);
        when(repository.save(any(Calificacion.class))).thenAnswer(i -> i.getArgument(0));
        when(feedbackRepo.save(any())).thenAnswer(i -> i.getArgument(0));

        AiDetalleDTO aiDetalle = new AiDetalleDTO();
        aiDetalle.setCriterioId(5L);
        aiDetalle.setPuntaje(6);
        aiDetalle.setComentario("en la slide 4 tartamudeaste");

        AiFeedbackDTO fb = new AiFeedbackDTO();
        fb.setObservacion("Buen trabajo");
        fb.setAutor("IA");

        AiCalificacionDTO dto = new AiCalificacionDTO();
        dto.setCalificacionId(1L);
        dto.setPuntajeGlobalAi(7.0);
        dto.setDetalles(List.of(aiDetalle));
        dto.setObservacionGlobalAi("Observación global IA");
        dto.setFeedbacks(List.of(fb));

        CalificacionResponseDTO result = service.aplicarCalificacionAI(dto);

        assertNotNull(result);
        assertEquals(7.5, result.getPuntajeGlobal());
        assertNotNull(result.getDetalles());
        assertEquals(1, result.getDetalles().size());
        assertEquals(5L, result.getDetalles().get(0).getCriterioId());
        assertEquals(7, result.getDetalles().get(0).getPuntaje());
        verify(detalleRepo, times(1)).save(any(DetalleCalificacion.class));
        verify(feedbackRepo, times(1)).save(any());
        assertEquals("Observación global IA", calificacion.getObservacionGlobal());
        assertEquals("en la slide 4 tartamudeaste", detalle.getComentario());
    }
}
