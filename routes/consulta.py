from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.gemini_service import extraer_nombre_profesor_ia, generar_resumen_profesor, generar_respuesta
from database.session import get_db
from services.db_service import buscar_profesores_por_nombre, obtener_comentarios_profesor, obtener_profesor
from services.conversacion_contexto import nueva_conversacion, obtener_profesor_conversacion
from services.conversacion_contexto import obtener_todas_conversaciones

router = APIRouter()

class MensajeUsuario(BaseModel):
    mensaje: str
    conversation_id: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "mensaje": "Ahora dime del profesor Ramírez",
                "conversation_id": "e68e8a2c-0df9-4e2a-9fcd-bd7ccfe03b97"
            }
        }

class PreguntaConversacion(BaseModel):
    conversation_id: str
    mensaje: str

    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "e68e8a2c-0df9-4e2a-9fcd-bd7ccfe03b97",
                "mensaje": "¿Hace exámenes sorpresa o pasa lista?"
            }
        }


@router.post("/consulta")
def consulta_profesor(request: MensajeUsuario, db: Session = Depends(get_db)):
    # 1. Intentar extraer un nombre
    nombre_extraido = extraer_nombre_profesor_ia(request.mensaje)

    if not nombre_extraido:
        # Si no hay nombre pero hay conversation_id → redirigir a /pregunta
        if request.conversation_id:
            profesor_id = obtener_profesor_conversacion(request.conversation_id)
            if not profesor_id:
                return JSONResponse(status_code=404, content={"error": "Conversación no encontrada."})
            profesor = obtener_profesor(db, profesor_id)
            comentarios = obtener_comentarios_profesor(db, profesor_id)
            respuesta = generar_respuesta(
                nombre_profesor=profesor.nombre,
                departamento=profesor.departamento or "Departamento desconocido",
                comentarios=comentarios,
                pregunta_usuario=request.mensaje
            )
            return {"respuesta": respuesta}
        # Si no hay nombre ni contexto → error
        return JSONResponse(
            status_code=400,
            content={"error": "No se detectó un nombre de profesor y no se proporcionó contexto de conversación."}
        )

    # 2. Buscar profesores por nombre extraído
    profesores = buscar_profesores_por_nombre(db, nombre_extraido)

    if not profesores:
        return JSONResponse(
            status_code=404,
            content={"status": "sin_coincidencias", "mensaje": f"No se encontró ningún profesor que coincida con '{nombre_extraido}'"}
        )

    if len(profesores) > 1:
        return {
            "status": "varios_resultados",
            "mensaje": f"Se encontraron varios profesores que coinciden con '{nombre_extraido}'",
            "opciones": [
                {"id": p.id_profesor, "nombre": p.nombre, "departamento": p.departamento}
                for p in profesores
            ]
        }

    # 3. Sólo un profesor encontrado → generar resumen
    profesor = profesores[0]
    comentarios = obtener_comentarios_profesor(db, profesor.id_profesor)
    resumen = generar_resumen_profesor(
        nombre_profesor=profesor.nombre,
        departamento=profesor.departamento or "Departamento desconocido",
        comentarios=comentarios
    )
    conversation_id = nueva_conversacion(profesor.id_profesor)

    return {
        "status": "ok",
        "profesor": {
            "id": profesor.id_profesor,
            "nombre": profesor.nombre,
            "departamento": profesor.departamento
        },
        "resumen": resumen,
        "conversation_id": conversation_id
    }


@router.post("/pregunta")
def preguntar_con_contexto(request: PreguntaConversacion, db: Session = Depends(get_db)):
    profesor_id = obtener_profesor_conversacion(request.conversation_id)

    if not profesor_id:
        return JSONResponse(status_code=404, content={"error": "Conversación no encontrada o expirada."})

    profesor = obtener_profesor(db, profesor_id)
    comentarios = obtener_comentarios_profesor(db, profesor_id)

    respuesta = generar_respuesta(
        nombre_profesor=profesor.nombre,
        departamento=profesor.departamento or "Departamento desconocido",
        comentarios=comentarios,
        pregunta_usuario=request.mensaje
    )

    return {"respuesta": respuesta}

@router.get("/conversaciones")
def listar_conversaciones():
    """
    Devuelve todas las conversaciones activas en memoria.
    """
    return obtener_todas_conversaciones()