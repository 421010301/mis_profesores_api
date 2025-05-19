from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from routes import consulta
from database.session import get_db
from sqlalchemy import text

app = FastAPI(
    title="Mis Profesores API",
    description="API para generar respuestas naturales sobre opiniones de profesores usando Gemini.",
    version="1.0.0"
)

# CORS (ajusta para producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Usa tu dominio real en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(consulta.router, prefix="/api")

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))   # consulta simple para probar la conexión
        return {"status": "ok", "message": "Conexión a la base de datos exitosa."}
    except SQLAlchemyError as e:
        return {"status": "error", "message": "Error al conectar con la base de datos.", "details": str(e)}
