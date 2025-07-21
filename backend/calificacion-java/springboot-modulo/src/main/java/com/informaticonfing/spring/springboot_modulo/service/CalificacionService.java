package com.informaticonfing.spring.springboot_modulo.service;

import com.informaticonfing.spring.springboot_modulo.dto.CalificacionRequestDTO;
import com.informaticonfing.spring.springboot_modulo.dto.CalificacionResponseDTO;
import com.informaticonfing.spring.springboot_modulo.dto.AiCalificacionDTO;
import com.informaticonfing.spring.springboot_modulo.dto.AiDetalleDTO;
import com.informaticonfing.spring.springboot_modulo.dto.AiFeedbackDTO;

import com.informaticonfing.spring.springboot_modulo.mapper.CalificacionMapper;
import com.informaticonfing.spring.springboot_modulo.model.Calificacion;
import com.informaticonfing.spring.springboot_modulo.model.FeedbackCalificacion;
import com.informaticonfing.spring.springboot_modulo.model.ParametrosIdeales;
import com.informaticonfing.spring.springboot_modulo.model.DetalleCalificacion;
import com.informaticonfing.spring.springboot_modulo.repository.CalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.ParametrosIdealesRepository;
import com.informaticonfing.spring.springboot_modulo.repository.DetalleCalificacionRepository;
import com.informaticonfing.spring.springboot_modulo.repository.FeedbackCalificacionRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.beans.factory.annotation.Value;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de calificaciones.
 */
@Service
public class CalificacionService {
    private final CalificacionRepository repository;
    private final ParametrosIdealesRepository parametrosRepo;
    private final DetalleCalificacionRepository detalleRepo;
    private final FeedbackCalificacionRepository feedbackRepo;
    private final RestTemplate restTemplate;
    
    @Value("${ws.notification.url:http://localhost:9000}")
    private String wsNotificationUrl;
    
    @Value("${ws.notification.token:dev}")
    private String wsNotificationToken;

    public CalificacionService(
            CalificacionRepository repository,
            ParametrosIdealesRepository parametrosRepo,
            DetalleCalificacionRepository detalleRepo,
            FeedbackCalificacionRepository feedbackRepo,
            RestTemplate restTemplate
    ) {
        this.repository = repository;
        this.parametrosRepo = parametrosRepo;
        this.detalleRepo = detalleRepo;
        this.feedbackRepo = feedbackRepo;
        this.restTemplate = restTemplate;
    }

    /**
     * Obtiene todas las calificaciones.
     * @return lista de CalificacionResponseDTO
     */
    public List<CalificacionResponseDTO> findAll() {
        return repository.findAll()
            .stream()
            .map(CalificacionMapper::toDTO)
            .collect(Collectors.toList());
    }

    /**
     * Busca una calificación por su ID.
     * @param id identificador de la calificación
     * @return CalificacionResponseDTO si existe, vacío si no
     */
    public Optional<CalificacionResponseDTO> findById(Long id) {
        return repository.findById(id)
            .map(CalificacionMapper::toDTO);
    }

    /**
     * Crea una nueva calificación.
     * @param dto datos de la nueva calificación
     * @return la calificación creada
     */
    public CalificacionResponseDTO create(CalificacionRequestDTO dto) {
        ParametrosIdeales parametros = null;
        if (dto.getParametrosIdealesId() != null) {
            parametros = parametrosRepo.findById(dto.getParametrosIdealesId()).orElse(null);
        }
        Calificacion entidad = CalificacionMapper.toEntity(dto, parametros);
        Calificacion saved = repository.save(entidad);
        
        // Enviar notificación
        enviarNotificacion("calificacion.creada", Map.of(
            "id", saved.getId(),
            "grabacionId", saved.getGrabacionId(),
            "usuarioId", saved.getUsuarioId(),
            "puntajeGlobal", saved.getPuntajeGlobal()
        ));
        
        return CalificacionMapper.toDTO(saved);
    }

