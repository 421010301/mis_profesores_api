from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde .env

# URL de conexión (por ejemplo: mysql+pymysql://admin:adminpass@db:3306/mis_profesores)
DATABASE_URL = os.getenv("DATABASE_URL")

# Crea el motor de conexión
engine = create_engine(DATABASE_URL)

# Crea una clase de sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para usar en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
