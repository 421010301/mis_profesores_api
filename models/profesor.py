from sqlalchemy import Column, Integer, String, Text
from database.base import Base

class Profesor(Base):
    __tablename__ = "profesores"

    id_profesor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    institucion = Column(String(255))
    departamento = Column(String(100))
    perfil_url = Column(Text)
