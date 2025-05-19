import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde el archivo .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
