from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.0-flash"

def generar_resumen_profesor(nombre_profesor: str, departamento: str, comentarios: list[str]) -> str:
    n_opiniones = len(comentarios)

    contexto = (
        f"Profesor: {nombre_profesor}\n"
        f"Departamento: {departamento}\n"
        f"Opiniones recientes:\n" +
        ("\n".join(f"- {c}" for c in comentarios) if comentarios else "No hay comentarios disponibles.")
    )

    prompt = (
        f"Resume en pocas frases cómo es el profesor según las opiniones siguientes.\n"
        f"Devuelve el resultado en Markdown, incluyendo una frase como:\n"
        f"**Basado en {n_opiniones} opiniones:** y luego el resumen.\n"
        f"Evita repetir frases literales. Sé claro, conciso y útil.\n\n"
        f"{contexto}"
    )

    config = types.GenerateContentConfig(
        system_instruction="Eres un asistente académico que resume de forma clara y precisa las opiniones estudiantiles sobre un profesor. No inventes información si no hay suficientes comentarios."
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        config=config,
        contents=[prompt]
    )

    return response.text.strip()

def extraer_nombre_profesor_ia(mensaje_usuario: str) -> str | None:
    """
    Usa Gemini para extraer el nombre del profesor mencionado en una oración natural.
    Devuelve solo el nombre (sin la palabra 'profesor' ni 'profesora').
    """
    prompt = (
        "Extrae solo el nombre completo del profesor o profesora que se menciona en la siguiente oración.\n"
        "Devuélvelo como una frase o nombre corto, sin incluir títulos como 'profesor', 'profa', etc.\n"
        "Si no hay ningún nombre, responde solo con la palabra 'ninguno'.\n\n"
        f"Mensaje: {mensaje_usuario}"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[prompt]
    )

    resultado = response.text.strip()

    # Si Gemini responde "ninguno", devolvemos None
    if resultado.lower() == "ninguno":
        return None

    # Devolver el nombre extraído
    return resultado

def generar_respuesta(nombre_profesor: str, departamento: str, comentarios: list[str], pregunta_usuario: str) -> str:
    contexto = (
        f"Profesor: {nombre_profesor}\n"
        f"Departamento: {departamento}\n"
        f"Comentarios recientes:\n" +
        ("\n".join(f"- {c}" for c in comentarios) if comentarios else "No hay comentarios.")
    )

    prompt = (
        f"El estudiante ha preguntado:\n«{pregunta_usuario}»\n\n"
        f"Con base en las opiniones anteriores sobre el profesor, responde de forma clara y directa.\n\n"
        f"{contexto}"
    )

    config = types.GenerateContentConfig(
        system_instruction=(
            "Eres un asistente académico claro y directo, sin saludos ni despedidas. "
            "No respondas preguntas que no sean sobre profesores o sobre un contexto académico. "
            "Si los comentarios no permiten responder con certeza, sé honesto y dilo claramente."
        )
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        config=config,
        contents=[prompt]
    )

    return response.text.strip()