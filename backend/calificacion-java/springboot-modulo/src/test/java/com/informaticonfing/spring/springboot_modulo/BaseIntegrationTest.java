package com.informaticonfing.spring.springboot_modulo;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Clase base para todos los tests de integración.
 * Incluye configuración común y utilidades.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test") // Siempre usa el perfil test
public abstract class BaseIntegrationTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ObjectMapper objectMapper;

    // Puedes agregar métodos utilitarios aquí, por ejemplo:
    // protected <T> T postAndReturn(String url, Object dto, Class<T> responseClass) { ... }
}