    /**
     * Actualiza una calificación existente.
     * @param id identificador de la calificación a actualizar
     * @param dto nuevos datos de la calificación
     * @return la calificación actualizada
     */
    public CalificacionResponseDTO update(Long id, CalificacionRequestDTO dto) {
        ParametrosIdeales parametros = null;
        if (dto.getParametrosIdealesId() != null) {
            parametros = parametrosRepo.findById(dto.getParametrosIdealesId()).orElse(null);
        }
        Calificacion entidad = CalificacionMapper.toEntity(dto, parametros);
        entidad.setId(id);
        Calificacion saved = repository.save(entidad);
        return CalificacionMapper.toDTO(saved);
    }

    /**
     * Elimina una calificación por su ID.
     * @param id identificador de la calificación a eliminar
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }

    /**
     * Procesa las calificaciones generadas por IA y actualiza la calificación manual.
     * Combina los puntajes manuales con los de la IA calculando un promedio.
     * @param dto datos provenientes de la IA
     * @return CalificacionResponseDTO actualizado con el puntaje final
     */
    public CalificacionResponseDTO aplicarCalificacionAI(AiCalificacionDTO dto) {
        Calificacion calificacion = repository.findById(dto.getCalificacionId())
                .orElseThrow(() -> new IllegalArgumentException("Calificación no encontrada"));

        // Actualizar detalles promediando con los valores de IA
        List<DetalleCalificacion> detalles = detalleRepo.findByCalificacionId(calificacion.getId());
        for (AiDetalleDTO aiDetalle : dto.getDetalles()) {
            detalles.stream()
                    .filter(d -> d.getCriterioEvaluacion() != null &&
                            d.getCriterioEvaluacion().getId().equals(aiDetalle.getCriterioId()))
                    .findFirst()
                    .ifPresent(d -> {
                        double promedio = (d.getPuntaje() + aiDetalle.getPuntaje()) / 2.0;
                        d.setPuntaje((int) Math.round(promedio));
                        if (aiDetalle.getComentario() != null) {
                            d.setComentario(aiDetalle.getComentario());
                        }
                        detalleRepo.save(d);
                    });
        }

        double finalGlobal = (calificacion.getPuntajeGlobal() + dto.getPuntajeGlobalAi()) / 2.0;
        calificacion.setPuntajeGlobal(finalGlobal);
        if (dto.getObservacionGlobalAi() != null) {
            calificacion.setObservacionGlobal(dto.getObservacionGlobalAi());
        }
        Calificacion saved = repository.save(calificacion);

        if (dto.getFeedbacks() != null) {
            for (AiFeedbackDTO fb : dto.getFeedbacks()) {
                FeedbackCalificacion entidad = new FeedbackCalificacion();
                entidad.setCalificacion(saved);
                entidad.setObservacion(fb.getObservacion());
                entidad.setAutor(fb.getAutor());
                entidad.setFecha(LocalDateTime.now());
                feedbackRepo.save(entidad);
            }
        }

        // Enviar notificación de calificación con IA
        enviarNotificacion("calificacion.ia.aplicada", Map.of(
            "id", saved.getId(),
            "grabacionId", saved.getGrabacionId(),
            "puntajeFinal", saved.getPuntajeGlobal(),
            "detallesCount", dto.getDetalles().size()
        ));

        // Obtener los detalles actualizados para incluirlos en la respuesta
        List<DetalleCalificacion> detallesActualizados = detalleRepo.findByCalificacionId(saved.getId());

        return CalificacionMapper.toDTO(saved, detallesActualizados);
    }
    
    /**
     * Envía notificación al servicio WebSocket
     */
    private void enviarNotificacion(String evento, Map<String, Object> payload) {
        try {
            String url = wsNotificationUrl + "/notify?token=" + wsNotificationToken;
            
            Map<String, Object> notificationData = new HashMap<>();
            notificationData.put("event", evento);
            
            Map<String, Object> enrichedPayload = new HashMap<>(payload);
            enrichedPayload.put("timestamp", LocalDateTime.now().toString());
            enrichedPayload.put("source", "calificacion-java");
            notificationData.put("payload", enrichedPayload);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(notificationData, headers);
            
            restTemplate.postForObject(url, request, String.class);
            
            System.out.println("📡 Notificación enviada: " + evento);
        } catch (Exception e) {
            System.err.println("❌ Error enviando notificación " + evento + ": " + e.getMessage());
            // No lanzamos la excepción para que no afecte la operación principal
        }
    }
}
