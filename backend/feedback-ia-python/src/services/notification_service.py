"""
Servicio para enviar notificaciones al WebSocket
"""
import os
import requests
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.ws_url = os.getenv('WS_NOTIFICATION_URL', 'http://localhost:9000')
        self.token = os.getenv('WS_NOTIFICATION_TOKEN', 'dev')
        self.timeout = 5  # segundos

    def send_notification(self, event: str, payload: Dict[str, Any]) -> bool:
        """
        Envía una notificación al servicio WebSocket
        
        Args:
            event: Nombre del evento
            payload: Datos del evento
            
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
        try:
            # Enriquecer payload con metadatos
            enriched_payload = {
                **payload,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'feedback-ia-python'
            }
            
            # Preparar datos de la notificación
            notification_data = {
                'event': event,
                'payload': enriched_payload
            }
            
            # Enviar petición POST
            response = requests.post(
                f"{self.ws_url}/notify",
                json=notification_data,
                params={'token': self.token},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"📡 Notificación enviada: {event}")
                return True
            else:
                logger.error(f"❌ Error enviando notificación {event}: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error(f"❌ Timeout enviando notificación {event}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de conexión enviando notificación {event}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado enviando notificación {event}: {str(e)}")
            return False

    def send_feedback_created(self, feedback_data: Dict[str, Any]) -> bool:
        """Envía notificación de feedback creado"""
        return self.send_notification('feedback.creado', {
            'id': feedback_data.get('id'),
            'grabacionId': feedback_data.get('grabacion_id'),
            'parametroId': feedback_data.get('parametro_id'),
            'valor': feedback_data.get('valor'),
            'esManual': feedback_data.get('es_manual', False)
        })

    def send_ai_analysis_completed(self, analysis_data: Dict[str, Any]) -> bool:
        """Envía notificación de análisis de IA completado"""
        return self.send_notification('feedback.ia.completado', {
            'grabacionId': analysis_data.get('grabacion_id'),
            'totalFeedbacks': analysis_data.get('total_feedbacks', 0),
            'promedioScore': analysis_data.get('promedio_score', 0),
            'parametrosAnalizados': analysis_data.get('parametros_analizados', [])
        })

    def send_metric_created(self, metric_data: Dict[str, Any]) -> bool:
        """Envía notificación de métrica creada"""
        return self.send_notification('metrica.creada', {
            'id': metric_data.get('id'),
            'nombre': metric_data.get('nombre'),
            'tipoMetricaId': metric_data.get('tipo_metrica_id')
        })

# Instancia global del servicio
notification_service = NotificationService()