from typing import Dict
import uuid

# Almacén simple en memoria: conversation_id → profesor_id
conversaciones: Dict[str, int] = {}

def nueva_conversacion(profesor_id: int) -> str:
    conversation_id = str(uuid.uuid4())
    conversaciones[conversation_id] = profesor_id
    return conversation_id

def obtener_profesor_conversacion(conversation_id: str) -> int | None:
    return conversaciones.get(conversation_id)

def obtener_todas_conversaciones() -> Dict[str, int]:
    return conversaciones