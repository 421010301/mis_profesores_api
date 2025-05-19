from sqlalchemy import Column, Integer, String, Float, Text, Date
from database.base import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_profesor = Column(Integer, index=True)
    fecha = Column(Date)
    tipo_calificacion = Column(String(50))
    calidad = Column(Integer)
    facilidad = Column(Integer)
    calificacion_obtenida = Column(Float)
    interes_clase = Column(Integer)
    comentario = Column(Text)
    etiquetas_opinion = Column(Text)
    likes = Column(Integer)
    dislikes = Column(Integer)
    calificacion_general = Column(Float)
    nivel_dificultad = Column(Float)
    porcentaje_recomendacion = Column(String(10))
    id_materia = Column(Integer)
