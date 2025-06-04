package com.informaticonfing.spring.springboot_modulo;

import org.junit.jupiter.api.Test;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.boot.test.context.SpringBootTest;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

// ACTIVA el perfil "test" que usa H2 y datos de test
@ActiveProfiles("test")
@SpringBootTest
class SeguridadTest extends BaseIntegrationTest {

    // Endpoint público: ajusta según tu API
    @Test
    void parametrosIdealesDebeSerPublico() throws Exception {
        mockMvc.perform(get("/api/parametros-ideales"))
               .andExpect(status().isOk());
    }

    @Test
    void calificacionesDebeEstarProtegido() throws Exception {
        mockMvc.perform(get("/api/calificaciones"))
               .andExpect(status().isUnauthorized());
    }

    @Test
    void calificacionesConAuthBasica() throws Exception {
        // Usuario de pruebas definido en application-test.properties
        mockMvc.perform(get("/api/calificaciones")
                    .with(httpBasic("admin", "admin123")))
                .andExpect(status().isOk()); // O isForbidden() si hay roles
    }

    @Test
    void endpointNoExisteDevuelve404() throws Exception {
        mockMvc.perform(get("/api/noexiste")
                .with(httpBasic("admin", "admin123")))
               .andExpect(status().isNotFound());
    }

    @Test
    void criteriosDebeEstarProtegido() throws Exception {
        mockMvc.perform(get("/api/criterios"))
               .andExpect(status().isUnauthorized());
    }
}
