from sqlalchemy.orm import Session
from models.profesor import Profesor
from models.evaluacion import Evaluacion

def obtener_profesor(db: Session, profesor_id: int) -> Profesor | None:
    return db.query(Profesor).filter(Profesor.id_profesor == profesor_id).first()

def buscar_profesores_por_nombre(db: Session, nombre: str) -> list:
    nombre = nombre.lower()
    return db.query(Profesor).filter(Profesor.nombre.ilike(f"%{nombre}%")).all()

def obtener_comentarios_profesor(db: Session, profesor_id: int, limite: int = 10) -> list[str]:
    resultados = (
        db.query(Evaluacion.comentario)
        .filter(Evaluacion.id_profesor == profesor_id)
        .filter(Evaluacion.comentario != None)
        .order_by(Evaluacion.fecha.desc())
        .limit(limite)
        .all()
    )
    return [r[0] for r in resultados if r[0]]
