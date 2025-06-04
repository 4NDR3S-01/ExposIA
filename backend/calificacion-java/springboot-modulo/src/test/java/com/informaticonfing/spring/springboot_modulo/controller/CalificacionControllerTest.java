package com.informaticonfing.spring.springboot_modulo.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.informaticonfing.spring.springboot_modulo.dto.CalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CalificacionResponseDTO;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.context.ActiveProfiles;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc(addFilters = false)
@ActiveProfiles("test")
class CalificacionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void testCreateAndGetCalificacion() throws Exception {
        // Asegúrate de tener algún ParametrosIdealesId válido (por ejemplo, 1)
        Long parametrosIdealesId = 1L;

        CalificacionRequestDTO requestDTO = new CalificacionRequestDTO();
        requestDTO.setGrabacionId(1L);
        requestDTO.setUsuarioId(2L); // Si hay FK, asegúrate de que ese usuario exista, o ponlo null si es permitido
        requestDTO.setPuntajeGlobal(8.5);
        requestDTO.setObservacionGlobal("Muy buena exposición");
        requestDTO.setTipoCalificacion("manual");
        requestDTO.setParametrosIdealesId(parametrosIdealesId);

        // Crear
        String response = mockMvc.perform(post("/api/calificaciones")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(requestDTO)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        CalificacionResponseDTO created = objectMapper.readValue(response, CalificacionResponseDTO.class);

        assertThat(created.getObservacionGlobal()).isEqualTo("Muy buena exposición");
        assertThat(created.getPuntajeGlobal()).isEqualTo(8.5);

        // Obtener por ID
        mockMvc.perform(get("/api/calificaciones/" + created.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(created.getId()));
    }
}
