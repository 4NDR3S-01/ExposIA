# filepath: /src/test_basic.py
"""
Prueba básica del sistema sin dependencias complejas.
"""
import os
import sys

# Configurar variables de entorno antes de importar
os.environ["API_KEY"] = "test-api-key-12345"
os.environ["DEBUG"] = "true"

# Añadir el directorio src al path
sys.path.insert(0, '/home/andres/Documentos/ExposIA/backend/feedback-ia-python/src')

def test_imports():
    """Prueba que las importaciones funcionen."""
    print("🔍 Probando importaciones...")
    
    try:
        from infrastructure.security.auth_middleware import AuthMiddleware
        print("✅ AuthMiddleware importado correctamente")
    except Exception as e:
        print(f"❌ Error importando AuthMiddleware: {e}")
    
    try:
        from domain.entities.feedback import Feedback
        print("✅ Feedback entity importado correctamente")
    except Exception as e:
        print(f"❌ Error importando Feedback: {e}")
    
    try:
        from domain.value_objects.feedback_score import FeedbackScore
        print("✅ FeedbackScore value object importado correctamente")
    except Exception as e:
        print(f"❌ Error importando FeedbackScore: {e}")


def test_auth_middleware():
    """Prueba el middleware de autenticación."""
    print("\n🔐 Probando middleware de autenticación...")
    
    try:
        from infrastructure.security.auth_middleware import AuthMiddleware
        
        auth = AuthMiddleware()
        print(f"✅ AuthMiddleware creado con API_KEY: {auth.api_key[:10]}...")
        print(f"✅ Modo debug: {auth.debug_mode}")
        
    except Exception as e:
        print(f"❌ Error probando AuthMiddleware: {e}")


def test_domain_entities():
    """Prueba las entidades de dominio."""
    print("\n🏗️ Probando entidades de dominio...")
    
    try:
        from domain.entities.feedback import Feedback
        from domain.value_objects.feedback_score import FeedbackScore
        
        # Crear un score válido
        score = FeedbackScore(85.0)
        print(f"✅ FeedbackScore creado: {score}")
        
        # Crear un feedback
        feedback = Feedback(
            id=None,
            grabacion_id=1,
            parametro_id=1,
            score=score,
            comentario="Test feedback",
            es_manual=True
        )
        print(f"✅ Feedback creado: {feedback}")
        
    except Exception as e:
        print(f"❌ Error probando entidades: {e}")


def test_basic_fastapi():
    """Prueba básica de FastAPI."""
    print("\n🚀 Probando FastAPI básico...")
    
    try:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        app = FastAPI()
        
        @app.get("/test")
        def test_endpoint():
            return {"message": "Test successful"}
        
        client = TestClient(app)
        response = client.get("/test")
        
        print(f"✅ FastAPI respuesta: {response.json()}")
        print(f"✅ Status code: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error probando FastAPI: {e}")


if __name__ == "__main__":
    print("🧪 Iniciando pruebas básicas del sistema...")
    
    test_imports()
    test_auth_middleware()
    test_domain_entities()
    test_basic_fastapi()
    
    print("\n✅ Pruebas básicas completadas!")
