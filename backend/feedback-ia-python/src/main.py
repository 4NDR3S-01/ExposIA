from fastapi import FastAPI
from src.api.endpoints import router
from src.database.connection import Base, engine

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Feedback Module API",
    description="API para gestionar feedbacks de grabaciones",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1", tags=["feedback"])

@app.get("/")
def root():
    return {"message": "Módulo de Feedback API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)